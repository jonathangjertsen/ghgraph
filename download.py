import json
from pathlib import Path
from github import Github

from my_secret import PAT, REPO

def main():
    gh = Github(PAT)
    r = gh.get_repo(REPO)
    issues = {"issues": [{
        "number": issue.number,
        "created_at": str(issue.created_at),
        "closed_at": str(issue.closed_at),
        "labels": [label.name for label in issue.labels]
    } for issue in r.get_issues(state="all")]}
    Path("issues.json").write_text(json.dumps(issues))
    print("Wrote to issues.json")

if __name__ == "__main__":
    main()
