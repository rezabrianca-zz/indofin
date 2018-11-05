#!/usr/bin/python3
from slackclient import SlackClient
import os

def sendMessage(message):

    slack_token = os.getenv('SLACK_TOKEN')
    sc = SlackClient(slack_token)
    sc.api_call(
        'chat.postMessage',
        channel='DDNGMN7KK',
        text=message,
        username='Slack API'
        )
    return

def uploadFile(file, title):

    slack_token = os.getenv('SLACK_TOKEN')
    sc = SlackClient(slack_token)
    with open(file, 'rb') as f:
        sc.api_call(
            'files.upload',
            channels='DDNGMN7KK',
            file=f,
            username='Slack API',
            title=title
            )
    return
