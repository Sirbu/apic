# python 3.x
# encoding utf-8

import re
import sys
import math
import base64
import argparse
from github import Github, GithubException
from configobj import ConfigObj


api_entropy_limit = {
    "github": 4,
    "pastebin": 3.2
}

bad_words = ['api', 'key', 'format', 'pastebin', 'github', 'shodan', 'test',
             'developer']


# Calculates entropy of a string
def entropy(data):
    if not data:
        return 0
    entropy = 0
    for x in range(256):
        p_x = float(data.count(chr(x)))/len(data)
        if p_x > 0:
            entropy += - p_x*math.log(p_x, 2)
    return entropy


def argManager():

    parser = argparse.ArgumentParser(sys.argv[0])
    parser.add_argument("search", help="Keyword for the search (eg. shodan)", type=str)

    params = parser.parse_args()

    return params


def checkForAPIKey(text):
    regex = re.compile("\w{32}")
    result = regex.search(text)

    if result is not None:
        print(result.group(), end=' ')
        print('entropy : ', entropy(result.group()))


def main():

    config = ConfigObj('config.cf')
    params = argManager()

    try:
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

    except GithubException:
        print('[!] Incorrect Github credentials : check conf.cnf file')

if __name__ == "__main__":
    main()
