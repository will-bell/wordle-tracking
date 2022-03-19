import time

import requests


GROUPME_BASE_URL = "https://api.groupme.com/v3/"
ACCESS_TOKEN = "VL2kpeoZ9L9B7hgFtt9Dwa5iCcYnJIjaJ2wtipVZ"

MESSAGES_URL = GROUPME_BASE_URL + "groups/22167037/messages"

HUEY_BOT_ID = "1484862e4299309c77fcce5fc1"
HUEY_TEST_BOD_ID = "f5824e65b3ede2d08322bacfc3"

BEGIN_SCAN_ID = "164501938358404170"


def extract_messages(r: requests.Response):
    if r.status_code == 200:
        data = r.json()
        messages = data['response']['messages']

        return messages

    raise Exception("HTTP 400")


def get_n_last_messages(n_msgs: int):
    n_msgs = 100 if n_msgs > 100 else n_msgs

    r = requests.get(MESSAGES_URL, params={"token": ACCESS_TOKEN, "limit": n_msgs})

    return extract_messages(r)


def get_all_wordle_messages_since(start_id: str):
    most_recent_msg = get_n_last_messages(1)[0]
    most_recent_id = most_recent_msg['id']

    messages = []
    next_start_id = start_id
    while True:
        r = requests.get(MESSAGES_URL, params={"token": ACCESS_TOKEN, "limit": 100, "after_id": next_start_id})
        msg_batch = extract_messages(r)

        for msg in msg_batch:
            text = msg['text']
            if text:
                if 'Wordle' in text:
                    start_ind = text.find('Wordle')

                    # Check if a number follows 'Wordle' and exclude this message if that isn't the case
                    try:
                        int(text[start_ind + 7: start_ind + 10])
                        messages += [msg]
                    except:
                        pass

        next_start_id = msg_batch[-1]['id']

        if next_start_id == most_recent_id:
            return messages

        # Let's be nice to GroupMe
        time.sleep(1/20)


def get_all_wordle_messages():
    return get_all_wordle_messages_since(BEGIN_SCAN_ID)
