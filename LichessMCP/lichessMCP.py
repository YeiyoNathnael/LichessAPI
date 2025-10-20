from typing import *
from mcp.server.fastmcp import FastMCP
from data_parser import *
import berserk


client = berserk.Client()
# Initialize FastMCP server
mcp = FastMCP("lichessMCP")

# redesigned tools using the python version of the api
#user api's
@mcp.tool()

async def get_crosstable(user1,user2):
    crosstable = client.users.get_crosstable(user1=user1, user2=user2)
    return(f"""
    Number of games: {crosstable["nbGames"]}
    User 1: {crosstable["users"].get(user1)} 
    User 2: {crosstable['users'].get(user2)}
          
          """)
@mcp.tool()

async def get_user_performance(username: str,perf:str):
    data= client.users.get_user_performance(username=username, perf=perf)
    performance = parse_user_performance_data(data)
    return(performance)

@mcp.tool()

async def get_leaderboard(perf_type:str, count:int):
    data= client.users.get_leaderboard(perf_type=perf_type, count=count)
    leaderboard = parse_lichess_leaderboard(data)
    return(leaderboard)

@mcp.tool()

async def get_public_data(username: str):
    data= client.users.get_public_data(username=username)
    public_data = parse_user_public_data(data)
    return(public_data)


################################################33
# Team related stuff down here


@mcp.tool()
async def get_team_members(team_id : str):
    data=client.teams.get_members(team_id=team_id)
    members = parse_team_members(data)
    return members

@mcp.tool()
async def get_team_search(team_id : str):
    data=client.teams.search(text=team_id)
    teams = parse_team_search(data)
    return teams

def main():
    # Initialize and run the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()