import json
from typing import List, Optional
from datetime import datetime, timedelta
import httpx
from app.schemas.match import MatchOut, MatchTeam, MatchEvent
from app.schemas.team import TeamOut
from app.schemas.league import LeagueOut
from app.services.cache import redis_client
from app.config import settings


class _DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def _to_json(data):
    return json.dumps(data, cls=_DateTimeEncoder)


_API_BASE = "https://v3.football.api-sports.io"


def _api_headers():
    return {
        "x-apisports-key": settings.FOOTBALL_API_KEY,
    }


async def _api_get(endpoint: str, params: Optional[dict] = None) -> list:
    if settings.FOOTBALL_API_KEY in ("", "YOUR_API_KEY"):
        return []
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                f"{_API_BASE}/{endpoint}",
                headers=_api_headers(),
                params=params,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("response", [])
    except Exception:
        return []


def _parse_fixture(item: dict) -> MatchOut:
    fixture = item.get("fixture", {})
    league = item.get("league", {})
    teams = item.get("teams", {})
    goals = item.get("goals", {})
    events_raw = item.get("events", [])
    stats_raw = item.get("statistics", [])

    status_short = fixture.get("status", {}).get("short", "NS")
    minute = fixture.get("status", {}).get("elapsed")
    if status_short in ("1H", "HT", "2H", "ET", "P", "LIVE"):
        status = "LIVE"
    elif status_short in ("FT", "AET", "PEN"):
        status = "finished"
    elif status_short in ("NS", "TBD"):
        status = "upcoming"
    else:
        status = status_short

    date_str = fixture.get("date")
    try:
        date = datetime.fromisoformat(date_str.replace("Z", "+00:00")) if date_str else datetime.now()
    except Exception:
        date = datetime.now()

    home_team_data = teams.get("home", {})
    away_team_data = teams.get("away", {})

    events = []
    for ev in events_raw:
        ev_time = str(ev.get("time", {}).get("elapsed", ""))
        extra = ev.get("time", {}).get("extra")
        if extra:
            ev_time += f"+{extra}"
        ev_time += "'"
        ev_type = ev.get("type", "").lower()
        if ev_type == "card":
            detail = (ev.get("detail") or "").lower()
            if "red" in detail:
                ev_type = "red"
            else:
                ev_type = "yellow"
        elif ev_type == "subst":
            ev_type = "substitution"
        events.append(MatchEvent(
            time=ev_time,
            type=ev_type,
            player=ev.get("player", {}).get("name"),
            team=ev.get("team", {}).get("name", ""),
        ))

    possession = None
    statistics = {}
    for stat_group in stats_raw:
        group_stats = stat_group.get("statistics", [])
        for stat in group_stats:
            stat_type = (stat.get("type") or "").lower().replace(" ", "_").replace("%", "")
            home_val = stat.get("value")
            away_val = None
            # API-Football returns stats per team in separate groups
            # But we parse what we can from the nested structure
            # For simplicity, if home_val is a string with %, strip it
            if isinstance(home_val, str) and "%" in home_val:
                try:
                    home_val = int(home_val.replace("%", "").strip())
                except ValueError:
                    pass
            if stat_type == "ball_possession":
                possession = {"home": home_val or 0, "away": 0}
            else:
                statistics[stat_type] = {"home": home_val or 0, "away": 0}
    # Try to pair away stats by scanning again (simple heuristic)
    if possession:
        for stat_group in stats_raw:
            group_stats = stat_group.get("statistics", [])
            for stat in group_stats:
                if (stat.get("type") or "").lower() == "ball possession":
                    away_val = stat.get("value")
                    if isinstance(away_val, str) and "%" in away_val:
                        try:
                            away_val = int(away_val.replace("%", "").strip())
                        except ValueError:
                            pass
                    possession["away"] = away_val or (100 - (possession["home"] or 0))
    # Clean stats
    stats_map = {
        "shots_on_goal": "shots_on_target",
        "total_shots": "shots",
        "corner_kicks": "corners",
    }
    clean_statistics = {}
    for k, v in statistics.items():
        key = stats_map.get(k, k)
        clean_statistics[key] = v

    return MatchOut(
        id=fixture.get("id", 0),
        home_team=MatchTeam(
            id=home_team_data.get("id", 0),
            name=home_team_data.get("name", ""),
            logo=home_team_data.get("logo"),
            score=goals.get("home"),
        ),
        away_team=MatchTeam(
            id=away_team_data.get("id", 0),
            name=away_team_data.get("name", ""),
            logo=away_team_data.get("logo"),
            score=goals.get("away"),
        ),
        league=league.get("name", ""),
        league_logo=league.get("logo"),
        status=status,
        minute=minute,
        date=date,
        events=events,
        possession=possession,
        statistics=clean_statistics if clean_statistics else None,
    )


