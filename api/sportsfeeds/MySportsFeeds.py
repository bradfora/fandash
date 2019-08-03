from urllib.request import Request, urlopen
from urllib.error import URLError
from urllib import parse
import platform
import base64
import gzip

from util.constants import VERSION

_supported_auth_types = ["BASIC"]

_valid_feeds = [
    'current_season',
    'cumulative_player_stats',
    'full_game_schedule',
    'daily_game_schedule',
    'daily_player_stats',
    'game_playbyplay',
    'game_boxscore',
    'scoreboard',
    'overall_team_standings',
    'conference_team_standings',
    'division_team_standings',
    'player_gamelogs',
    'team_gamelogs',
    'roster_players',
    'game_startinglineup',
    'active_players',
    'player_injuries',
    'latest_updates',
    'daily_dfs'
]

_base_url = "https://www.mysportsfeeds.com/api/feed/pull"

_base_headers = {
    "Accept-Encoding": "gzip",
    "User-Agent": "app Python/{} ({})".format(VERSION, platform.platform())
}


class MySportsFeeds:
    """Supports the API for MySportsFeeds version 1"""

    def __init__(self, username, password, verbose=False):
        self._verbose = verbose

        self._username = username
        self._password = password

    def __verify_feed_name(self, feed):
        return feed in _valid_feeds

    def __verify_format(self, output_format):
        return output_format in ['json', 'xml', 'csv']

    def __league_url(self, league, feed, output_format, params):
        url = "{base_url}/{league}/{feed}.{output}".format(
            base_url=_base_url, league=league,
            feed=feed, output=output_format)

        url = url + "?" + parse.urlencode(params)
        return url

    def __league__season_url(self, league, season, feed, output_format, params):
        url = "{base_url}/{league}/{season}/{feed}.{output}".format(
            base_url=_base_url, league=league, season=season,
            feed=feed, output=output_format)

        url = url + "?" + parse.urlencode(params)
        return url

    def __auth(self):
        utf_auth = '{}:{}'.format(self._username, self._password).encode('utf-8')
        return "Basic " + base64.b64encode(utf_auth).decode('ascii')

    def get_data(self, **kwargs):
        # error check for missing args
        if not self.__auth:
            raise AssertionError("You must authenticate() before making requests.")

        league, season, feed, output_format = "", "", "", ""
        params = {}

        for key, val in kwargs.items():
            if str(key) == 'league':
                league = val
            elif str(key) == 'season':
                season = val
            elif str(key) == 'feed':
                feed = val
            elif str(key) == 'format':
                output_format = val
            else:
                params[key] = val

        if "force" not in params:
            params['force'] = 'false'

        if not self.__verify_feed_name(feed):
            raise ValueError("Unknown feed '" + feed + "'.")

        if not self.__verify_format(output_format):
            raise ValueError("Unsupported format '" + output_format + "'.")

        if feed == 'current_season':
            url = self.__league_url(league, feed, output_format, params)
        else:
            url = self.__league__season_url(league, season, feed, output_format, params)

        headers = {
            **_base_headers,
            'Authorization': self.__auth(),
        }

        if self._verbose:
            print("Making API request to '{}'.".format(url))
            print("  with headers:")
            print(headers)
            print(" and params:")
            print(params)

        try:
            req = Request(url, headers=headers)
            res = urlopen(req).read()
            res = gzip.decompress(res)
            return res

        except URLError as e:
            print(url)
            if hasattr(e, 'code'):
                if e.code == 304:
                    print("The content has not changed")
                # return content from database
                else:
                    print("The server couldn't fulfill the request")
                    print("Error code: ", e.code)
            if hasattr(e, 'reason'):
                print("Failed to reach a server.")
                print("Reason: ", e.reason)
            raise e
