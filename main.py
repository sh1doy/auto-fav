import json
import time
from requests_oauthlib import OAuth1Session
import config


class Autofav:

    def __init__(self):
        self.sess = OAuth1Session(
            config.CONSUMER_KEY,
            config.CONSUMER_KEY_SECRET,
            config.ACSESS_TOKEN,
            config.ACSESS_TOKEN_SECRET
        )
        self.keywords = config.KEYWORDS
        self.latest_id = 1

    def get_timeline(self):
        params = {
            "count": "200",
            "since_id": str(self.latest_id)
        }
        req = self.sess.get("https://api.twitter.com/1.1/statuses/home_timeline.json",
                            params=params)
        timeline = json.loads(req.text)
        return timeline

    def fav(self, tweet_id):
        params = {"id": tweet_id}
        self.sess.post("https://api.twitter.com/1.1/favorites/create.json",
                       params=params)

    def egosearh(self):
        timeline = self.get_timeline()
        for tweet in timeline[::-1]:
            for keyword in self.keywords:
                if keyword in tweet["text"]:
                    self.fav(tweet["id_str"])
                    print("Fav - {}: {}".format(tweet["user"]["name"], tweet["text"]))
                    break
            self.latest_id = tweet["id_str"]


def main():

    cls = Autofav()
    print("Session created.")

    while 1:
        cls.egosearh()
        time.sleep(config.INTERVAL)


if __name__ == '__main__':
    main()
