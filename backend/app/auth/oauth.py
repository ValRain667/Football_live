from fastapi import HTTPException
from httpx import AsyncClient

GOOGLE_CLIENT_ID = ""
GOOGLE_CLIENT_SECRET = ""
GITHUB_CLIENT_ID = ""
GITHUB_CLIENT_SECRET = ""


async def verify_google_token(token: str) -> dict:
    async with AsyncClient() as client:
        resp = await client.get(
            f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid Google token")
        return resp.json()


async def verify_github_token(token: str) -> dict:
    async with AsyncClient() as client:
        resp = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {token}"}
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid GitHub token")
        return resp.json()
