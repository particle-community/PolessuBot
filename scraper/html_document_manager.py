from typing import Dict, List, Generator

import requests
from bs4 import BeautifulSoup


class HtmlDocumentManager:
    @staticmethod
    def get_document(address: str, params: Dict[str, str] = None) -> BeautifulSoup:
        with requests.get(url=address, params=params) as response:
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")

    @staticmethod
    def get_documents(addresses: List[str]) -> Generator[BeautifulSoup, None, None]:
        with requests.Session() as session:
            for address in addresses:
                with session.get(address) as response:
                    response.raise_for_status()
                    yield BeautifulSoup(response.text, "html.parser")
