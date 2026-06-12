# 📓 dev-log

Daily LeetCode problem tracker — auto-logged every morning via GitHub Actions.

Each entry includes the problem title, difficulty, tags, and a direct link. I use this to stay consistent with DSA practice while job hunting.

## Structure

- `log.md` — running log of daily problems (newest at top)
- `.github/workflows/daily.yml` — the automation

## How it works

A GitHub Actions workflow runs every day at 7 AM UTC. It hits the LeetCode daily challenge API, parses the response, and prepends a new entry to `log.md` with a commit.

> Built by [Anshit Singh Rajput](https://anshitsingh.com)
