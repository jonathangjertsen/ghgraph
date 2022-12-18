from pathlib import Path
import json
from datetime import datetime
from matplotlib import pyplot as plt
import matplotlib

from my_secret import REPO

def set_style():
    matplotlib.style.use("seaborn")

def load_issues():
    return [{
        "number": issue["number"],
        "created_at": datetime.strptime(issue["created_at"], "%Y-%m-%d %H:%M:%S"),
        "closed_at": datetime.strptime(issue["closed_at"], "%Y-%m-%d %H:%M:%S") if issue["closed_at"] != "None" else None,
        "labels": issue["labels"]
    } for issue in json.loads(Path("issues.json").read_text())["issues"]]

def convert_to_events(issues):
    events = []
    for issue in issues:
        events.append({ "e": "opened", "t": issue["created_at"], "i": issue })
        if issue["closed_at"] is not None:
            events.append({ "e": "closed", "t": issue["closed_at"], "i": issue })
    return sorted(events, key=lambda event: event["t"])

def same(vectors, v):
    vectors[v].append(vectors[v][-1])

def inc(vectors, v):
    vectors[v].append(vectors[v][-1] + 1)

def dec(vectors, v):
    vectors[v].append(vectors[v][-1] - 1)

def accumulate(events):
    ts = [events[0]["t"]]
    vectors = {
        "open": [0],
        "open_with_bug": [0],
        "closed": [0],
        "closed_with_bug": [0],
        "created": [0],
        "created_with_bug": [0]
    }
    for event in events:
        ts.append(event["t"])
        if event["e"] == "opened":
            inc(vectors, "open")
            inc(vectors, "created")
            if "bug" in event["i"]["labels"]:
                inc(vectors, "open_with_bug")
                inc(vectors, "created_with_bug")
            else:
                same(vectors, "open_with_bug")
                same(vectors, "created_with_bug")
            same(vectors, "closed")
            same(vectors, "closed_with_bug")
        if event["e"] == "closed":
            dec(vectors, "open")
            same(vectors, "created")
            same(vectors, "created_with_bug")
            if "bug" in event["i"]["labels"]:
                dec(vectors, "open_with_bug")
                dec(vectors, "closed_with_bug")
            else:
                same(vectors, "open_with_bug")
                same(vectors, "closed_with_bug")
            dec(vectors, "closed")
        assert all(len(vectors[v]) == len(vectors["open"]) for v in vectors)
    return ts, vectors

def plot(ts, vectors):
    plt.plot(ts, vectors["open"], color="green")
    plt.fill_between(ts, vectors["open_with_bug"], color="black", alpha=1)
    plt.plot(ts, vectors["closed"], color="purple")
    plt.fill_between(ts, vectors["closed_with_bug"], color="black", alpha=1)
    plt.fill_between(ts, vectors["open"], color="green", alpha=0.7)
    plt.fill_between(ts, vectors["closed"], color="purple", alpha=0.7)
    plt.legend(["open issues", "issues with tag 'bug'", "closed issues"])
    plt.title(f"Issues in {REPO}")
    plt.show()

def main():
    set_style()
    issues = load_issues()
    events = convert_to_events(issues)
    ts, vectors = accumulate(events)
    plot(ts, vectors)


if __name__ == "__main__":
    main()
