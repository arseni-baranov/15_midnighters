import requests
import pytz
from datetime import datetime


def load_attempts():
    devman_api = "https://devman.org/api/challenges/solution_attempts?page={page}"
    number_of_pages = requests.get(devman_api.format(page=1)).json()['number_of_pages']

    for page in range(1, number_of_pages):
        response = requests.get(devman_api.format(page=page)).json()
        for entry in response['records']:
            yield entry


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
