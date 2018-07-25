import requests
import pytz
import datetime


def load_attempts(dev_url):
    page_number = 0
    while True:
        page_number += 1
        payload = {'page': page_number}
        data_from_page = requests.get(dev_url, params=payload).json()
        for record in data_from_page["records"]:
            yield record
        if page_number == data_from_page["number_of_pages"]:
            break


def get_local_user_time(attempt):
    time_zone = pytz.timezone(attempt['timezone'])
    return datetime.datetime.fromtimestamp(attempt['timestamp'], time_zone)


def get_midnighters(attempts, hour_from, hour_to):
    midnighters = set()
    for attempt in attempts:
        user_name = attempt["username"]
        if hour_from <= get_local_user_time(attempt).hour <= hour_to:
            midnighters.add(user_name)
    return midnighters


def print_midnighters(midnighters):
    print("\n".join(midnighters))


if __name__ == "__main__":
    dev_url = "https://devman.org/api/challenges/solution_attempts/"
    hour_from = 0
    hour_to = 6

    try:
        attempt = load_attempts(dev_url)
        midnighters = get_midnighters(attempt, hour_from, hour_to)
    except requests.HTTPError as error:
        exit("Error: {}".format(error))

    print_midnighters(midnighters)
