import json
import os
import sys
from datetime import datetime
from enum import Enum

class StartTimeSource(Enum):
    IN_PROGRESS = 0
    CREATED_AT = 1

def load_issues(filename):
    if not os.path.exists(filename):
        raise Exception("file f{filename} not found")
    with open(filename, "r") as f:
        return json.load(f)


def calculate_lead_time(issue):
    start_time = get_start_time(issue)
    close_time = get_close_time(issue)
    if close_time is None:
        print(f'skipping {issue["github"]["number"]} ({issue["github"]["title"]}): missing close data')
        return None
    return ((close_time - start_time[0]).total_seconds(), start_time[1])


def get_start_time(issue):
    for event in issue["zenhub"]:
        if event["type"] == "transferIssue" and event["to_pipeline"]["name"] == "In Progress":
            return (datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"), StartTimeSource.IN_PROGRESS)
    return (datetime.strptime(issue["github"]["created_at"], "%Y-%m-%dT%H:%M:%SZ"), StartTimeSource.CREATED_AT)


def get_close_time(issue):
    return datetime.strptime(issue["github"]["closed_at"], "%Y-%m-%dT%H:%M:%SZ")


def has_labels(issue, labels):
    return all(label in map(lambda l: l["name"], issue["github"]["labels"]) for label in labels)
