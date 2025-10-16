from typing import Any

from mcp.server.fastmcp import FastMCP
from datetime import datetime
from requestLichess import *
from utilities.users import format_user_info


# Initialize FastMCP server
mcp = FastMCP("lichessMCP")


@mcp.tool()

async def get_user_info(username: str) -> str:
    """Get public information for a Lichess user."""
    userinfo = await get_lichess_user_public_data(username)
    return (userinfo)
@mcp.tool()

async def get_crosstable_comparison(user1:str , user2:str) -> str:
    """Get public information for a Lichess user."""
    crosstable = await get_lichess_users_crosstable(user1, user2)
    return (crosstable)





def main():
    # Initialize and run the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()