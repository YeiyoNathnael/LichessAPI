import berserk

from data_parser import *
client = berserk.Client()

top10 = client.users.get_all_top_10()
crosstable = client.users.get_crosstable(user1="delight2024", user2="listock")

#List[Dict[str]]
print(crosstable["users"])
#test to see if the python api actually works, and generally to see some values to use later


members = parse_team_members( client.teams.get_members(team_id="ethchess"))

members =client.teams.search(text="ethchess")
print(members)