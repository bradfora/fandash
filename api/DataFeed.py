from api.sportsfeeds.MySportsFeeds import MySportsFeeds
from config.settings import MY_SPORTS_FEEDS_USERNAME, MY_SPORTS_FEEDS_PASSWORD

supported_providers = ["sports-feeds"]


class SportsFeedsData:
    supported_versions = ["1"]


provider_versions = {"sports-feeds": SportsFeedsData.supported_versions}


class DataFeedWrapper:
    """Wrapper for requesting data from verified providers"""

    # Factory design pattern to assign the correct provider/version class
    def __init__(self, provider="sports-feeds", version="1", verbose=False):
        self.__verify_provider(provider)
        self.__verify_version(provider, version)

        self._provider = provider
        self._version = version

        if self._provider == "sports-feeds":
            if self._version == "1":
                self.api_instance = MySportsFeeds(
                    username=MY_SPORTS_FEEDS_USERNAME, password=MY_SPORTS_FEEDS_PASSWORD, verbose=verbose
                )

    # Private method to ensure that provider is a known & valid provider
    def __verify_provider(self, provider):
        if str(provider) not in supported_providers:
            raise ValueError("Unrecognized data feed provider {}. Supported providers are {}."
                             .format(provider, supported_providers))

    # Private method to ensure that version is known & valid for provider
    def __verify_version(self, provider, version):
        if str(version) not in provider_versions[str(provider)]:
            raise ValueError("Unrecognized version {} for {}. Supported versions are {}"
                             .format(version, provider, provider_versions[provider]))

    # Retrieves the data requested with the provided arguments
    def get_data(self, **kwargs):
        return self.api_instance.get_data(**kwargs)
