import os
import sys
from random import choice
import twitter

api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"])

print api.VerifyCredentials()



def open_and_read_file(filenames):
    """Given a list of files, open them, read the text, and return one long
        string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Takes input text as string; returns dictionary of markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    key = choice(chains.keys())
    words = [key[0], key[1]]
    while key in chains:
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text)
        #
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.

        word = choice(chains[key])
        words.append(word)
        key = (key[1], word)

    generated_tweet = " ".join(words)

    if len(generated_tweet) < 140:
        return generated_tweet
    else:
        return make_text(chains)


def tweet_interface(chains):
    while True:
        continue_tweeting = raw_input("Press enter to tweet [q to quit]: ")
        if continue_tweeting == "":
            tweet_string = make_text(chains)
            status = api.PostUpdate(tweet_string)
            all_tweets = api.GetUserTimeline(screen_name='markovtweetbot1')
            group_of_all_tweets = [s.text for s in all_tweets]
            print "The last tweet was: ", group_of_all_tweets[1]
            print "Just tweeted: ", status.text
        elif continue_tweeting == "q":
            break
        else:
            print "Not a valid input."
            


# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain as a dictionary
chains = make_chains(text)

# Write a new function tweet, that will take chains (dictionary) as input and returns a tweet string


# tweet(chains)
tweet_interface(chains)