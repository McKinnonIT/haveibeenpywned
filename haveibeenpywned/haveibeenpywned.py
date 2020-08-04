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

    def _do_request(self, endpoint):
        resp = requests.get(urljoin(API_BASE_URL, endpoint), headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def get_all_breaches_for_account(self, email):
        return self._do_request(urljoin("breachedaccount", email))


if __name__ == "__main__":
    pass
