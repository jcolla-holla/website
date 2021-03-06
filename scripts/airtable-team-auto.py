#! /usr/bin/env python3

from airtable import Airtable
import json
import os


VIEW_NAME = "^^dont_change_team_name"
TABLE_NAME = "team"
OUTPUT_PATH = "../assets/data/teamlist.json"

def valid_entry(entry):
    for value in ["name", "team"]:
        if value not in entry:
            return False

    return True


def main():
    try:
        # these keys have been set up Github /websites repo secrets already
        airtable = Airtable(
            os.environ["AIRTABLE_TEAM_BASE_KEY"],
            TABLE_NAME,
            api_key=os.environ["AIRTABLE_API_KEY"],
        )
    except KeyError:
        print("Couldn't find airtable base key or api key")
        exit(1)

    team_list = {}

    for page in airtable.get_iter(view=VIEW_NAME):
        for record in page:
            new_values = record["fields"]


            print(new_values)
            # print(new_values.get("team"))
            if valid_entry(new_values):
                if team_list.get(new_values.get("team")) is not None:
                    team_list[new_values.get("team")].append(new_values.get("name"))
                else:
                    team_list[new_values.get("team")] = []


    with open(OUTPUT_PATH, "w") as f:
        json.dump(team_list, f, indent=2, sort_keys=True)


if __name__ == "__main__":
    main()
