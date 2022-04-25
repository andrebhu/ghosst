#!/usr/bin/env python3

import os
import csv
import json
import timeit
import requests

from time import sleep
from itertools import cycle
from datetime import datetime
from dotenv import dotenv_values
from multiprocessing.pool import ThreadPool as Pool


# only store Github tokens in .env
secrets = dotenv_values()
tokens = list(secrets.values())
token_cycle = cycle(tokens)


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


def worker(reader, writer, outfile):

    while True:
        urlname = next(reader)[0]

        # initial request to check if org actually exists
        with requests.get(f"https://github.com/{urlname}") as r:
            if r.status_code == 404: continue
        
        headers = {
            "Authorization": f"token {next(token_cycle)}"
        }


        data = requests.get(f"https://api.github.com/orgs/{urlname}", headers=headers).json()

        if not data['is_verified']: continue
    
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

        print(f"[{datetime.now()}] {data['login']} {data['id']}", "{:.5f}%".format(data['id'] / 104219624 * 100))

        # outfile.sync()
        outfile.flush() # save file
        
        

        




def main():

    # create reader
    infile = open("organizations-4-22-2022.csv", "r")
    reader = csv.reader(infile)
    next(reader) # skip headers

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
    

    # Skip reader to last saved organization
    row = next(reader)
    while int(row[1]) < last_id:
        row = next(reader)
    
    # Creating writer
    outfile = open("verified_organizations.csv", "a")
    writer = csv.DictWriter(outfile, fieldnames=FEATURES)

    print(f"[{datetime.now()}] Last entry {row}")

    # creating workers
    p = Pool(5)
    for i in range(5):
        p.apply_async(worker, (reader, writer, outfile))

    p.close()
    p.join()
    print("Finishing...")



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print("EXCEPTION:", e)
        sleep(600)
        print("Restarting...")
        main()