def _parse_team(item: dict) -> TeamOut:
    return TeamOut(
        id=item.get("id", 0),
        name=item.get("name", ""),
        logo=item.get("logo"),
        country=item.get("country", ""),
        founded=item.get("founded"),
        stadium=item.get("venue"),
    )


def _parse_league(item: dict) -> LeagueOut:
    return LeagueOut(
        id=item.get("id", 0),
        name=item.get("name", ""),
        country=item.get("country", {}).get("name", ""),
        logo=item.get("logo"),
    )


DEMO_TEAMS = {
    1: {"id": 1, "name": "Manchester City", "logo": "https://media.api-sports.io/football/teams/50.png", "country": "England", "founded": 1880, "stadium": "Etihad Stadium", "coach": "Pep Guardiola"},
    2: {"id": 2, "name": "Liverpool", "logo": "https://media.api-sports.io/football/teams/40.png", "country": "England", "founded": 1892, "stadium": "Anfield", "coach": "Arne Slot"},
    3: {"id": 3, "name": "Real Madrid", "logo": "https://media.api-sports.io/football/teams/541.png", "country": "Spain", "founded": 1902, "stadium": "Santiago Bernabeu", "coach": "Carlo Ancelotti"},
    4: {"id": 4, "name": "Barcelona", "logo": "https://media.api-sports.io/football/teams/529.png", "country": "Spain", "founded": 1899, "stadium": "Camp Nou", "coach": "Hansi Flick"},
    5: {"id": 5, "name": "Bayern Munich", "logo": "https://media.api-sports.io/football/teams/157.png", "country": "Germany", "founded": 1900, "stadium": "Allianz Arena", "coach": "Vincent Kompany"},
    6: {"id": 6, "name": "Borussia Dortmund", "logo": "https://media.api-sports.io/football/teams/165.png", "country": "Germany", "founded": 1909, "stadium": "Signal Iduna Park", "coach": "Nuri Sahin"},
    7: {"id": 7, "name": "Juventus", "logo": "https://media.api-sports.io/football/teams/496.png", "country": "Italy", "founded": 1897, "stadium": "Allianz Stadium", "coach": "Thiago Motta"},
    8: {"id": 8, "name": "Inter Milan", "logo": "https://media.api-sports.io/football/teams/505.png", "country": "Italy", "founded": 1908, "stadium": "San Siro", "coach": "Simone Inzaghi"},
    9: {"id": 9, "name": "PSG", "logo": "https://media.api-sports.io/football/teams/85.png", "country": "France", "founded": 1970, "stadium": "Parc des Princes", "coach": "Luis Enrique"},
    10: {"id": 10, "name": "Marseille", "logo": "https://media.api-sports.io/football/teams/81.png", "country": "France", "founded": 1899, "stadium": "Orange Velodrome", "coach": "Roberto De Zerbi"},
    11: {"id": 11, "name": "Arsenal", "logo": "https://media.api-sports.io/football/teams/42.png", "country": "England", "founded": 1886, "stadium": "Emirates Stadium", "coach": "Mikel Arteta"},
    12: {"id": 12, "name": "Chelsea", "logo": "https://media.api-sports.io/football/teams/49.png", "country": "England", "founded": 1905, "stadium": "Stamford Bridge", "coach": "Enzo Maresca"},
}

DEMO_LEAGUES = [
    {"id": 39, "name": "Premier League", "country": "England", "logo": "https://media.api-sports.io/football/leagues/39.png"},
    {"id": 140, "name": "La Liga", "country": "Spain", "logo": "https://media.api-sports.io/football/leagues/140.png"},
    {"id": 135, "name": "Serie A", "country": "Italy", "logo": "https://media.api-sports.io/football/leagues/135.png"},
    {"id": 78, "name": "Bundesliga", "country": "Germany", "logo": "https://media.api-sports.io/football/leagues/78.png"},
    {"id": 61, "name": "Ligue 1", "country": "France", "logo": "https://media.api-sports.io/football/leagues/61.png"},
    {"id": 2, "name": "Champions League", "country": "Europe", "logo": "https://media.api-sports.io/football/leagues/2.png"},
    {"id": 3, "name": "Europa League", "country": "Europe", "logo": "https://media.api-sports.io/football/leagues/3.png"},
]


