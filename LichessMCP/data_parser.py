
from datetime import datetime

def parse_user_performance_data(data):
    # --- Basic info ---
    user_name = data.get("user", {}).get("name", "Unknown")
    perf = data.get("perf", {})
    rating = perf.get("glicko", {}).get("rating", "N/A")
    deviation = perf.get("glicko", {}).get("deviation", "N/A")
    total_games = perf.get("nb", 0)
    progress = perf.get("progress", 0)
    rank = data.get("rank", "Unranked")
    percentile = data.get("percentile", "N/A")

    # --- Stats section ---
    stat = data.get("stat", {})
    perf_type = stat.get("perfType", {}).get("name", "Unknown")
    count = stat.get("count", {})

    wins = count.get("win", 0)
    losses = count.get("loss", 0)
    draws = count.get("draw", 0)
    tournaments = count.get("tour", 0)
    berserks = count.get("berserk", 0)
    op_avg = count.get("opAvg", 0)
    seconds_played = count.get("seconds", 0)
    disconnects = count.get("disconnects", 0)

    # --- Rating history ---
    highest = stat.get("highest", {})
    lowest = stat.get("lowest", {})

    def parse_rating_entry(entry):
        if not entry:
            return None, None, None
        rating_value = entry.get("int", None)
        date_str = entry.get("at", None)
        date = None
        if date_str:
            try:
                date = datetime.fromisoformat(date_str.replace("Z", "+00:00")).strftime("%b %d, %Y")
            except Exception:
                date = date_str
        game_id = entry.get("gameId", None)
        link = f"https://lichess.org/{game_id}" if game_id else None
        return rating_value, date, link

    high_rating, high_date, high_link = parse_rating_entry(highest)
    low_rating, low_date, low_link = parse_rating_entry(lowest)

    # --- Streaks ---
    streaks = stat.get("resultStreak", {})
    win_streak = streaks.get("win", {}).get("max", {}).get("v", 0)
    loss_streak = streaks.get("loss", {}).get("max", {}).get("v", 0)

    # --- Best wins / worst losses ---
    def parse_game_results(result_list):
        parsed = []
        for r in result_list:
            opp_info = r.get("opId", {}) or r.get("op", {})
            opp = opp_info.get("name", "Unknown")
            opp_rating = r.get("opRating") or opp_info.get("rating", "N/A")
            game_id = r.get("gameId", None)
            date_str = r.get("at", None)
            date = None
            if date_str:
                try:
                    date = datetime.fromisoformat(date_str.replace("Z", "+00:00")).strftime("%b %d, %Y")
                except Exception:
                    date = date_str
            game_link = f"https://lichess.org/{game_id}" if game_id else "N/A"
            parsed.append({
                "opponent": opp,
                "rating": opp_rating,
                "link": game_link,
                "date": date or "Unknown"
            })
        return parsed

    best_wins = parse_game_results(stat.get("bestWins", {}).get("results", []))
    worst_losses = parse_game_results(stat.get("worstLosses", {}).get("results", []))

    # --- Build Output String ---
    lines = []
    lines.append(f"=== Lichess Stats for {user_name} ===")
    lines.append(f"Mode: {perf_type}")
    lines.append(f"Rating: {rating:.0f} ±{deviation:.2f} | Progress: {progress}")
    lines.append(f"Rank: {rank} | Percentile: {percentile}%")
    lines.append(f"Games Played: {total_games}")

    if high_rating or low_rating:
        lines.append("\n--- Rating History ---")
        if high_rating:
            lines.append(f"Highest: {high_rating} on {high_date or 'Unknown'} — {high_link}")
        if low_rating:
            lines.append(f"Lowest: {low_rating} on {low_date or 'Unknown'} — {low_link}")

    lines.append("\n--- Performance ---")
    lines.append(f"Wins: {wins}, Losses: {losses}, Draws: {draws}")
    lines.append(f"Tournaments: {tournaments}, Berserks: {berserks}")
    lines.append(f"Average Opponent Strength: {op_avg}")
    lines.append(f"Total Play Time: {seconds_played // 3600}h {(seconds_played % 3600) // 60}m")
    lines.append(f"Disconnects: {disconnects}")

    lines.append("\n--- Streaks ---")
    lines.append(f"Longest Win Streak: {win_streak}")
    lines.append(f"Longest Losing Streak: {loss_streak}")

    if best_wins:
        lines.append("\n--- Best Wins ---")
        for bw in best_wins:
            lines.append(f"• Beat {bw['opponent']} ({bw['rating']}) on {bw['date']} — {bw['link']}")
    else:
        lines.append("\n--- Best Wins ---\nNone recorded.")

    if worst_losses:
        lines.append("\n--- Worst Losses ---")
        for wl in worst_losses:
            lines.append(f"• Lost to {wl['opponent']} ({wl['rating']}) on {wl['date']} — {wl['link']}")
    else:
        lines.append("\n--- Worst Losses ---\nNone recorded.")

    return "\n".join(lines)


