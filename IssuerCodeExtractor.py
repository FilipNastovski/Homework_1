from bs4 import BeautifulSoup
from typing import List
import requests

class IssuerCodeExtractor:
    def __init__(self):
        self.url = "https://www.mse.mk/en/stats/symbolhistory/ADIN"

    def get_issuer_codes(self) -> List[str]:
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')

        dropdown = soup.find('select', {'id': 'Code'})
        options = dropdown.find_all('option')
        codes = [option['value'] for option in options if option['value']]

        return codes

    def filter_codes(self, codes: List[str]) -> List[str]:
        return [code for code in codes if not any(char.isdigit() for char in code) and not code.startswith(('E', 'M', 'S'))]

    def get_data(self) -> List[str]:
        return self.get_issuer_codes()