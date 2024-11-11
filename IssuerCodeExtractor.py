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
        #Codes that don't have a table
        useless_issuer_codes = (
        'OPFO', 'PROT', 'VFPM', 'TTKO', 'OMOS', 'FKTL', 'INOV', 'CKBKO', 'KKST', 'GRDN', 'TSZS', 'JAKO', 'KULT', 'VSC',
        'LHND', 'LAJO', 'PTRS', 'OSPO', 'GDKM', 'VARG', 'CBNG', 'OBPP', 'FROT', 'JUSK', 'KORZ', 'TRUB', 'PELK', 'RINS',
        'TBKO', 'IJUG', 'KMPR', 'GRSN', 'ZUAS', 'PGGV', 'CDHV', 'BIKF', 'KDFO', 'SNBTO', 'SNBT', 'ENSA', 'MAGP', 'MLKR',
        'ELNC', 'MPTE', 'EDST', 'SKON', 'EUMK', 'ENER', 'ELMA')
        return [code for code in codes if
                not any(char.isdigit() for char in code)  and code not in useless_issuer_codes]

    def get_data(self) -> List[str]:
        return self.get_issuer_codes()
