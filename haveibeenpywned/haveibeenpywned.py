import time
import requests
from posixpath import join as urljoin

API_BASE_URL = "https://haveibeenpwned.com/api/v3/"


class Pywned:
    def __init__(self, api_key, rate_limit=1.3):
        """HIBP API Setup Class, contains required headers, rate limits, api key etc

        Args:
            api_key (string): HIBP API Key 
            rate_limit (float, optional): [description]. Delay in between each request
                Defaults to 1.3.
        """
        self._api_key = api_key
        self.headers = {
            "hibp-api-key": api_key,
            "user-agent": "haveibeenpywned.py",
        }
        self.rate_limit = rate_limit

    def _do_request(self, endpoint, params=None):
        """Internal method for building request url and performing HTTP request to the
        HIBP API

        Args:
            endpoint (string): API endpoint string (eg. "breachedaccount" or "breach" )
            params (dict, Optional): HTTP request parameters to be passed to the HTTP
                request

        Returns:
            json: Requests response .json() object
        """

        resp = requests.get(
            urljoin(API_BASE_URL, endpoint), headers=self.headers, params=params
        )
        time.sleep(self.rate_limit)
        if resp.status_code == 404:
            return []
        resp.raise_for_status()
        return resp.json()

    def get_all_breaches_for_account(self, email, truncate_response=True):
        """Returns a list of all breaches a particular account (email) has been involved
        in

        Args:
            email (string): Account (email address) to search for breaches
            truncate_response (bool): Return a complete, non-truncated response of
            breach data (Default is True)

        Returns:
            list: Breaches for the email (account) has been involved in
        """
        resp = self._do_request(
            urljoin("breachedaccount", email),
            params={"truncateResponse": truncate_response},
        )
        return resp

    def get_all_breaches_names_for_account(self, email):
        """Returns a list of breach names a particular account (email) has been involved
        in

        Args:
            email (string): Account (email address) to search for breaches

        Returns:
            list: Names of breaches for the email (account) has been involved in
        """
        resp = self.get_all_breaches_for_account(email)
        return [breach["Name"] for breach in resp]


if __name__ == "__main__":
    pass
