from typing import Dict

USERAGENTS_FILE: str = 'useragents.txt'

HEADERS: Dict[str, str] = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "accept-charset": "cp1254,ISO-8859-9,utf-8;q=0.7,*;q=0.3",
    "accept-encoding": "gzip,deflate,sdch",
    "accept-language": "tr,tr-TR,en-US,en;q=0.8",
    "Upgrade-Insecure-Requests": "1",
}

STATIC_URLS: Dict[str, str] = {
    "cyberpuerta": "https://www.cyberpuerta.mx/"
}