def parse_lichess_leaderboard(data, perf_type="bullet"):
    """
    Parses Lichess leaderboard data and returns a formatted string.
    Example data source: https://lichess.org/api/player/top/10/{perf_type}
    """

    if not isinstance(data, list):
        raise ValueError("Expected a list of player data")

    lines = []
    lines.append(f"=== Lichess {perf_type.capitalize()} Leaderboard ===\n")

    for i, player in enumerate(data, start=1):
        username = player.get("username", "Unknown")
        title = player.get("title", "")
        user_id = player.get("id", "")
        perfs = player.get("perfs", {})
        perf = perfs.get(perf_type, {})

        rating = perf.get("rating", "N/A")
        progress = perf.get("progress", 0)
        patron = "💎 Patron" if player.get("patron") else ""
        color = f"(Color ID: {player.get('patronColor')})" if player.get("patronColor") else ""
        link = f"https://lichess.org/@/{user_id}"

        lines.append(f"#{i} {title + ' ' if title else ''}{username} — {rating} ({'+' if progress > 0 else ''}{progress}) {patron} {color}")
        lines.append(f"   Profile: {link}\n")

    return "\n".join(lines)



def parse_user_public_data(data):
    username = data.get("username", "Unknown")
    user_id = data.get("id", "")
    url = data.get("url", f"https://lichess.org/@/{username}")
    flair = data.get("flair", "")
    profile = data.get("profile", {})
    bio = profile.get("bio", "").strip().replace("\r", "")
    flag = profile.get("flag", "N/A")
    created = data.get("createdAt")
    seen = data.get("seenAt")

    def fmt_time(t):
        if isinstance(t, datetime):
            return t.strftime("%Y-%m-%d %H:%M:%S UTC")
        return str(t)

    # --- Ratings / Perfs ---
    perfs = data.get("perfs", {})
    perf_lines = []
    for mode, perf in perfs.items():
        if mode == "racer":
            runs = perf.get("runs", 0)
            score = perf.get("score", 0)
            perf_lines.append(f"{mode.capitalize()}: {score} points over {runs} runs")
        else:
            games = perf.get("games", 0)
            rating = perf.get("rating", "N/A")
            rd = perf.get("rd", "N/A")
            prog = perf.get("prog", 0)
            prov = perf.get("prov", False)
            perf_lines.append(f"{mode.capitalize()}: {rating} ({'+' if prog>0 else ''}{prog}), Games: {games}, RD: {rd}{' [Provisional]' if prov else ''}")

    # --- Counts ---
    count = data.get("count", {})
    counts_lines = [
        f"All games: {count.get('all', 0)}",
        f"Rated: {count.get('rated', 0)}",
        f"Wins: {count.get('win', 0)}",
        f"Losses: {count.get('loss', 0)}",
        f"Draws: {count.get('draw', 0)}",
        f"Bookmarks: {count.get('bookmark', 0)}",
        f"Playing: {count.get('playing', 0)}",
        f"Imported: {count.get('import', 0)}",
        f"Me: {count.get('me', 0)}"
    ]

    # --- Playtime ---
    playtime = data.get("playTime", {})
    total_hours = playtime.get("total", 0)/3600
    tv_hours = playtime.get("tv", 0)/3600

    # --- Build output ---
    lines = [
        f"=== Lichess Profile: {username} ===",
        f"User ID: {user_id}",
        f"Profile URL: {url}",
        f"Flag: {flag}   Flair: {flair or 'None'}",
        f"Account created: {fmt_time(created)}",
        f"Last seen: {fmt_time(seen)}",
        "\n--- Perfs / Ratings ---"
    ]
    lines += perf_lines

    lines += [
        "\n--- Counts ---"
    ]
    lines += counts_lines

    lines += [
        "\n--- Playtime ---",
        f"Total playtime: {total_hours:.1f} hours",
        f"TV playtime: {tv_hours:.1f} hours",
        "\n--- Bio ---",
        bio or "No bio provided."
    ]

    return "\n".join(lines)


