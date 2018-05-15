# python 3.x
# encoding utf-8

import re
import sys
import base64
import argparse
from github import Github
from configobj import ConfigObj


def argManager():

    parser = argparse.ArgumentParser(sys.argv[0])
    parser.add_argument("search", help="Keyword for the search (eg. shodan)", type=str)

    params = parser.parse_args()

    return params


def checkForAPIKey(text):
    regex = re.compile("\w{32}")
    result = regex.search(text)

    if result is not None:
        print(result.group())


def main():

    config = ConfigObj('config.cf')
    params = argManager()

    g = Github(config['github_creds']['username'],
               config['github_creds']['password'])

    results = g.search_code(query=params.search + ' api key')

    for result in results:
        # print(g.get_rate_limit().rate)
        # print(g.rate_limiting_resettime)
        # print("FILENAME : " + result.path)
        # print(base64.b64decode(result.content), end='\n\n')
        # print("Checking " + result.path)
        checkForAPIKey(str(base64.b64decode(result.content)))


if __name__ == "__main__":
    main()
