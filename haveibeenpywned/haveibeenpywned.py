import requests
from posixpath import join as urljoin

API_BASE_URL = "https://haveibeenpwned.com/api/v3/"


class Pywned:
    def __init__(self, api_key=None):
        self._api_key = api_key
        self.headers = {
            "hibp-api-key": self.api_key,
            "user-agent": "haveibeenpywned.py",
        }

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        self._api_key = api_key
        self.headers["hibp-api-key"] = api_key

    def _do_request(self, endpoint, params=None):
        """Internal method for building request url and performing HTTP request to the
        HIBP API

        Args:
            endpoint (string): API endpoint string (eg. "breachedaccount" or "breach" )
            params (dict): HTTP request parameters to be passed to the HTTP request

        Returns:
            json: Requests response .json() object
        """
        resp = requests.get(
            urljoin(API_BASE_URL, endpoint), headers=self.headers, params=params
        )
        resp.raise_for_status()
        return resp.json()

    def get_all_breaches_for_account(self, email, truncate_response=True):
        """Returns a list of all breaches a particular account (email) has been involved
        in

        Args:
            email (string): Account (email address) to search for breaches
            truncate_response (boolean): Return a complete, non-truncated response of
            breach data

        Returns:
            list: Names of breaches the email (account) has been involved in
        """
        resp = self._do_request(
            urljoin("breachedaccount", email),
            params={"truncateResponse": truncate_response},
        )
        if not truncate_response:
            return resp
        return [breach["Name"] for breach in resp]

    def get_all_breached_sites(self):
        pass


if __name__ == "__main__":
    pass
