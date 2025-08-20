import json
from aiohttp import ClientSession


url: str = "https://karban.posiflora.com/api/v1/sessions"
headers = {
        'Content-Type': 'application/vnd.api+json',
    }
payload = {
    "data": {
        "type": "sessions",
        "attributes": {
            "username": "***",
            "password": "***"
        }
    }
}

class PosifloraClient:
    session: ClientSession

    async def run(self):
        async with ClientSession() as self.session:
            await self.request()

    async def request(self):
        async with self.session.post(url=url, json=payload, headers=headers) as response:
            if response.status < 300:
                data = await response.json()
                print(json.dumps(data, indent=4))

            elif response.status >= 400:
                print(response.text)
                return
