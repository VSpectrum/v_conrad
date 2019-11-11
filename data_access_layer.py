from scraper import PyOrganizers
from pathlib import Path

from datetime import date
import json

class DAL:
    def access_data_by_year(self, desired_year: int, sorted_field=None):
        PyO_conferences = PyOrganizers().fetch_year(desired_year)
        filename = f'{desired_year}.json'
        if PyO_conferences:  # url scraper returned data
            #store data in json file (with year name)
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(PyO_conferences, jsonfile, indent=4)
                return PyO_conferences
        elif Path(filename).exists():  #no data returned .'. return jsonified stale data
            print("Fresh fetch failed. Using stored data!!!")
            with open(filename, 'r', encoding='utf-8') as jsonfile:
                conferences = json.load(jsonfile)
                return conferences
        else:  #no previously saved data, no scraper data, raise ERROR?
            raise Exception('Data for requested year is currently unattainable')

    def get_future_conferences(self):
        today = date.today()
        PyO_conferences = self.access_data_by_year(today.year)
        future_conferences = [conf for conf in PyO_conferences if conf['Start Date'] >= str(today)]
        future_conferences += self.access_data_by_year((today.year + 1))
        return future_conferences

    def set_reminder(self, id: str):
        filename = "reminders.txt"
        with open(filename, 'a', encoding='utf-8') as reminder_file:
            reminder_file.write(id + '\n')
    
    def get_reminders(self):
        filename = "reminders.txt"
        Path(filename).touch()
        with open(filename, 'r', encoding='utf-8') as reminder_file:
            reminders = [line.rstrip() for line in reminder_file]
            return [conf for conf in self.get_future_conferences() if conf["ID"] in reminders]

    def delete_reminder(self, id: str):
        filename = "reminders.txt"
        Path(filename).touch()
        with open(filename, 'r+', encoding='utf-8') as reminder_file:
            reminders = reminder_file.readlines()
            if id in reminders: reminders.remove(id)
            reminder_file.write(reminders)
