from datetime import datetime
import time
import bot
import os
from dotenv import load_dotenv
import slack
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import json


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._html("hi!"))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        data_string = self.rfile.read(int(self.headers['Content-Length']))
        body = json.loads(data_string)
        self.wfile.write(bytes(body['challenge'], encoding='utf-8'))


with socketserver.TCPServer(("", 8000), S) as httpd:
    print("Server up . .. ")
    httpd.serve_forever()

bot_obj = bot.Bot(os.getenv("CHANNEL"))


@slack.RTMClient.run_on(event="app_mention")
def say_hello():
    bot_obj.say_hello()


def worker():
    load_dotenv()

    while True:
        date_today = datetime.now().timetuple()
        everyday = date_today.tm_wday in range(0, 5)

        print(f"{date_today.tm_hour, date_today.tm_min} Making a new check cause it's a 15 mins interval")
        # bot_obj._post_message("So good to have a name of my own :smiley: ")
        # Check for Friday show and tell
        if date_today.tm_wday == 4 and date_today.tm_hour in (15, 16) and date_today.tm_min in (30, 45, 0):
            bot_obj.remind_show_and_tell(date_today.tm_hour, date_today.tm_min)
        elif date_today.tm_wday == 0 and date_today.tm_hour in (8, 9) and date_today.tm_min in (30, 45, 0):
            bot_obj.remind_monday_meeting(date_today.tm_hour, date_today.tm_min)
        elif everyday and (date_today.tm_hour, date_today.tm_min) == (9, 30):
            bot_obj.remind_stand_up()
        elif everyday and date_today.tm_hour in (11, 12) and date_today.tm_min in (30, 45, 0):
            bot_obj.remind_break(date_today.tm_hour, date_today.tm_min)
        elif everyday and (date_today.tm_hour, date_today.tm_min) == (13, 0):
            bot_obj.post_tip()
        elif date_today.tm_wday == 0 and (date_today.tm_hour, date_today.tm_min) == (10, 0):
            bot_obj.remind_work()
        # elif everyday and date_today.tm_min == 0 and date_today.tm_hour % 2 == 0:
        #     bot.Bot.post_google_form_tip()
        elif date_today.tm_wday == 2 and date_today.tm_hour in (14, 15) and date_today.tm_min in (30, 45, 0):
            bot_obj.remind_skillshare(date_today.tm_hour, date_today.tm_min)
        # Making sure the interval is 15 mins but sleep all weekend

        if date_today.tm_wday == 4 and date_today.tm_hour == 18:
            sleep_time = 194400
        elif date_today.tm_min == 0 or (15 % date_today.tm_min == 0 and date_today.tm_min > 1):
            sleep_time = 15 * 60
        else:
            sleep_time = (15 - (date_today.tm_min % 15)) * 60

        time.sleep(sleep_time)


worker()

