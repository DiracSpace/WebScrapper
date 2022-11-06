from exceptions.Exceptions import KeyNotFoundError
from modules.WebRequests import WebRequestMethods
from models.Constants import STATIC_URLS, HEADERS

def make_request(staticUrlKey: str):
    """
        entry point for invoking and testing
        core functions
    """

    # TODO: find a way to make dynammic parameters
    params = {
        "cl": "search",
        "searchparam": "be quiet"
    }

    if staticUrlKey not in STATIC_URLS:
        raise KeyNotFoundError("Cannot find key in STATIC_URLS")

    web_requests = WebRequestMethods(
        STATIC_URLS.get(staticUrlKey),
        params,
        HEADERS
    )

    web_content = web_requests.make_request_return_content()
    search_results = web_requests.parse_content(web_content)

    for result in search_results:
        print (f'Title: {result.title}')
        print (f'Product price: {result.price}')
        print (f'Delivery cost: {result.delivery}\n')

make_request('cyberpuerta')
