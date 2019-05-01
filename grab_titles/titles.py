import config
import praw
import os

submission_id_file = 'submission_titles_id.txt'


def authenticate():
    print('Authenticating User....')
    reddit = praw.Reddit(client_id=config.client_id,
                         client_secret=config.client_secret,
                         user_agent=config.user_agent,
                         username=config.username,
                         password=config.password)
    print("User '{user}' Authenticated".format(user=reddit.user.me()))
    return reddit


reddit = authenticate()


def get_submission_ids(file):
    if not os.path.isfile(file):
        replied_ids = []
    else:
        with open(file, 'r') as fin:
            replied_ids = fin.read()
            replied_ids = replied_ids.split('\n')
            replied_ids = list(filter(None, replied_ids))

    return replied_ids


def main():
    submission_ids = get_submission_ids(submission_id_file)

    while True:
        SUBREDDIT = input('Enter Subreddit: ')
        try:
            reddit.subreddits.search_by_name(SUBREDDIT, exact=True)

            while True:
                try:
                    LIMIT = int(input('Enter amount of posts to grab titles from: '))
                    break
                except ValueError:
                    print('Must enter a digit not a letter!')

            break

        except Exception as e:
            print('Invalid Subreddit')
            print('Check spelling and enter again: ')

    titles = []

    for submission in reddit.subreddit(SUBREDDIT).hot(limit=LIMIT):
        if submission.id not in submission_ids:
            print('Found New Title')
            with open('submission_titles_id.txt', 'a') as fout:
                fout.write(submission.id + '\n')

            titles.append(submission.title)

    with open('subreddit_titles.txt', 'a') as fout:
        for title in titles:
            fout.write(title)
            fout.write('\n')

    print("Program complete")


if __name__ == '__main__':
    main()
