import pandas as pd
import numpy as np


def get_data_start_ind(text: str) -> int:
    return text.find('Wordle')


def extract_wordle_number(message):
    # Get the text
    text = message['text']

    # Extract the Wordle number
    start_ind = get_data_start_ind(text)
    wordle_num = int(text[start_ind + 7: start_ind + 10])

    return wordle_num


def extract_wordle_guesses(message):
    # Get the text
    text = message['text']

    # Extract the Wordle attempts
    start_ind = get_data_start_ind(text)
    wordle_guesses = text[start_ind + 11]

    if wordle_guesses == 'X':
        wordle_guesses = 7
    else:
        wordle_guesses = int(wordle_guesses)

    return wordle_guesses


def extract_to_dataframe(messages) -> pd.DataFrame:
    first_wordle_num = extract_wordle_number(messages[0])

    data = {}

    for msg in messages:
        # Get the name of the player
        name = msg['name']

        # Extract the Wordle data
        number = extract_wordle_number(msg)
        guesses = extract_wordle_guesses(msg)

        wordle_index = number - first_wordle_num
        if name not in data.keys():
            data[name] = [np.nan] * wordle_index + [guesses]
        else:
            data[name] += [np.nan] * (wordle_index - len(data[name]))
            data[name] += [guesses]

    most_wordles = -1
    for k, v in data.items():
        if len(v) > most_wordles:
            most_wordles = len(v)

    for k, v in data.items():
        data[k] += [np.nan] * (most_wordles - len(v))
        data[k] = pd.array(data[k], dtype='Int64')

    keys = list(data.keys())
    for k in keys:
        new_k = k.split(' ')[0]
        new_k = 'Kevin' if new_k == 'William' else new_k
        new_k = 'Godless Cheater' if new_k == 'Grady' else new_k
        data[new_k] = data.pop(k)

    cols = first_wordle_num + np.arange(0, most_wordles)
    return pd.DataFrame.from_dict(data, orient='index', columns=cols)
