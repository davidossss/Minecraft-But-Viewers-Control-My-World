import json, httpx, websockets, backoff
from httpx import ConnectError

class DonationAlerts:
    """
    Инициализация класса DonationAlerts.
    """
    
    def __init__(self, app_id, app_token, languageData):
        self.app_id = app_id
        self.app_token = app_token
        self.languageData = languageData

        self.redirect_uri = "http://127.0.0.1:5000/get_token"

    """
    Запускаем все методы.
    """
    async def run(self, code: str) -> None:
        await self.getting_tokens(code)
        await self.connect_through_centrifugo()
        await self.donation()

    """
    Авторизовываемся в DonationAlerts. Для этого, с помощью полученного кода, мы должны получить токен доступа, токен для сокет соединения и айди пользователя.
    """
    @backoff.on_exception(backoff.expo, ConnectError, max_tries=5)
    async def getting_tokens(self, code: str) -> None:
        async with httpx.AsyncClient() as client:
            """
            Получаем токен доступа.
            """
            token_response = await client.post(url="https://www.donationalerts.com/oauth/token",json={
                "grant_type": "authorization_code",
                "client_id": self.app_id,
                "client_secret": self.app_token,
                "redirect_uri": self.redirect_uri,
                "code": code
            })
            token_response = token_response.json()
            self.access_token = token_response["access_token"]
            
            """
            Получаем сокет токен и юзер айди.
            """
            user_response = await client.get(url="https://www.donationalerts.com/api/v1/user/oauth",headers={
                "Authorization": f"Bearer {self.access_token}"
            })
            user_response = user_response.json()
            self.user_id = user_response["data"]["id"]
            self.socket_connection_token = user_response["data"]["socket_connection_token"]

    """
    Мы получили всё что нужно. Теперь соединяемся через Centrifugo...
    """
    @backoff.on_exception(backoff.expo, ConnectError, max_tries=5)
    async def connect_through_centrifugo(self) -> None:
        """
        Подключаемся к Centrifugo и получаем клиент айди, он нам понадобится для подписок на каналы.
        """
        self.websocketConnection = await websockets.connect("wss://centrifugo.donationalerts.com/connection/websocket")
        await self.websocketConnection.send(json.dumps({
            "params": {
                "token": self.socket_connection_token
            },
            "id": 1
        }))
        connect_response = await self.websocketConnection.recv()
        client_id = json.loads(connect_response)["result"]["client"]
        
        """
        Подписываемся на каналы.
        """
        async with httpx.AsyncClient() as client:
            url_post = "https://www.donationalerts.com/api/v1/centrifuge/subscribe"
            response = await client.post(
                url=url_post,
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "channels": [f"$alerts:donation_{self.user_id}"],
                    "client": client_id
                }
            )
            
        """
        Теперь, подключаемся к каналам... готово!
        """
        for channel in response.json()["channels"]:
            await self.websocketConnection.send(json.dumps({
                "params": {
                    "channel": channel["channel"],
                    "token": channel["token"]
                },
                "method": 1,
                "id": 2
            }))
            
    """
    Теперь, когда мы подключены к DonationAlerts, мы можем получать информацию о донатах.
    """
    async def donation(self) -> None:
        onConnected = False
        while True:
            message = await self.websocketConnection.recv()
            data = json.loads(message)
            
            if onConnected == False:
                onConnected = True
                print(self.languageData["connected.donationalerts.2"])
            
            if "data" in data["result"] and "data" in data["result"]["data"]:
                await self.get_donation(data["result"]["data"]["data"])
    
    """
    Пустая функция. Нужна для работы с донатами внутри класса Minecraft.
    """
    async def get_donation(self, donation):
        pass