def _demo_matches(status: Optional[str] = None) -> List[MatchOut]:
    now = datetime.now()
    matches = [
        MatchOut(
            id=1001,
            home_team=MatchTeam(id=1, name="Manchester City", logo=DEMO_TEAMS[1]["logo"], score=2 if status != "upcoming" else None),
            away_team=MatchTeam(id=11, name="Arsenal", logo=DEMO_TEAMS[11]["logo"], score=1 if status != "upcoming" else None),
            league="Premier League", league_logo=DEMO_LEAGUES[0]["logo"],
            status="LIVE", minute=67, date=now,
            events=[MatchEvent(time="12'", type="goal", player="Haaland", team="Manchester City"),
                    MatchEvent(time="34'", type="yellow", player="Saliba", team="Arsenal"),
                    MatchEvent(time="45'", type="goal", player="Saka", team="Arsenal"),
                    MatchEvent(time="58'", type="goal", player="De Bruyne", team="Manchester City")],
            possession={"home": 62, "away": 38},
            statistics={"shots": {"home": 14, "away": 8}, "shots_on_target": {"home": 6, "away": 3}, "corners": {"home": 7, "away": 3}}
        ),
        MatchOut(
            id=1002,
            home_team=MatchTeam(id=3, name="Real Madrid", logo=DEMO_TEAMS[3]["logo"], score=3 if status != "upcoming" else None),
            away_team=MatchTeam(id=4, name="Barcelona", logo=DEMO_TEAMS[4]["logo"], score=2 if status != "upcoming" else None),
            league="La Liga", league_logo=DEMO_LEAGUES[1]["logo"],
            status="LIVE", minute=78, date=now,
            events=[MatchEvent(time="5'", type="goal", player="Bellingham", team="Real Madrid"),
                    MatchEvent(time="22'", type="goal", player="Lewandowski", team="Barcelona"),
                    MatchEvent(time="51'", type="red", player="Gavi", team="Barcelona"),
                    MatchEvent(time="65'", type="goal", player="Vinicius", team="Real Madrid"),
                    MatchEvent(time="71'", type="goal", player="Mbappe", team="Real Madrid"),
                    MatchEvent(time="75'", type="goal", player="Yamal", team="Barcelona")],
            possession={"home": 55, "away": 45},
            statistics={"shots": {"home": 18, "away": 12}, "shots_on_target": {"home": 8, "away": 5}, "corners": {"home": 9, "away": 6}}
        ),
        MatchOut(
            id=1003,
            home_team=MatchTeam(id=5, name="Bayern Munich", logo=DEMO_TEAMS[5]["logo"], score=1),
            away_team=MatchTeam(id=6, name="Borussia Dortmund", logo=DEMO_TEAMS[6]["logo"], score=1),
            league="Bundesliga", league_logo=DEMO_LEAGUES[3]["logo"],
            status="LIVE", minute=34, date=now,
            events=[MatchEvent(time="18'", type="goal", player="Kane", team="Bayern Munich"),
                    MatchEvent(time="29'", type="goal", player="Adeyemi", team="Borussia Dortmund")],
            possession={"home": 58, "away": 42},
            statistics={"shots": {"home": 9, "away": 6}, "shots_on_target": {"home": 4, "away": 2}, "corners": {"home": 4, "away": 2}}
        ),
        MatchOut(
            id=1004,
            home_team=MatchTeam(id=2, name="Liverpool", logo=DEMO_TEAMS[2]["logo"], score=None),
            away_team=MatchTeam(id=12, name="Chelsea", logo=DEMO_TEAMS[12]["logo"], score=None),
            league="Premier League", league_logo=DEMO_LEAGUES[0]["logo"],
            status="upcoming", minute=None, date=now + timedelta(hours=2),
            events=[], possession=None, statistics=None
        ),
        MatchOut(
            id=1005,
            home_team=MatchTeam(id=7, name="Juventus", logo=DEMO_TEAMS[7]["logo"], score=None),
            away_team=MatchTeam(id=8, name="Inter Milan", logo=DEMO_TEAMS[8]["logo"], score=None),
            league="Serie A", league_logo=DEMO_LEAGUES[2]["logo"],
            status="upcoming", minute=None, date=now + timedelta(hours=3, minutes=30),
            events=[], possession=None, statistics=None
        ),
        MatchOut(
            id=1006,
            home_team=MatchTeam(id=9, name="PSG", logo=DEMO_TEAMS[9]["logo"], score=2),
            away_team=MatchTeam(id=1, name="Manchester City", logo=DEMO_TEAMS[1]["logo"], score=1),
            league="Champions League", league_logo=DEMO_LEAGUES[5]["logo"],
            status="finished", minute=None, date=now - timedelta(days=1),
            events=[MatchEvent(time="7'", type="goal", player="Dembele", team="PSG"),
                    MatchEvent(time="44'", type="goal", player="Foden", team="Manchester City"),
                    MatchEvent(time="88'", type="goal", player="Kolo Muani", team="PSG")],
            possession={"home": 48, "away": 52},
            statistics={"shots": {"home": 11, "away": 15}, "shots_on_target": {"home": 5, "away": 6}, "corners": {"home": 5, "away": 8}}
        ),
    ]
    if status:
        matches = [m for m in matches if m.status == status]
    return matches


