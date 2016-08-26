import requests
import datetime
from datetime import timedelta
import sys
import time
import smtplib
import accountData
from email.MIMEText import MIMEText

class Area:
    def __init__(self, max_latitude, min_latitude, max_longitude, min_longitude):
        self.min_lat = min_latitude
        self.max_lat = max_latitude
        self.min_long = min_longitude
        self.max_long = max_longitude

class User:
    def __init__(self, area, email, active, table):
        self.area = area
        self.email = email
        self.active = active
        self.table = table