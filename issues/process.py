import json
import os
import sys
from datetime import datetime


def load_issues(filename):
    if not os.path.exists(filename):
        raise Exception("file f{filename} not found")
    with open(filename, "r") as f:
        return json.load(f)


def calculate_lead_time(issue):
    start_time = get_start_time(issue)
    if start_time is None:
        return None
    close_time = get_close_time(issue)
    if close_time is None:
        return None
    return (close_time - start_time).total_seconds()


def label_filter(issue):
    if len(sys.argv) >= 2:
        return all(label in map(lambda label: label["name"], issue["labels"]) for label in sys.argv[1:])
    return True


def get_start_time(issue):
    for event in issue["zenhub"]:
        if event["type"] == "transferIssue" and event["to_pipeline"]["name"] == "In Progress":
            return datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")


def get_close_time(issue):
    return datetime.strptime(issue["github"]["closed_at"], "%Y-%m-%dT%H:%M:%SZ")
