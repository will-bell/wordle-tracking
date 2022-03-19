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


def format_two_stat_leaderboard(header: str, col1: pd.Series, col2: pd.Series) -> str:
    message = header

    for ((index, row1), (_, row2)) in zip(col1.iteritems(), col2.iteritems()):
        message += f'{index}: {row1:.2f}, {row2}\n'

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


def send_average_guesses_leaderboard(leaderboard: pd.Series):
    header = 'Average guesses leaderboard\n-----------------------------------------------\n'

    send_message_as_huey(format_one_stat_leaderboard(header, leaderboard))


def send_average_guesses_and_total_wordles_leaderboard(average_guesses_ldb: pd.Series, total_wordles_ldb: pd.Series):
    header = 'Average guesses and total wordles played\n-------------------------------------------------' \
             '------------------\n'

    send_message_as_huey(
        format_two_stat_leaderboard(header, average_guesses_ldb, total_wordles_ldb))


def send_leaderboard_to_test_group(leaderboard: pd.Series):
    header = 'Average guesses leaderboard\n-----------------------------------------------\n'

    send_message_to_test_group(format_one_stat_leaderboard(header, leaderboard))

