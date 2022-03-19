from gets import get_all_wordle_messages
from analysis import extract_to_dataframe
from messaging import send_average_guesses_and_total_wordles_leaderboard

if __name__ == '__main__':
    # Scrape the GroupMe messages
    msgs = get_all_wordle_messages()

    # Parse the messages to get the Wordle data, and keep it in a pandas dataframe for analysis
    df = extract_to_dataframe(msgs)

    # Get the average number of guesses each player has used
    average_guesses = df.mean(axis=1)
    sort_ind = average_guesses.argsort().values
    average_guesses_leaderboard = average_guesses.iloc[sort_ind]
    print(average_guesses_leaderboard)
    
    # Count the number of Wordles each person has played
    played_wordle = df > 0
    total_wordles_leaderboard = played_wordle.sum(axis=1)
    total_wordles_leaderboard = total_wordles_leaderboard.iloc[sort_ind]
    print(total_wordles_leaderboard)

    # Send a message with the leaderboards
    send_average_guesses_and_total_wordles_leaderboard(average_guesses_leaderboard, total_wordles_leaderboard)
