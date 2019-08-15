import os
import slack
from dotenv import load_dotenv
from aiohttp.client_exceptions import ClientConnectorError
import scraper


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

    def remind_show_and_tell(self):
        """
        Reminds show and tell when the action is dispatched
        :return: None
        """
        self._post_message("It's time for show and tell, let's meet at the board room.")

    def remind_monday_meeting(self):
        """
        Remind friday meeting
        :return: None
        """
        self._post_message("It's time for weekly progress meeting")

    def remind_stand_up(self):
        """
        Remind every day stand up
        :return: None
        """
        self._post_message("It's time for stand up")

    def remind_break(self, minute, hour):
        if hour == 11:
            if minute in (30, 45):
                self._post_message(f"{60 - minute} minutes to break")
            elif minute == 0:
                self._post_message("It's time for break")
        elif hour == 12:
            if minute == 0:
                self._post_message("It's time for break, see you in an hour!")

    def post_tip(self):
        """
        DevTo or Medium API sends a post daily here
        :return:
        """
        print("Posting message to slack now...")
        message = "***TIPS FOR TODAY*** \n\n\n\n"
        scraper_obj = scraper.Scraper()
        for article in scraper_obj.get_articles():
            message += f"{article['title']} \n {article['link']} \n\n"
        print(message)
        self._post_message(message)
