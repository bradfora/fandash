from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(verbose=True)


def get_var(key):
    try:
        return os.environ[key]
    except KeyError as e:
        raise EnvironmentError('Missing required configuration setting {}'.format(key)) from None


MY_SPORTS_FEEDS_USERNAME = get_var('MY_SPORTS_FEEDS_USERNAME')
MY_SPORTS_FEEDS_PASSWORD = get_var('MY_SPORTS_FEEDS_PASSWORD')
