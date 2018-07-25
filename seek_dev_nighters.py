import requests
import pytz
import datetime


def load_attempts(dev_url):
    response = requests.get(dev_url).json()
    for page in response["records"]:
        yield page


def get_local_user_time(attempt):
    time_zone = pytz.timezone(attempt['timezone'])
    return datetime.datetime.fromtimestamp(attempt['timestamp'], time_zone)


def get_midnighters(attempt, time_from, time_to):
    midnighters = []
    for user in attempt:
        user_name = user["username"]
        if time_from <= get_local_user_time(user).hour <= time_to \
                and user_name not in midnighters:
            midnighters.append(user_name)
    return midnighters


def print_midnighters(midnighters):
    for midnighter in midnighters:
        print(midnighter)


if __name__ == '__main__':
    dev_url = "https://devman.org/api/challenges/solution_attempts/?page=2"
    time_from = 0
    time_to = 6

    try:
        attempt = load_attempts(dev_url)
        midnighters = get_midnighters(attempt, time_from, time_to)
    except requests.HTTPError as error:
        exit("Error: {}".format(error))

    print_midnighters(midnighters)