def parse_team_search(json_data):
    """
    Parses paginated Lichess team JSON and returns a formatted string.
    """
    page = json_data.get("currentPage", 1)
    max_per_page = json_data.get("maxPerPage", 15)
    nb_results = json_data.get("nbResults", 0)
    nb_pages = json_data.get("nbPages", 1)

    teams = json_data.get("currentPageResults", [])

    lines = [
        f"=== Teams Page {page}/{nb_pages} ===",
        f"Showing up to {max_per_page} per page, total results: {nb_results}\n"
    ]

    for i, team in enumerate(teams, start=1):
        tid = team.get("id", "N/A")
        name = team.get("name", "Unknown")
        desc = team.get("description", "No description")
        open_status = "Open" if team.get("open") else "Closed"
        nb_members = team.get("nbMembers", 0)
        flair = team.get("flair", "None")
        
        leader = team.get("leader", {})
        leader_name = leader.get("name", "N/A")
        leader_id = leader.get("id", "N/A")
        leader_flair = leader.get("flair", "")
        leader_str = f"{leader_name} ({leader_id})"
        if leader_flair:
            leader_str += f" [{leader_flair}]"

        # all leaders
        leaders_list = team.get("leaders", [])
        leaders_str = []
        for l in leaders_list:
            lname = l.get("name", "N/A")
            lid = l.get("id", "N/A")
            lflair = l.get("flair", "")
            s = f"{lname} ({lid})"
            if lflair:
                s += f" [{lflair}]"
            leaders_str.append(s)
        leaders_formatted = ", ".join(leaders_str) if leaders_str else "None"

        lines.append(f"#{i} Team: {name} ({tid})")
        lines.append(f"   Description: {desc}")
        lines.append(f"   Status: {open_status}")
        lines.append(f"   Members: {nb_members}")
        lines.append(f"   Flair: {flair}")
        lines.append(f"   Leader: {leader_str}")
        lines.append(f"   Leaders: {leaders_formatted}\n")

    return "\n".join(lines)


def parse_team_members(members):
    """
    Parses a list of Lichess team members in the format:
    [
        {'name': ..., 'id': ..., 'url': ..., 'joinedTeamAt': ...},
        ...
    ]
    Returns a formatted string.
    """

    lines = ["=== Team Members ===\n"]

    for i, member in enumerate(members, start=1):
        name = member.get("name", "Unknown")
        user_id = member.get("id", "N/A")
        url = member.get("url", "N/A")
        joined_ts = member.get("joinedTeamAt", None)

        joined_date = "Unknown"
        if joined_ts:
            # convert milliseconds timestamp to datetime
            joined_date = datetime.utcfromtimestamp(joined_ts / 1000).strftime("%Y-%m-%d %H:%M:%S UTC")

        lines.append(f"#{i} {name} ({user_id})")
        lines.append(f"   Profile: {url}")
        lines.append(f"   Joined Team At: {joined_date}\n")

    return "\n".join(lines)
    
def parse_fide_player(fide_player):
    
    player_id = fide_player.get("id", "Unknown")
    name = fide_player.get("name", "Unknown")
    federation = fide_player.get("federation", "N/A")
    year = fide_player.get("year", "N/A")
    standard = fide_player.get("standard", "N/A")
    rapid = fide_player.get("rapid", "N/A")
    blitz = fide_player.get("blitz", "N/A")

    lines = [
        f"=== FIDE Player: {name} ===",
        f"FIDE ID: {player_id}",
        f"Federation: {federation}",
        f"Birth Year: {year}",
        "\n--- Ratings ---",
        f"Standard: {standard}",
        f"Rapid: {rapid}",
        f"Blitz: {blitz}"
    ]

    return "\n".join(lines)   
