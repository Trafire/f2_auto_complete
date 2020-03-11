import datetime
import heapq

import pyautogui
from sqlalchemy.exc import OperationalError

import closef2
import login, reports
from auth.passwords import f2_password
from database import get_data, update_data, insert_data
from parse import dates
from stock import SHIPMENT_LOCATIONS, SELLING_LOCATIONS, price_stock_location


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]


def min_sec_to_sec(t):
    return t[0] * 60 + t[1]


def get_job_time(job, reference, timer):
    time_since = get_data.get_time_since_report(system, job, reference)
    if time_since:
        time_since = difference_in_seconds(time_since, datetime.datetime.now(datetime.timezone.utc))
    else:
        time_since = (999999, 999999)
    return min_sec_to_sec(time_since) - min_sec_to_sec(timer)


def tasks():
    to_do = PriorityQueue()

    # price location
    for location in SHIPMENT_LOCATIONS:
        timer = (8, 0)
        job = 'price_location'
        seconds = get_job_time(job, location, timer)
        to_do.push({"job": job, 'reference': location, }, seconds)

    for location in SELLING_LOCATIONS:
        timer = (60, 0)
        job = 'price_location'
        seconds = get_job_time(job, location, timer)
        to_do.push({"job": job, 'reference': location, }, seconds)

    # reports
    job = 'openorders'
    year, week = dates.get_current_week()
    for i in range(12):
        r_year = year + (week + i) // 53
        r_week = (week + i) % 54
        timer = (15 * (2 ** i), 0)
        reference = f'{year},{week}'
        seconds = get_job_time(job, reference, timer)
        print(seconds)
        to_do.push({"job": job, 'reference': reference, }, seconds)


    return to_do


def difference_in_seconds(first_time, later_time):
    difference = later_time - first_time
    seconds_in_day = 24 * 60 * 60
    return divmod(difference.days * seconds_in_day + difference.seconds, 60)


def close_everything():
    closef2.close()
    closef2.close()
    closef2.close()


def do_job(system, job):
    if job['job'] == 'price_location':
        price_stock_location(job['reference'])
    elif job['job'] == 'openorders':
        year, week = job['reference'].split(',')
        year = int(year)
        week = int(week)

        reports.update_week(system, year, week)
    else:
        return False
    if get_data.get_time_since_report(system, job['job'], job['reference']):
        update_data.update_last_done(system, job['job'], job['reference'])
    else:
        insert_data.insert_last_done(system, job['job'], job['reference'])
    return True


def system_loop(system, username, password, logged_in):
    if not logged_in:
        close_everything()
        if login.sign_in_toronto(username, password, system, attempts=0):
            logged_in = True
    else:
        get_data.check_priced_lots_bulk("12345", "test")
        jobs = tasks()

        while True:
            next_job = jobs.pop()
            if do_job(system,next_job):
                break
            else:
                print(next_job, 'job failed')
                exit()

    return logged_in


if __name__ == '__main__':
    logged_in = False
    username = f2_password['username']
    password = f2_password['password']
    system = 'f2_canada_real'
    last_good = datetime.datetime.now()

    while True:
        last_success = difference_in_seconds(last_good, datetime.datetime.now())
        try:
            logged_in = system_loop(system, username, password, logged_in)
            last_good = datetime.datetime.now()
        except pyautogui.FailSafeException:
            print("Corner exit Detected")
            exit()
        except(OperationalError):
            print(f"Waiting For Database connection for {last_success[0]} min {last_success[1]} seconds")
            if last_success[0] > 2:
                print('Restart')
