from utilities.users import *
from typing import Any


LICHESS_API_BASE = "https://lichess.org"
USER_AGENT = "lichessMCP/1.0"

async def get_lichess_user_public_data(username: str) -> str:
   url = f"{LICHESS_API_BASE}/api/user/{username}"
   data = await make_lichess_request(url)

   if not data:
        return "Unable to fetch data for the user."

   if not "username" in data:
        return "No user by this name."

   userinfo = format_user_info(data)
   return (userinfo)

async def get_lichess_users_crosstable(user1: str, user2: str) -> str  :
   url = f"{LICHESS_API_BASE}/api/crosstable/{user1}/{user2}"
   data = await make_lichess_request(url)

   if not data:
        return "Unable to fetch data for the user."
    
   crosstable = format_crosstable_info(data, user1,user2)
   return (crosstable)


  

