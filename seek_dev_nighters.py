import requests
import pytz
from datetime import datetime

DEVMAN_API = "https://devman.org/api/challenges/solution_attempts"


def load_attempts():
    page_number = 1
    number_of_pages = 1

    while page_number <= number_of_pages:
        response = requests.get(DEVMAN_API, params={'page': page_number}).json()
        number_of_pages = int(response['number_of_pages'])

        for entry in response['records']:
            yield entry

        page_number += 1


def get_midnighters(records):
    for entry in records:
        dt = get_datetime(entry['timestamp'], entry['timezone'])
        if dt and dt.hour in range(1, 5):
            yield entry['username'], dt


def get_datetime(timestamp, timezone):
    if timestamp is None or timezone is None:
        return None
    return datetime.fromtimestamp(timestamp, pytz.timezone(timezone))


def main():
    for user, dt in get_midnighters(load_attempts()):
        print('"{0}" sent task on {1} at {2}'.format(user, dt.strftime('%d-%m-%Y'), dt.strftime('%H:%M %Z')))


if __name__ == '__main__':
 main()
