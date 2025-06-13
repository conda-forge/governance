# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "requests",
# ]
# ///

import csv
import os
from pathlib import Path
from collections.abc import Iterable
from difflib import unified_diff

import requests

ROOT = Path(__file__).parent.parent
TEAMS = ROOT / "teams"

ORG = "conda-forge"
TEAM_NAME_OVERRIDES = {
    # CSV Name -> Github Name
    "emeritus": "emeritus-core",
}
GH_TOKEN = os.environ.get("GITHUB_TOKEN")


def _team_csv_files() -> dict[str, Path]:
    return {path.stem: path for path in sorted(TEAMS.glob("*.csv"))}


def _usernames_from_csv(path: Path) -> Iterable[str]:
    with path.open() as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            yield row[0].lower()  # username


def teams_in_repo() -> dict[str, list[str]]:
    teams = {}
    for team_name, path in _team_csv_files().items():
        for username in _usernames_from_csv(path):
            teams.setdefault(team_name, []).append(username)
    return teams


def _gh_team_members(team_name: str) -> list[str]:
    r = requests.get(
        f"https://api.github.com/orgs/{ORG}/teams/{team_name}/members",
        params={"per_page": 100},
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {GH_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    r.raise_for_status()
    return [user["login"].lower() for user in r.json()]


def check_github_team(team_name: str, usernames: Iterable[str]) -> None:
    gh_usernames = _gh_team_members(team_name)
    sorted_usernames = sorted(usernames)
    sorted_gh_usernames = sorted(gh_usernames)
    if sorted_usernames != sorted_gh_usernames:
        diff = unified_diff(
            [f"{x}\n" for x in sorted_usernames],
            [f"{x}\n" for x in sorted_gh_usernames],
            "csv",
            "github",
        )
        raise ValueError(f"Team {team_name} is not up-to-date!\n" f"{''.join(diff)}")


def check_teams() -> int:
    exceptions = []
    for csv_team_name, usernames in teams_in_repo().items():
        gh_team_name = TEAM_NAME_OVERRIDES.get(csv_team_name, csv_team_name)
        try:
            check_github_team(gh_team_name, usernames)
        except Exception as exc:
            exceptions.append(exc)
    if exceptions:
        for exception in exceptions:
            print(f"{exception.__class__.__name__}:", exception)
        return 1
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(check_teams())
