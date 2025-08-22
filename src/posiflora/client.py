from json import JSONDecodeError

from aiohttp import ClientSession

from config import cfg


auth_payload = {
    "data": {
        "type": "sessions",
        "attributes": {
            "username": cfg.username,
            "password": cfg.password,
        }
    }
}


BASE_URL = "https://karban.posiflora.com/api/v1"


class PosifloraClient:
    session: ClientSession
    headers: dict
    contact: str = None
    access_token: str | None = None

    def __init__(self, contact: str):
        self.search_url = f"/customers?search={contact}"
        self.headers = {
            "Content-Type": "application/vnd.api+json",
        }

    async def run(self):
        async with ClientSession() as self.session:
            return await self.get(self.search_url)

    async def do_auth(self):
        url = f"{BASE_URL}/sessions"
        async with self.session.post(url=url, json=auth_payload, headers=self.headers) as response:
            data = await response.json()
            self.access_token = data["data"]["attributes"]["accessToken"]
            self.headers["Authorization"] = f"Bearer {self.access_token}"

    async def get(self, path: str, **kwargs):
        return await self.request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs):
        return await self.request("POST", path, **kwargs)

    async def request(self, method: str, path: str, attempt: bool = False, **kwargs):
        if not self.access_token:
            await self.do_auth()

        kwargs = dict(
            method=method,
            url=f"{BASE_URL}/{path}",
            headers=self.headers,
            **kwargs
        )
        try:
            async with self.session.request(**kwargs) as response:
                if response.status < 300:
                    try:
                        data = await response.json()
                    except JSONDecodeError:
                        data = await response.text()
                    return data

                elif response.status == 401:
                    await self.do_auth()
                    return await self.request(method, path)

                elif response.status >= 400:
                    if not attempt:
                        return await self.request(method, path, attempt=True)
        except Exception as e:
            print(f"[{method}] {path} -> {e}")