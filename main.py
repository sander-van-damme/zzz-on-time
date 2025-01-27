#!/usr/bin/env python3

import os
import requests
import garth
from garth.exc import GarthException
from dotenv import load_dotenv
from pytz import timezone
from datetime import datetime, timedelta

load_dotenv()

TZ: datetime.tzinfo = timezone(os.getenv("TIMEZONE"))
BEDTIME: datetime = TZ.localize(
    datetime.combine(
        datetime.now(TZ).date() - timedelta(days=1),
        datetime.strptime(os.getenv("BEDTIME"), "%H:%M").time(),
    )
)
BEEMINDER_USER: str = os.getenv("BEEMINDER_USER")
BEEMINDER_TOKEN: str = os.getenv("BEEMINDER_TOKEN")
BEEMINDER_GOAL: str = os.getenv("BEEMINDER_GOAL")


def get_sleep_start_time(date: str) -> datetime:
    """
    Get the sleep start time from Garmin Connect.
    :param date: The date in the format "YYYY-MM-DD".
    :return: The sleep start time as a datetime object.
    """
    garth.resume("./.garth")
    sleep_data = garth.SleepData.get(date)
    sleep_start_time_unix = sleep_data.daily_sleep_dto.sleep_start_timestamp_gmt / 1000
    sleep_start_time = datetime.fromtimestamp(sleep_start_time_unix, TZ)
    return sleep_start_time


def send_to_beeminder(value: str, comment: str) -> None:
    """
    Send the data to Beeminder.
    :param value: The value to send.
    :param comment: The comment to send.
    """
    url = f"https://www.beeminder.com/api/v1/users/{BEEMINDER_USER}/goals/{BEEMINDER_GOAL}/datapoints.json"
    data = {"auth_token": BEEMINDER_TOKEN, "value": value, "comment": comment}
    requests.post(url, data=data)


def main():
    try:
        current_date = datetime.now(tz=TZ).strftime("%Y-%m-%d")
        sleep_start_time = get_sleep_start_time(current_date)
        if sleep_start_time < BEDTIME:
            send_to_beeminder(1, "Early to bed.")
        else:
            send_to_beeminder(0, "Late to bed.")
    except GarthException:
        send_to_beeminder(0, "Error: log in to Garmin Connect.")
    except AttributeError:
        send_to_beeminder(0, "Error: no sleep data found.")


main()
