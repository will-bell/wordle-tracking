from gets import get_all_wordle_messages
from analysis import extract_to_dataframe
from messaging import send_leaderboard_as_huey

if __name__ == '__main__':
    msgs = get_all_wordle_messages()

    df = extract_to_dataframe(msgs)
    print(df)

    leader_board = df.mean(axis=1).sort_values()
    print(leader_board)

    send_leaderboard_as_huey(leader_board)
