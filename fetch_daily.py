#!/usr/bin/env python3
"""
Fetches today's LeetCode daily challenge via LeetCode's GraphQL API
and prepends a formatted entry to log.md.
No authentication needed.
"""

import urllib.request
import urllib.error
import json
import datetime
import sys

LEETCODE_GRAPHQL = "https://leetcode.com/graphql"
LOG_FILE = "log.md"
START_MARKER = "<!-- ENTRIES START -->"
END_MARKER   = "<!-- ENTRIES END -->"

GRAPHQL_QUERY = json.dumps({
    "operationName": "questionOfToday",
    "query": """
        query questionOfToday {
            activeDailyCodingChallengeQuestion {
                date
                link
                question {
                    questionFrontendId
                    title
                    titleSlug
                    difficulty
                    acRate
                    topicTags { name }
                }
            }
        }
    """
})

DIFFICULTY_EMOJI = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}

def fetch_daily():
    req = urllib.request.Request(
        LEETCODE_GRAPHQL,
        data=GRAPHQL_QUERY.encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com",
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def build_entry(data):
    today = datetime.date.today().strftime("%Y-%m-%d")
    q = data["data"]["activeDailyCodingChallengeQuestion"]
    problem   = q["question"]
    link      = f"https://leetcode.com{q['link']}"
    num       = problem["questionFrontendId"]
    title     = problem["title"]
    difficulty= problem["difficulty"]
    ac_rate   = round(float(problem.get("acRate", 0)), 1)
    tags      = [t["name"] for t in problem.get("topicTags", [])]

    emoji    = DIFFICULTY_EMOJI.get(difficulty, "⚪")
    tags_str = " ".join(f"`{t}`" for t in tags) if tags else "—"

    return (
        f"## [{today}] #{num} — [{title}]({link})\n\n"
        f"**Difficulty:** {emoji} {difficulty} &nbsp;|&nbsp; "
        f"**Acceptance:** {ac_rate}%  \n"
        f"**Tags:** {tags_str}\n\n"
        f"---\n"
    )

def prepend_entry(entry):
    with open(LOG_FILE, "r") as f:
        content = f.read()

    s = content.find(START_MARKER)
    e = content.find(END_MARKER)
    if s == -1 or e == -1:
        print("Markers not found in log.md", file=sys.stderr)
        sys.exit(1)

    after = s + len(START_MARKER)
    existing = content[after:e]

    today = datetime.date.today().strftime("%Y-%m-%d")
    if f"## [{today}]" in existing:
        print(f"Entry for {today} already exists — skipping.")
        sys.exit(0)

    new_content = (
        content[:after]
        + "\n"
        + entry
        + existing.lstrip("\n")
        + content[e:]
    )

    with open(LOG_FILE, "w") as f:
        f.write(new_content)

    print(f"✅ Logged: {entry.splitlines()[0]}")

if __name__ == "__main__":
    data = fetch_daily()
    entry = build_entry(data)
    prepend_entry(entry)
