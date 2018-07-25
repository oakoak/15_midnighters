import requests
import datetime


def load_attempts():
    response = requests.get(
        "https://devman.org/api/challenges/solution_attempts/?page=2"
    )
    for page in response.json()["records"]:

        yield page


def get_midnighters():
    midnighters = []
    for user in load_attempts():
        if datetime.datetime.utcfromtimestamp(user["timestamp"]).hour <= 6 \
                and user["username"] not in midnighters:
            midnighters.append(user["username"])
    return midnighters


def print_midnighters(midnighters):
    for midnighter in midnighters:
        print(midnighter)


if __name__ == '__main__':
    midnighters = get_midnighters()
    print_midnighters(midnighters)