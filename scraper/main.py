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

tokens = [GITHUB_TOKEN, GITHUB_TOKEN2, GITHUB_TOKEN3]
token_cycle = cycle(tokens)
SLEEP_RATE = 0.8 / len(tokens) # 0.72 3600 seconds / 5000 requests, 0.8 for safe measure
FEATURES = ['login', 'id']

URL = 'https://api.github.com/organizations?per_page=100&since='



def main():
    # appending to existing file
    if os.path.exists('organizations.csv'):
        # retrieve last line id to continue adding orgs
        # https://stackoverflow.com/questions/46258499/how-to-read-the-last-line-of-a-file-in-python

        since = 0
        with open('organizations.csv', 'rb') as f:
            try:
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)

            last_line = f.readline().decode().split(',')
            
            since = int(last_line[1])
        
        
        print(f"Starting from {since}")        
        with open('organizations.csv', 'a') as f:
            writer = csv.DictWriter(f, fieldnames=FEATURES)

            while True:
                url = URL + str(since)

                headers = {
                    'Authorization': f'token {next(token_cycle)}'
                }

                r = requests.get(url, headers=headers)
                data = r.json()

                # print(data[0]['login'], data[0]['id'])
                for org in data:
                    writer.writerow({
                        'login': org['login'],
                        'id': org['id'],
                    })
                
                since = data[-1]['id']
                sleep(SLEEP_RATE)

    # creating a new file
    else:    
        with open('organizations.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FEATURES)
            writer.writeheader()

            since = 0
            while True:        
                url = URL + str(since)      

                headers = {
                    'Authorization': f'token {next(token_cycle)}'
                }

                r = requests.get(url, headers=headers)
                data = r.json()

                # print(data[0]['login'], data[0]['id'])
                for org in data:
                    writer.writerow({
                        'login': org['login'],
                        'id': org['id'],
                    })            
                
                since = data[-1]['id']
                sleep(SLEEP_RATE)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(e)