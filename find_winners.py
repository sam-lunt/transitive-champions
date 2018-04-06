#!/usr/bin/env python
from __future__ import absolute_import, division, print_function
import sys
import re
import collections


def main():
    if len(sys.argv) < 2 or sys.argv[1] == "-":
        games = parse_games(sys.stdin)
    else:
        with open(sys.argv[1]) as file:
            games = parse_games(file)

    defeated = collections.defaultdict(set)
    defeated_by = collections.defaultdict(set)

    teams = set()
    for winner, loser in games:
        defeated[winner].add(loser)
        defeated_by[loser].add(winner)

        teams.add(winner)
        teams.add(loser)

    champions = { "Villanova": 0 }
    new_champions = list(champions.keys())
    degree_of_seperation = 0

    while len(new_champions) > 0:
        degree_of_seperation += 1
        additions = []
        for champion in new_champions:
            for winner in defeated_by[champion]:
                if winner not in champions:
                    champions[winner] = degree_of_seperation
                    additions.append(winner)
        new_champions = additions

    not_champions = teams - set(champions.keys())
    print("There were {} transitive champions and {} not champions".format(len(champions) - 1, len(not_champions)))

    if len(sys.argv) >= 3:
        with open(sys.argv[2], "w") as file:
            for champion, degree in sorted(champions.items(), key=lambda t: t[1]):
                print(champion, degree, sep="\t", file=file)
            for not_champion in not_champions:
                print(not_champion, "-1", sep="\t", file=file)


def parse_games(file):
    pattern = re.compile(
        r"(?P<date>\d{4}-\d{2}-\d{2})\s+"
        r"@?(?P<winner>.*?)\s+"
        r"(?P<winning_score>\d+)\s+"
        r"@?(?P<loser>.*?)\s+"
        r"(?P<losing_score>\d+)"
    )

    results = []
    for line in file:
        match = pattern.match(line)
        assert match is not None
        assert int(match.group("winning_score")) > int(match.group("losing_score"))
        results.append((match.group("winner"), match.group("loser")))

    return results


if __name__ == "__main__":
    main()