async def get_matches(date: Optional[str] = None, league_id: Optional[int] = None, status: Optional[str] = None) -> List[MatchOut]:
    cache_key = f"matches:{date}:{league_id}:{status}"
    cached = await redis_client.get(cache_key)
    if cached:
        data = json.loads(cached)
        return [MatchOut(**item) for item in data]
    params = {}
    if date:
        params["date"] = date
    if league_id:
        params["league"] = league_id
    if status == "LIVE":
        params["live"] = "all"
    elif status == "upcoming":
        params["status"] = "NS-TBD"
    elif status == "finished":
        params["status"] = "FT-AET-PEN"
    api_data = await _api_get("fixtures", params if params else None)
    if api_data:
        result = [_parse_fixture(item) for item in api_data]
        await redis_client.setex(cache_key, 60, _to_json([m.model_dump() for m in result]))
        return result
    result = _demo_matches(status)
    await redis_client.setex(cache_key, 60, _to_json([m.model_dump() for m in result]))
    return result


async def get_live_matches() -> List[MatchOut]:
    cache_key = "matches:live"
    cached = await redis_client.get(cache_key)
    if cached:
        data = json.loads(cached)
        return [MatchOut(**item) for item in data]
    api_data = await _api_get("fixtures", {"live": "all"})
    if api_data:
        result = [_parse_fixture(item) for item in api_data]
        await redis_client.setex(cache_key, 30, _to_json([m.model_dump() for m in result]))
        return result
    result = _demo_matches(status="LIVE")
    await redis_client.setex(cache_key, 30, _to_json([m.model_dump() for m in result]))
    return result


async def get_match_by_id(match_id: int) -> Optional[MatchOut]:
    cache_key = f"match:{match_id}"
    cached = await redis_client.get(cache_key)
    if cached:
        return MatchOut(**json.loads(cached))
    api_data = await _api_get("fixtures", {"id": match_id})
    if api_data:
        match = _parse_fixture(api_data[0])
        await redis_client.setex(cache_key, 60, _to_json(match.model_dump()))
        return match
    for m in _demo_matches():
        if m.id == match_id:
            await redis_client.setex(cache_key, 60, _to_json(m.model_dump()))
            return m
    return None


async def get_teams(search: Optional[str] = None) -> List[TeamOut]:
    if search:
        api_data = await _api_get("teams", {"search": search})
        if api_data:
            return [_parse_team(item["team"]) for item in api_data]
    else:
        api_data = await _api_get("teams", {"league": 39, "season": 2024})
        if api_data:
            return [_parse_team(item["team"]) for item in api_data]
    teams = [TeamOut(**t) for t in DEMO_TEAMS.values()]
    if search:
        search = search.lower()
        teams = [t for t in teams if search in t.name.lower() or (t.country and search in t.country.lower())]
    return teams


async def get_team_by_id(team_id: int) -> Optional[TeamOut]:
    api_data = await _api_get("teams", {"id": team_id})
    if api_data:
        return _parse_team(api_data[0]["team"])
    t = DEMO_TEAMS.get(team_id)
    if t:
        return TeamOut(**t)
    return None


async def get_leagues() -> List[LeagueOut]:
    api_data = await _api_get("leagues")
    if api_data:
        return [_parse_league(item["league"]) for item in api_data]
    return [LeagueOut(**l) for l in DEMO_LEAGUES]


async def get_league_by_id(league_id: int) -> Optional[LeagueOut]:
    api_data = await _api_get("leagues", {"id": league_id})
    if api_data:
        return _parse_league(api_data[0]["league"])
    for l in DEMO_LEAGUES:
        if l["id"] == league_id:
            return LeagueOut(**l)
    return None


