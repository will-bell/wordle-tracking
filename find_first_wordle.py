import time

import requests

from gets import extract_messages, get_n_last_messages, MESSAGES_URL, ACCESS_TOKEN


most_recent_msg = get_n_last_messages(1)[0]
most_recent_id = most_recent_msg['id']

done_counter = 0
next_before_id = most_recent_id
begin_scan_id = ''
while True:
    r = requests.get(MESSAGES_URL, params={"token": ACCESS_TOKEN, "limit": 100, "before_id": next_before_id})
    msg_batch = extract_messages(r)

    changed = False
    for i, msg in enumerate(msg_batch[:-1]):
        text = msg['text']
        if text:
            if 'Wordle' in text:
                begin_scan_id = msg_batch[i + 1]['id']

                changed = True

    if not changed:
        done_counter += 1
        if done_counter == 3:
            break
    else:
        done_counter = 0

    print(done_counter)

    next_before_id = msg_batch[-2]['id']

    time.sleep(1)


print(begin_scan_id)
