import re
import requests
from ratelimit import limits, sleep_and_retry
from ratelimit.exception import RateLimitException
from posixpath import join as urljoin

API_BASE_URL = "https://haveibeenpwned.com/api/v3/"


class Pywned:
    def __init__(self, api_key):
        """haveibeenpwned.com API setup class, contains required headers, api key etc

        Args:
            api_key (string): Your haveibeenpwned.com API key
        """
        self._api_key = api_key
        self.headers = {
            "hibp-api-key": api_key,
            "user-agent": "haveibeenpywned.py",
        }
        """Dict of additional headers required for api calls to the haveibeenpwned.com
        api"""

    @sleep_and_retry
    @limits(calls=1, period=1.7)
    def _do_request(self, endpoint, params=None):
        """Internal method for building request url and performing HTTP request to the
        haveibeenpwned.com API

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
        print(urljoin(API_BASE_URL, endpoint))
        if resp.status_code == 404:
            return []
        if resp.status_code == 429:
            period_remaining = int(
                re.match(r"\D*(\d+)\D*", resp.json()["message"]).group(1)
            )
            raise RateLimitException(
                message=resp.json()["message"], period_remaining=period_remaining
            )
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
            list: Details of breaches for an email (account)
        """
        return self._do_request(
            urljoin("breachedaccount", email),
            params={"truncateResponse": truncate_response},
        )

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

    def get_all_breached_sites(self, domain=None):
        """Return the details of every breach

        Args:
            domain (string, optional): Filters the result set to only breaches against
                the domain specified. It is possible that one site (and consequently
                domain), is compromised on multiple occasions. Defaults to None.

        Returns:
            list: Details of all breached sites.
        """
        if domain:
            return self._do_request("breaches", params={"domain": domain})
        return self._do_request("breaches")

    def get_breached_site(self, name):
        """Returns a single breach by breach "name". This is the stable value which may
        or may not be the same as the reach "title" (which can change).

        Args:
            name (string): Breach site name to lookup

        Returns:
            dict: Details of a single breach.
        """
        return self._do_request(urljoin("breach", name))

    def get_data_classes(self):
        """Returns all "data classes". A "data class" is an attribute of a record
        compromised in a breach. For example, many breaches expose data classes such as
        "Email addresses" and "Passwords".

        Returns:
            list: Data class names
        """
        return self._do_request("dataclasses")

    def get_all_pastes_for_account(self, email):
        """Returns all pastes for an account (email)

        Args:
            email (string): Email (account) to search

        Returns:
            list: Details of each paste for an email (account)
        """
        return self._do_request(urljoin("pasteaccount", email))


if __name__ == "__main__":
    pass
