from exceptions.Exceptions import HttpResponseFailedError
from modules.SearchResult import WebSearchResult
from modules.LibraryInstall import install
from typing import Dict, List
import os

try:
    import requests
except ImportError:
    install('requests')

try:
    from furl import furl
except ImportError:
    install('furl')

try:
    from bs4 import BeautifulSoup
except ImportError:
    install('beautifulsoup4')

try:
    import secrets
except ImportError:
    install('secrets')


class WebRequestMethods:
    """
        Class that will store the core functions for
        scrapping web data from sites
    """

    request_url: str = ""
    query_params: Dict[str, str] = {}
    request_headers: Dict[str, str] = {}

    def __init__(
        self,
        url: str,
        query_params,
        request_headers
    ):
        self.request_url = url
        self.query_params = query_params
        self.request_headers = request_headers

    def add_random_user(self, filename: str) -> str:
        """
            function that reads user agents
            and assigns new key-value to params
        """

        if filename is None:
            raise TypeError("Please provide a filename.")

        if not os.path.isfile(filename):
            raise FileNotFoundError("Could not find \"{filename}\".")

        if not os.access(filename, os.R_OK):
            raise PermissionError("Could not access \"{filename}\".")

        agents: List[str] = []
        with open(filename, encoding='utf8') as searched_file:
            for line in searched_file:
                if line is None:
                    raise TypeError("Line in file is empty!")

            agents.append(
                line.strip()
            )

        return secrets.choice(agents)

    def make_request_return_content(self) -> bytes:
        """
            function that makes an HTTP GET
            request and returns content
        """

        if self.request_url is None:
            raise TypeError("Please provide a correct url")

        print(f'HTTP GET request -> {self.request_url}\n')

        content: bytes = bytearray()
        with requests.Session() as session:
            response = session.get(
                self.request_url,
                headers=self.request_headers,
                params=self.query_params
            )

            if response.status_code != 200:
                raise HttpResponseFailedError(
                    f'HTTP Status -> {response.status_code}')

            content = response.content

        return content

    def remove_non_digits(self, url: str) -> str:
        """
            simple function that receives
            string and removes all charscters
        """
        return ''.join(c for c in url if c.isdigit())

    # TODO: separate into more dynamic way of parsing
    def parse_content(self, byteContent: bytes) -> list:
        """
            receives content from a website request
            and parses for title, pricing and other
            tags
        """

        if byteContent is None or byteContent is []:
            print('Content is empty.')
            return []

        content = byteContent.decode()
        result_list_id = "productList"

        soup = BeautifulSoup(content, "html.parser")

        results_url = [
            a["href"] for a in soup.find_all("a", {"class": "selected"})
        ]
        
        results_per_query = self.remove_non_digits(
            furl(results_url).args['_artperpage']
        )

        result_form_ids = [
            f'tobasket.productList-{i}' for i in range(1, int(results_per_query) + 1)
        ]

        result_list_ids = [
            f'{result_list_id}-{i}' for i in range(1, int(results_per_query) + 1)]

        print(f'There are {results_per_query} results per page!\n')

        forms = {}
        for product_id in result_form_ids:
            form = soup.find("form", {"name": product_id})
            forms[product_id] = form

        results: List[WebSearchResult] = []
        for index, (_, value) in enumerate(forms.items()):

            title = value.find(
                "a", {
                    "class": "emproduct_right_title",
                    "id": result_list_ids[index]
                }
            )["title"]

            price = value.find(
                "label", {
                    "class": "price"
                }
            ).string.strip()

            delivery_value = value.find(
                "span", {
                    "class": "deliveryvalue"
                }
            ).string.strip()

            result = WebSearchResult(title, price, delivery_value)
            results.append(result)

        return results
