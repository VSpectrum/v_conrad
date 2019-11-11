from urllib import request
from ssl import _create_unverified_context
from csv import DictReader
from hashlib import md5
import logging
# pip install python-shorturl for future consideration of shortening unwieldly URLs
INFO_MAX_LENGTH = 45
ID_MAX_LENGTH = 3

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='errors.log'
)

class ConferenceScraper:
    def __init__(self): 
        #{Provided_field_name_from_scraped_dataset : Common_field_name_we_want_to_normalize_field_name_to}
        self.field_map = {
            'Subject': 'Name',
            'Website URL': 'Website',
            'Location': 'City',
            'Country': 'Country',
            'Start Date': 'Start Date',
            'End Date': 'End Date',
        }

        #list of dictionaries with the fields appropriately named from the above map
        self.parsed_mappings = []

    def hash_id(self, name: str, city: str, country: str):
        string_to_hash = ''.join([name, city, country]).lower().encode('utf-8')
        return md5(string_to_hash).hexdigest()[-ID_MAX_LENGTH:]


class PyOrganizers(ConferenceScraper):
    def parsed(self, conference_list: list):
        """
        returns a list of dictionary objects that contain the fields of interest (determined by field_map)
        """
        for conference in conference_list:
            conf_dict = {self.field_map[key]:val[:INFO_MAX_LENGTH].strip() for key, val in conference.items() if key in self.field_map.keys()}
            city_state = conf_dict['City'].split(',')[:2] if len(conf_dict['City'].split(','))>2 else [conf_dict['City'].split(',')[0], ""]
            conf_dict['City'], conf_dict['State'] = city_state
            conf_dict['ID'] = self.hash_id(conf_dict['Name'], conf_dict['City'], conf_dict['Country'])
            self.parsed_mappings.append(conf_dict)
        return self.parsed_mappings

    def fetch_year(self, year_of_interest: int):
        context = _create_unverified_context()
        url = f'https://raw.githubusercontent.com/python-organizers/conferences/master/{year_of_interest}.csv'
        try:
            with request.urlopen(url, context=context) as response:
                csv_text = response.read().decode("utf-8").splitlines()
                return self.parsed(DictReader(csv_text))
        except Exception as e:  #HTTPError, URLError
            logging.error(e, exc_info=True)
            return []
