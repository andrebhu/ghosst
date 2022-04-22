#!/usr/bin/env python3

import os
import csv
import json
import requests

from time import sleep
from itertools import cycle
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_TOKEN2 = os.getenv('GITHUB_TOKEN2')
GITHUB_TOKEN3 = os.getenv('GITHUB_TOKEN3')
GITHUB_TOKEN4 = os.getenv('GITHUB_TOKEN4')

tokens = [GITHUB_TOKEN, GITHUB_TOKEN2, GITHUB_TOKEN3, GITHUB_TOKEN4]
token_cycle = cycle(tokens)
SLEEP_RATE = 0.8 / len(tokens) # 0.72 3600 seconds / 5000 requests, 0.8 for safe measure


def checkOrg(orgname):
    pass    




def main():
    with open("organizations-4-22-2022.csv", "r") as infile:
        reader = csv.reader(infile)
        # skip headers 
        next(reader)

        print(next(reader)[0])

        with open("verified_organizations.csv", "w") as outfile:
            pass




if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(e)