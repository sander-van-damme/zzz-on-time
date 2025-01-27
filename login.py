#!/usr/bin/env python3

import garth
from getpass import getpass


def garmin_login():
    """
    Log in to Garmin.
    """
    email = input("Enter Garmin e-mail address: ")
    password = getpass("Enter Garmin password: ")
    garth.login(email, password)
    garth.save("./.garth")


garmin_login()