def _parse_standings_row(row: dict) -> dict:
    team = row.get("team", {})
    all_stats = row.get("all", {})
    goals = all_stats.get("goals", {})
    return {
        "position": row.get("rank", 0),
        "team": {
            "id": team.get("id", 0),
            "name": team.get("name", ""),
            "logo": team.get("logo"),
            "country": "",
        },
        "played": all_stats.get("played", 0),
        "won": all_stats.get("win", 0),
        "draw": all_stats.get("draw", 0),
        "lost": all_stats.get("lose", 0),
        "goals_for": goals.get("for", 0),
        "goals_against": goals.get("against", 0),
        "goal_difference": row.get("goalsDiff", 0),
        "points": row.get("points", 0),
        "form": list(row.get("form", "")) if row.get("form") else [],
    }


async def get_standings(league_id: int, season: str = "2024") -> List[dict]:
    cache_key = f"standings:{league_id}:{season}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    api_data = await _api_get("standings", {"league": league_id, "season": season})
    if api_data:
        rows = api_data[0].get("league", {}).get("standings", [])
        if rows and isinstance(rows[0], list):
            result = [_parse_standings_row(r) for r in rows[0]]
        elif rows:
            result = [_parse_standings_row(r) for r in rows]
        else:
            result = []
        await redis_client.setex(cache_key, 120, json.dumps(result))
        return result
    demo = [
        {"position": 1, "team": DEMO_TEAMS[1], "played": 28, "won": 20, "draw": 4, "lost": 4, "goals_for": 62, "goals_against": 24, "goal_difference": 38, "points": 64, "form": ["W", "W", "D", "W", "W"]},
        {"position": 2, "team": DEMO_TEAMS[11], "played": 28, "won": 19, "draw": 5, "lost": 4, "goals_for": 58, "goals_against": 26, "goal_difference": 32, "points": 62, "form": ["W", "D", "W", "W", "L"]},
        {"position": 3, "team": DEMO_TEAMS[2], "played": 28, "won": 18, "draw": 6, "lost": 4, "goals_for": 55, "goals_against": 28, "goal_difference": 27, "points": 60, "form": ["W", "W", "W", "D", "W"]},
        {"position": 4, "team": DEMO_TEAMS[12], "played": 28, "won": 14, "draw": 6, "lost": 8, "goals_for": 48, "goals_against": 36, "goal_difference": 12, "points": 48, "form": ["L", "W", "D", "W", "W"]},
        {"position": 5, "team": DEMO_TEAMS[3], "played": 28, "won": 22, "draw": 4, "lost": 2, "goals_for": 68, "goals_against": 22, "goal_difference": 46, "points": 70, "form": ["W", "W", "W", "W", "D"]},
        {"position": 6, "team": DEMO_TEAMS[4], "played": 28, "won": 20, "draw": 4, "lost": 4, "goals_for": 64, "goals_against": 26, "goal_difference": 38, "points": 64, "form": ["W", "L", "W", "W", "W"]},
        {"position": 7, "team": DEMO_TEAMS[5], "played": 26, "won": 20, "draw": 4, "lost": 2, "goals_for": 72, "goals_against": 20, "goal_difference": 52, "points": 64, "form": ["W", "W", "W", "D", "W"]},
        {"position": 8, "team": DEMO_TEAMS[6], "played": 26, "won": 13, "draw": 6, "lost": 7, "goals_for": 48, "goals_against": 36, "goal_difference": 12, "points": 45, "form": ["L", "W", "D", "L", "W"]},
        {"position": 9, "team": DEMO_TEAMS[8], "played": 28, "won": 21, "draw": 5, "lost": 2, "goals_for": 60, "goals_against": 22, "goal_difference": 38, "points": 68, "form": ["W", "W", "D", "W", "W"]},
        {"position": 10, "team": DEMO_TEAMS[7], "played": 28, "won": 15, "draw": 7, "lost": 6, "goals_for": 45, "goals_against": 28, "goal_difference": 17, "points": 52, "form": ["W", "D", "W", "L", "W"]},
        {"position": 11, "team": DEMO_TEAMS[9], "played": 26, "won": 18, "draw": 6, "lost": 2, "goals_for": 58, "goals_against": 24, "goal_difference": 34, "points": 60, "form": ["W", "W", "D", "W", "W"]},
        {"position": 12, "team": DEMO_TEAMS[10], "played": 26, "won": 12, "draw": 6, "lost": 8, "goals_for": 40, "goals_against": 32, "goal_difference": 8, "points": 42, "form": ["L", "W", "L", "D", "W"]},
    ]
    await redis_client.setex(cache_key, 120, json.dumps(demo))
    return demo
