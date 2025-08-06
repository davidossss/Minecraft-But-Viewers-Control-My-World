from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from minecraft import Minecraft

from os import path, getenv

import asyncio, json, uvicorn, webbrowser

"""
Запускаем FastAPI.
"""
app = FastAPI()

"""
Загружаем конфиг.
"""
with open(path.abspath("resources/config.json"), "r", encoding="utf-8") as textfile:
	configData = json.load(textfile)
      
with open(path.abspath(f"resources/languages/{configData["language"]}.json"), "r", encoding="utf-8") as textfile:
	languageData = json.load(textfile)

"""
Пользователю достаточно перейти на сайт, чтобы авторизоваться и подключиться в DonationAlerts.
"""
@app.get("/")
async def index():
    return RedirectResponse(f"https://www.donationalerts.com/oauth/authorize?client_id={minecraftObject.app_id}&redirect_uri={minecraftObject.redirect_uri}&response_type=code&scope=oauth-user-show%20oauth-donation-subscribe%20oauth-donation-index%20")

"""
После успешной авторизации получаем токен, который используется для соединения с DonationAlerts.
"""
@app.get("/get_token")
async def get_token(code: str):
    asyncio.create_task(minecraftObject.run(code))
    return {"status": "success", "message": languageData["connected.donationalerts.1"]}

"""
Здесь запускается скрипт и сервер.
"""
if __name__ == "__main__":
	print(f"by davidossss (github: @davidossss, version: {configData["version"]})")
	print(languageData["message.greetings"])
	
	minecraftObject = Minecraft(configData, languageData)
	
	server_address = getenv("SERVER_ADDRESS", "127.0.0.1:5000")
	host, port = server_address.split(":")

	webbrowser.open("http://127.0.0.1:5000")
	
	uvicorn.run(app, host=host, port=int(port), log_config=None)