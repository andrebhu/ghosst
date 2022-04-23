#!/usr/bin/env python3

import os
import csv
import json
import requests

from time import sleep
from itertools import cycle
from datetime import datetime

# from dotenv import load_dotenv
from dotenv import dotenv_values

# only store Github tokens in .env
secrets = dotenv_values()
tokens = list(secrets.values())

token_cycle = cycle(tokens)
SLEEP_RATE = 0.8 / len(tokens) # 0.72 3600 seconds / 5000 requests, 0.8 for safe measure

FEATURES = [
    "login",
    "id",
    "name",
    "company",
    "blog",
    "email",
    "twitter_username",
    "is_verified",
    "has_organization_projects",
    "has_repository_projects",
    "public_repos",
    "public_gists",
    "html_url",
    "created_at",
    "updated_at",
    "type",
]

def checkOrg(orgname):    
    # If not found on normal GitHub, save an API call and return
    r = requests.get(f"https://github.com/{orgname}")
    if int(r.status_code) == 404:
        return

    headers = {
        'Authorization': f'token {next(token_cycle)}'
    }
    data = requests.get(f"https://api.github.com/orgs/{orgname}", headers=headers).json()

    if data['is_verified']:
        print(f"[{datetime.now()}] {data['login']} {data['id']}", "{:.5f}%".format(data['id'] / 104219624 * 100))
        return data


def main():

    with open("organizations-4-22-2022.csv", "r") as infile:
        reader = csv.reader(infile)
        # skip headers 
        next(reader)

        # If file already exists
        if os.path.exists('verified_organizations.csv'):
            # Find last org id
            last_id = 0
            with open('verified_organizations.csv', 'rb') as f:
                try:
                    f.seek(-2, os.SEEK_END)
                    while f.read(1) != b'\n':
                        f.seek(-2, os.SEEK_CUR)
                except OSError:
                    f.seek(0)

                last_line = f.readline().decode().split(',')
            
                last_id = int(last_line[1])

            # Skip rows until org id
            row = next(reader)
            while int(row[1]) < last_id:
                row = next(reader)

            print(f"[{datetime.now()}] Last entry {row}")
            
            # Appending to already existing file
            with open("verified_organizations.csv", "a") as outfile:
                writer = csv.DictWriter(outfile, fieldnames=FEATURES)

                while True:
                    name = next(reader)[0]
                    data = checkOrg(name)

                    if data:
                        writer.writerow({
                            "login": data['login'],
                            "id": data['id'],
                            "name": data['name'],
                            "company": data['company'],
                            "blog": data['blog'],
                            "email": data['email'],
                            "twitter_username": data['twitter_username'],
                            "is_verified": data['is_verified'],
                            "has_organization_projects": data['has_organization_projects'],
                            "has_repository_projects": data['has_repository_projects'],
                            "public_repos": data['public_repos'],
                            "public_gists": data['public_gists'],
                            "html_url": data['html_url'],
                            "created_at": data['created_at'],
                            "updated_at": data['updated_at'],
                            "type": data['type'],
                        })

                    sleep(SLEEP_RATE)

        else:
            with open("verified_organizations.csv", "w") as outfile:
                writer = csv.DictWriter(outfile, fieldnames=FEATURES)
                writer.writeheader()

                while True:
                    name = next(reader)[0]
                    data = checkOrg(name)

                    if data:
                        writer.writerow({
                            "login": data['login'],
                            "id": data['id'],
                            "name": data['name'],
                            "company": data['company'],
                            "blog": data['blog'],
                            "email": data['email'],
                            "twitter_username": data['twitter_username'],
                            "is_verified": data['is_verified'],
                            "has_organization_projects": data['has_organization_projects'],
                            "has_repository_projects": data['has_repository_projects'],
                            "public_repos": data['public_repos'],
                            "public_gists": data['public_gists'],
                            "html_url": data['html_url'],
                            "created_at": data['created_at'],
                            "updated_at": data['updated_at'],
                            "type": data['type'],
                        })
                    sleep(SLEEP_RATE)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(e)