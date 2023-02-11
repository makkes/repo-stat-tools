import json
import os
import sys
import time
from datetime import datetime

import requests


def get_zh_issue(repoId, issueId, token):
    response = requests.get(
        f"https://api.zenhub.com/p1/repositories/{repoId}/issues/{issueId}/events",
        headers={"X-Authentication-Token": token}
    )
    if response.status_code != 200:
        err = response.json()
        if response.status_code != 403:
            raise Exception(
                f"Failed to fetch issue events from ZenHub (HTTP status code {response.status_code}): {err}")
        rl_used = int(response.headers["X-RateLimit-Used"])
        rl_limit = int(response.headers["X-RateLimit-Limit"])
        if rl_used >= rl_limit:
            rl_reset = datetime.fromtimestamp(
                int(response.headers["X-RateLimit-Reset"]))
            print(f"waiting for API rate limit to reset at {rl_reset}")
            # account for 10 seconds of skew
            time.sleep((rl_reset - datetime.now()).total_seconds() + 10)
            return get_zh_issue(repoId, issueId, token)

    return response.json()


def get_repo_id(repo, gh_token):
    response = requests.get(
        f"https://api.github.com/repos/{repo}",
        headers={"Authorization": f"Token {gh_token}"}
    )
    if response.status_code != 200:
        raise Exception("Failed to fetch repo details")
    data = response.json()
    if not data:
        raise Exception("No data in response")
    return data["id"]


def fetch_issues(repo, state, gh_token, zh_token):
    filename = f"{repo.replace('/', '_')}_{state}_issues.json"
    issues = []
    page = 1
    repo_id = get_repo_id(repo, gh_token)

    # while page == 1:
    while True:
        response = requests.get(
            f"https://api.github.com/repos/{repo}/issues?state={state}&page={page}",
            headers={"Authorization": f"Token {gh_token}"}
        )
        if response.status_code != 200:
            raise Exception("Failed to fetch issues")
        data = response.json()
        if not data:
            break
        for issue in data:
            if "pull_request" in issue:
                continue
            issues.append(
                {"github": issue, "zenhub": get_zh_issue(repo_id, issue["number"], zh_token)},)
            if len(issues) % 20 == 0:
                print(f"processed {len(issues)} issues")
        page += 1

    with open(filename, "w") as f:
        json.dump(issues, f)
