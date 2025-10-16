
from datetime import datetime
from typing import Any  
import httpx

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
    profile = data.get('profile', {})
    streamer = data.get('streamer', {})
    playtime = data.get('playTime', {})

    ratings = []
    for perf_type, perf_data in perfs.items():
        rating = perf_data.get('rating', 'N/A')
        games = perf_data.get('games', 0)
        ratings.append(f"{perf_type.capitalize()}: {rating} ({games} games)")


    counts = []
    for count_type, count_value in count.items():
        count_name = count_type.capitalize().title()
        counts.append(f"{count_name}: {count_value}")

    streaming = data.get('streaming', False)
    twitch = streamer.get('twitch', {})
    youtube = streamer.get('youtube', {})

    total_playtime = playtime.get('total', 0)
    total_tv = playtime.get('tv', 0)

    createdAt = datetime.fromtimestamp(data.get('createdAt')/1000).strftime('%Y-%m-%d')
    lastSeen = datetime.fromtimestamp(data.get('seenAt')/1000).strftime('%Y-%m-%d %H:%M:%S')
    tosViolation = data.get('tosViolation', False)
    verified = data.get('verified', False)
    title = data.get('title', '')
    
    return f"""
            Username: {data.get('username', 'Unknown')}
            Profile: {data.get('url', 'N/A')}
            title: {title if title else 'No title'}
            Bio: {profile.get('bio', 'No bio')}
            Country: {profile.get('flag', 'Unknown')}
            Twitch: {twitch.get('channel', 'N/A')}
            YouTube: {youtube.get('channel', 'N/A')}

            {'Account is banned for TOS violation' if tosViolation else ''}
            {'Account is verified' if verified else ''}
            {'User is streaming' if streaming else ''}

            {f"Account created on {createdAt}"}
            Last Online: {lastSeen} 

            {f"User is currently playing, Watch their game at {data.get('playing','N/A')}" if data.get('playing') else 'Not currently playing'}
            Ratings:
            {ratings if ratings else 'No ratings available'}

            Stats:
            {counts if counts else 'No stats available'}
            Playtime: {total_playtime // 3600} hours total, {total_tv // 3600} hours on TV
"""   

def format_crosstable_info(data: dict, user1 : str,user2:str) -> str:
    """Format Lichess crosstable data into readable string."""
  
    users = data.get('users', {})
    score1, score2 = users.get(user1,0), users.get(user2,0) 
    draws = total_games - score1 - score2
    
    total_games = data.get('nbGames', 0)
    
    return f"""
            Crosstable between {user1} and {user2}:
            Total Games: {total_games}
            {user1}: {score1} points
            {user2}: {score2} points
            Draws: {draws} games
"""