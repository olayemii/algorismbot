import os
import slack
from dotenv import load_dotenv
from aiohttp.client_exceptions import ClientConnectorError
import scraper
import docsparser

class Bot:
    def __init__(self, channel):
        load_dotenv()
        self.channel = channel

        try:
            self.slack_client = slack.WebClient(token=os.getenv("SLACK_TOKEN"))
            self.connection_status = self.slack_client.rtm_connect(with_team_state=0)
        except ClientConnectorError as e:
            print(f"Error connecting with slack {e.strerror}")
            # exit(1)

    def _post_message(self, text):
        self.slack_client.chat_postMessage(channel=self.channel, text=text)

    def remind_show_and_tell(self, hour, min):
        """
        Reminds show and tell when the action is dispatched
        :return: None
        """
        print("Posting show and tell reminder")
        if hour == 16 and min == 0:
            self._post_message("*[REMINDER]* <!channel>, It's time for show and tell, let's meet at the board room.")
        elif hour == 15:
            self._post_message(f"*[REMINDER]* <!channel>, {60 - min} minutes to show and tell!")

    def remind_monday_meeting(self, hour, min):
        """
        Remind friday meeting
        :return: None
        """
        print("Posting monday reminder")
        if hour == 9 and min == 0:
            self._post_message("*[REMINDER]* <!channel>, It's time for weekly progress meeting, let's meet at the board room.")
        elif hour == 8:
            self._post_message(f"*[REMINDER]* <!channel>, {60 - min} minutes to weekly progress minute")

    def remind_stand_up(self):
        """
        Remind every day stand up
        :return: None
        """
        self._post_message("* <!channel> [REMINDER]* It's time for daily stand up")

    def remind_work(self):
        print("Posting work reminder")
        self._post_message('*[HELLO]* <!channel> , Do something good with time,'
                           ' dont just let it get wasted, live & code :grinning:')

    def remind_skillshare(self, hour, minute):
        if hour == 14:
            if minute in (30, 45):
                self._post_message(f" <!channel> {60 - minute} minutes to skill share")

        elif hour == 15:
            if minute == 0:
                self._post_message(" <!channel> It's time for skillshare!")


    def remind_break(self, hour, minute):
        print("Posting break reminder")
        if hour == 11:
            if minute in (30, 45):
                self._post_message(f" <!channel> {60 - minute} minutes to break")

        elif hour == 12:
            if minute == 0:
                self._post_message(" <!channel> It's time for break, see you in an hour!")

    def post_tip(self):
        """
        DevTo or Medium API sends a post daily here
        :return:
        """
        print("Posting tip to slack now...")
        message = "***TIPS FOR TODAY*** \n\n\n\n"
        scraper_obj = scraper.Scraper()
        for article in scraper_obj.get_articles():
            message += f"{article['title']} \n {article['link']} \n\n"
        message += "\n\n\n\n\n\n\n <!channel> :heart::slightly_smiling_face:  *I am Dele, a simple rule" \
                   " based bot, my code lives here: * https://github.com/olayemii/algorismbot " \
                   ":heart::slightly_smiling_face: "
        self._post_message(message)

    def post_google_form_tip(self):
        googlesheet_obj = docsparser.DocParser()
        self._post_message(googlesheet_obj.return_tip())

