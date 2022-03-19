import pandas as pd
import requests

GROUPME_API_URL = 'https://api.groupme.com/v3/bots/post'
HUEY_BOT_ID = '1484862e4299309c77fcce5fc1'
HUEY_TEST_BOT_ID = 'f5824e65b3ede2d08322bacfc3'


def format_one_stat_leaderboard(header: str, leaderboard: pd.Series) -> str:
    message = header

    for index, row in leaderboard.iteritems():
        message += f'{index}: {row:.2f}\n'

    return message


def send_message_as_huey(message: str):
    data = {
            'bot_id': HUEY_BOT_ID,
            'text':   message,
            }

    requests.post(url=GROUPME_API_URL, json=data)


def send_message_to_test_group(message: str):
    data = {
        'bot_id': HUEY_TEST_BOT_ID,
        'text':   message,
    }
    requests.post(url=GROUPME_API_URL, json=data)


def send_leaderboard_as_huey(leaderboard: pd.Series):
    header = 'Average guesses leaderboard\n-----------------------------------------------\n'

    send_message_as_huey(format_one_stat_leaderboard(header, leaderboard))


def send_leaderboard_to_test_group(leaderboard: pd.Series):
    header = 'Average guesses leaderboard\n-----------------------------------------------\n'

    send_message_to_test_group(format_one_stat_leaderboard(header, leaderboard))

