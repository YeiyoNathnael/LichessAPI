from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("lichessMCP")

# Constants
LICHESS_API_BASE = "https://lichess.org"
USER_AGENT = "lichessMCP/1.0"


async def make_lichess_request(url: str) -> dict[str, Any] | None:
    """Make a request to the Lichess API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
def format_user_info(data: dict) -> str:
    """Format Lichess user data into readable string."""
    
    perfs = data.get('perfs', {}) #Just for readability later on
    count = data.get('count', {})

    blitz = perfs.get('blitz', {})
    bullet = perfs.get('bullet', {})
    rapid = perfs.get('rapid', {})
    
    return f"""
Username: {data.get('username', 'Unknown')}
Country: {data.get('profile', {}).get('flag', 'Unknown')}
Bio: {data.get('profile', {}).get('bio', 'No bio')}

Ratings:
  Bullet: {bullet.get('rating', 'N/A')} ({bullet.get('games', 0)} games)
  Blitz: {blitz.get('rating', 'N/A')} ({blitz.get('games', 0)} games)
  Rapid: {rapid.get('rating', 'N/A')} ({rapid.get('games', 0)} games)

Stats:
  Total Games: {count.get('all', 0)}
  Wins: {count.get('win', 0)}
  Losses: {count.get('loss', 0)}
  Draws: {count.get('draw', 0)}

Profile: {data.get('url', 'N/A')}
"""    
        
@mcp.tool()

async def lichess_user(username: str) -> str:
   url = f"{LICHESS_API_BASE}/api/user/{username}"
   data = await make_lichess_request(url)

#    if not data:
#         return "Unable to fetch data for the user."

#    if not "username" in data:
#         return "No user by this name."

   userinfo = format_user_info(data)
   return "\n---\n".join(userinfo)


def main():
    # Initialize and run the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()