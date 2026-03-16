from requests_oauthlib import OAuth1Session

CONSUMER_KEY = "4Way2yDfVwHsEZxJHuPu8rAGi"
CONSUMER_SECRET = "yfCQMsWqa1KF7cuDGbT9Sv1pEKaN8YQYTDIv8l94kUlsDLrgCD"


class Tweet:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating the Tweet object and authenticating...")
            cls._instance = super(Tweet, cls).__new__(cls)
            cls._instance.oauth = None
            cls._instance.authenticate()
        return cls._instance

    def authenticate(self):
        request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"

        oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
        fetch_response = oauth.fetch_request_token(request_token_url)

        resource_owner_key = fetch_response.get("oauth_token")
        resource_owner_secret = fetch_response.get("oauth_token_secret")

        base_authorization_url = "https://api.twitter.com/oauth/authorize"
        authorization_url = oauth.authorization_url(base_authorization_url)
        print(f"Please go here and authorize: {authorization_url}")
        verifier = input("Paste the PIN here: ")

        access_token_url = "https://api.twitter.com/oauth/access_token"
        oauth = OAuth1Session(
            CONSUMER_KEY,
            client_secret=CONSUMER_SECRET,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=verifier,
        )
        oauth_tokens = oauth.fetch_access_token(access_token_url)

        self.oauth = OAuth1Session(
            CONSUMER_KEY,
            client_secret=CONSUMER_SECRET,
            resource_owner_key=oauth_tokens["oauth_token"],
            resource_owner_secret=oauth_tokens["oauth_token_secret"],
        )
        print("Authentication Successful!")

    def make_tweet(self, tweet_data):
        if not self.oauth:
            raise ValueError("Authentication failed!")

        response = self.oauth.post(
            "https://api.twitter.com/2/tweets",
            json=tweet_data,
        )

        if response.status_code != 201:
            raise Exception(
                f"Request returned an error: {response.status_code} {response.text}"
            )

        print(f"Tweet Posted! Response code: {response.status_code}")
        return response.json()
