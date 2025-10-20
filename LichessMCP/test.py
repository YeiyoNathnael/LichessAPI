import berserk
from data_parser import *
from typing import *




client = berserk.Client()

top10 = client.users.get_all_top_10()
crosstable = client.users.get_crosstable(user1="delight2024", user2="listock")

#List[Dict[str]]
print(crosstable["users"])
#test to see if the python api actually works, and generally to see some values to use later


fide_players = client.fide.search_players(name="Nate")
for item in fide_players:
    player = parse_fide_player(item)
    print(player)