import os
import time
from slackclient import SlackClient


# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command, channel):
    response = "hey! greetings from vivacity!!!"
    if command.find("help")>=0:
        response = "How can I help you?"
    elif command.find("many fest")>=0:
        response = "Well there are 3 fests...vivacity, desportivos and plinth. "
    elif command.find("time")>=0 or command.find("date")>=0 or command.find("venue")>=0 or command.find("when are they organised")>=0 or command.find("organised")>=0:
        response = "These fests are generally conducted during first week of february and that too in LNMIIT."
    elif command.find("celebrity")>=0 or command.find("celebrities")>=0:
        response = "yes!!!many celebrities come to our fest either to judge or to perform!!!some of them are mohammad irfan, sushree shreya mishra, eureka band and many more...."  
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    else:
    	response = "I can't understand what you are saying...s"

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output:
                # return text after the @ mention, whitespace removed
                return output['text'].strip().lower(), output['channel']
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
