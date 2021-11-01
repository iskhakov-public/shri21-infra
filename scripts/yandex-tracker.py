import requests
import os
import sys
import json
from requests.models import HTTPError
from requests.structures import CaseInsensitiveDict
import subprocess
from argparse import ArgumentParser

#--------------------------------------------------------------------------------
#------------------------------GIT Invoke Helpers--------------------------------

def run(args):
    res = subprocess.run(args.split(" "), stdout=subprocess.PIPE, encoding="utf-8")
    res.stdout = res.stdout.strip()
    return res

def getLastTag():
    out = run("git rev-list --tags --max-count=1")
    res = run(f'git describe --abbrev=0 --tags {out.stdout}')
    return res.stdout

def getLastHashCommit(tagVer):
    out = run(f'git rev-list -n 1 {tagVer}')
    return out.stdout[:7]

def getAuthor(tagVer):
    out = run(f'git rev-list -n 1 {tagVer} --pretty=format:\'%an\'')
    return out.stdout.splitlines().pop()


#--------------------------------------------------------------------------------
#------------------------------Data Preparation----------------------------------

tagVer = getLastTag()
hashCommit = getLastHashCommit(tagVer)
author = getAuthor(tagVer)

version = f'{tagVer}-0-{hashCommit}'

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"
headers["Authorization"] = f'OAuth {os.environ.get("YANDEX_OAUTH")}'
headers["OrgId"] = os.environ.get("YANDEX_ORGID")

#--------------------------------------------------------------------------------
#------------------------------API Requests--------------------------------------

def yt_create_ticket(description):
    url = "https://api.tracker.yandex.net/v2/issues/"

    data = {
        "summary": f'test-release: todoapp deploy {version}',
        "queue": "TMP",
        "description": f'{description} \n\nBy {author}',
        # "assignee": "iskhakov-nu"
    }

    # print(json.dumps(data))

    try:
        resp = requests.post(url, headers=headers, data=json.dumps(data))
        resp.raise_for_status()
    except HTTPError as e:
        print("> create-ticket: HTTPError - {}".format(e.strerror))
        sys.exit(1)

    respObj = resp.json()
    # print(respObj)

    key = respObj["key"]
    # print(key)
    
    print("{} {}".format(resp.status_code, key))



def yt_create_comment(text, issueid):

    url = f'https://api.tracker.yandex.net/v2/issues/{issueid}/comments'

    data = {
        "text": text
    }

    print(data)
    try:
        resp = requests.post(url, headers=headers, data=json.dumps(data))
        # print(resp.json())
        resp.raise_for_status()
    except HTTPError as e:
        print("> create-comment: HTTPError - {}".format(e.strerror))
        sys.exit(1)

    return resp.status_code

#--------------------------------------------------------------------------------
#------------------------------CLI Processing------------------------------------
cli = ArgumentParser()
subparsers = cli.add_subparsers(dest="subcommand")

def subcommand(args=[], parent=subparsers):
    def decorator(func):
        parser = parent.add_parser(func.__name__, description=func.__doc__)
        for arg in args:
            parser.add_argument(*arg[0], **arg[1])
        parser.set_defaults(func=func)
    return decorator

def argument(*name_or_flags, **kwargs):
    return ([*name_or_flags], kwargs)

@subcommand([argument("-t", "--text", help="Text to create ticket with"), argument("-i", "--issue", help="Key or ID of the ticket")])
def create_comment(args):
    textFile = args.text
    issueFile = args.issue

    text = ""
    issue = ""

    try:
        with open(textFile, encoding="utf-8") as f:
            text = f.read()

    except IOError as e:
        print("> create-comment: IOError - {} -> {}".format(textFile, e.strerror), file=sys.stderr)
        sys.exit(1)

    try:
        with open(issueFile, encoding="utf-8") as f:
            issue = f.read()
    except IOError as e:
        print("> create-comment: IOError - {} -> {}".format(issueFile, e.strerror), file=sys.stderr)
        sys.exit(1)
    
    yt_create_comment(text, issue)

@subcommand([argument("-d", "--description", help="Description to create ticket with")])
def create_ticket(args):
    descFile = args.description

    try:
        with open(descFile, encoding="utf-8") as f:
            yt_create_ticket(f.read())

    except IOError as e:
        print("> create-ticket: IOError - {}".format(e.strerror), file=sys.stderr)
        sys.exit(1)


# python scripts/yandex-tracker.py create_comment -t ./logs/tests.log -i ./logs/issueid.log
# python scripts/yandex-tracker.py create_ticket -d ./logs/changelog.txt

if __name__ == "__main__":
    args = cli.parse_args()
    if args.subcommand is None:
        cli.print_help()
    else:
        args.func(args)