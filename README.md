# Майнкрафт, но зрители управляют моим миром

«Майнкрафт, но зрители управляют моим миром» — Python-программа, благодаря которой, зрители могут управлять вашим миром через DonationAlerts! Первая версия этой программы была сделана ещё в 2023 году, но я решил полностью обновить её, сделав с нуля.

# Установка

## Создание приложения в DonationAlerts

Для начала, нам нужно создать приложение: 

1. Перейдите [по этой ссылке](https://www.donationalerts.com/application/clients).
2. Нажмите на кнопку "Создать новое приложение".
3. Вводите любое имя приложения, в URL перенаправления вводите следующее: http://127.0.0.1:5000/get_token 

## Подготовка сервера в Minecraft

Далее, вам нужно иметь сервер в Minecraft с возможностью включения RCON (Aternos не подойдёт, увы).
Если у вас нет сервера и вы не можете покупать хостинг, просмотрите следующий пункт.
Если у вас уже есть сервер, перейдите к пункту изменение server.properties.

### Установка локального Minecraft сервера

1. Установите [RadminVPN](https://www.radmin-vpn.com/ru).
2. После установки, включите его.

3. Теперь, установите [локальный сервер](https://www.minecraft.net/en-us/download/server) и расположите его в отдельную папку.
   p.s. Если вы хотите скачать другую версию, скачивайте [с этого сайта](https://mcversions.net) server.jar.

4. Создайте start.bat со следующими командами:
   ```bat
   java -Xmx1024M -Xms1024M -jar server.jar nogui
   pause
   ```
5. Запустите этот файл. После того как он попросит принять соглашение, закройте файл, примите его в файле eula.txt (поменяв false на true), и откройте снова файл.

6. Когда сервер откроется, закрываем его опять и заходим в server.properties.

## Изменение server.properties

1. Измените enable-rcon на true.

2. Измените rcon.password на очень сложный пароль. **ВАЖНО!** Конкретно на сложный!

Следующие пункты относятся к вам, если у вас локальный сервер:

3. Измените server-ip на айпи из программы RadminVPN.

4. Если у вас "пиратка", то измените online-mode на false.

## Скачивание Python-программы

1. Установите следующие библиотеки:
   ```bash
   pip install backoff==2.2.1
   pip install fastapi==0.116.1
   pip install httpx==0.28.1
   pip install rcon==2.4.9
   pip install uvicorn==0.35.0
   pip install websockets==15.0.1
   ```

2. Скачиваем и распаковываем архив.
3. Изменяем config.json в папке resources следующее:
   - `app_id` — айди вашего приложения, обязательно без кавычек!
   - `app_token` — токен вашего приложения, обязательно с кавычками!
   - `minecraft_server_ip` — айпи вашего сервера, обязательно с кавычками!
   - `port_rcon` — порт RCON, если вы его не трогали, оставьте всё как есть, обязательно без кавычек!
   - `password_rcon` — пароль RCON, обязательно с кавычками!
4. Это вы можете изменять по желанию:
   - `language` — язык программы (доступны ru-RU и en-US).
   - `sendCommandFeedback` — отправляет в чат Minecraft какие команды были сделаны, лучше отключить для красоты.
   - `send_donate_info_in_minecraft_chat` — отправляет в чат Minecraft информацию о том, кто прямо сейчас задонатил.
   - `findLastSmaller` — если этот пункт будет включён (включено по умолчанию), то в папке donations будет искаться последний наименьший "донат". Например, если в папке есть 25.txt, 35.txt и пользователь задонатил 30, то будет проигрываться файл 25.txt. В противном случае, если этот пункт будет выключен, то донат проигнорируется, так как он должен быть строго равен "донатам" из папки donations.
   - `currency` — валюта, в формате alfa-3. Если в донате будет другая валюта, то она конвертируется в вашу. При этом, схема выбора "донатов" из папки donations будет аналогична findFirstSmaller.

## Запуск программы
Запускайте файл main.py. Если всё правильно настроено, вам будет нужно пройти авторизацию в DonationAlerts, вскоре вы можете наконец играть! Если же у вас появились какие-то проблемы с запуском, пишите в Issues.

# Дополнительное
### Папка donations
Чтобы добавить особое условие для доната, добавляйте файл с ценой доната в названии, вот так: 250.txt. Внутри этого файла, добавляйте команды для веселья!

**ВАЖНО!** Имейте в виду, что все команды выполняются от лица сервера! Поэтому не забывайте про ```/execute as @a at @s``` в случае чего.

### Форматы
Вы можете добавлять разные форматы в донаты, например:
```give @a $randItem $randNum(1, 32)```


Вот какие есть форматы на сегодняшний день:
- ```$randFood``` — выбирает рандомную еду из minecraft-id.json.
- ```$randItem``` — выбирает рандомный предмет из minecraft-id.json.
- ```$randEffect``` — выбирает рандомный эффект из minecraft-id.json.
- ```$randNum(a, b)``` — выбирает рандомное число от a до b включительно.
- ```$nickDonator``` — заменяет этот формат на имя донатера.

Также есть ещё один особенный формат: если вы хотите как-то "назвать" донат, добавьте в начале файла следующее:
```nameDonate=на уж очень смешное действие```, в чате это будет выглядеть так:
```Имя пользователя задонатил(а) 50 RUB **на уж очень смешное действие** со словами: сообщение```

### Файл minecraft-id
В этом файле прописаны эффекты, еда и предметы. По желанию, вы можете его изменять.

by davidossss (@davidossss)

------------

# Minecraft, But Viewers Control My World  

"Minecraft, But Viewers Control My World" is a Python program that allows viewers to control your Minecraft world via DonationAlerts! The first version of this program was created back in 2023, but I decided to completely overhaul it, rewriting it from scratch.  

# Installation  

## Creating a DonationAlerts Application  

First, we need to create an application:  

1. Go to [this link](https://www.donationalerts.com/application/clients).  
2. Click the "Create New Application" button.  
3. Enter any name for the application, and in the redirect URL, enter the following: `http://127.0.0.1:5000/get_token`.  

## Preparing a Minecraft Server  

Next, you need a Minecraft server with RCON enabled (Aternos won't work, unfortunately).  
If you don’t have a server and can’t afford hosting, check the next section.  
If you already have a server, skip to the **server.properties modification** section.  

### Setting Up a Local Minecraft Server  

1. Install [RadminVPN](https://www.radmin-vpn.com/).  
2. After installation, launch it.  

3. Now, download the [local server](https://www.minecraft.net/en-us/download/server) and place it in a separate folder.  
   *Note: If you want a different version, download `server.jar` from [this site](https://mcversions.net).*  

4. Create a `start.bat` file with the following commands:  
   ```bat
   java -Xmx1024M -Xms1024M -jar server.jar nogui
   pause
   ```  
5. Run this file. After it asks you to accept the EULA, close it, edit `eula.txt` (changing `false` to `true`), and reopen the file.  

6. Once the server starts, close it again and open `server.properties`.  

## Modifying server.properties  

1. Change `enable-rcon` to `true`.  

2. Set `rcon.password` to a very strong password. **IMPORTANT!** Make sure it's strong!  

The following steps apply only if you're running a local server:  

3. Change `server-ip` to the IP from RadminVPN.  

4. If you're using a "pirated" version, set `online-mode` to `false`.  

## Downloading the Python Program  

1. Install the required libraries:  
   ```bash
   pip install backoff==2.2.1
   pip install fastapi==0.116.1
   pip install httpx==0.28.1
   pip install rcon==2.4.9
   pip install uvicorn==0.35.0
   pip install websockets==15.0.1
   ```  

2. Download and extract the archive.  
3. Modify `config.json` in the `resources` folder:  
   - `app_id` – your application ID (must be without quotes!)  
   - `app_token` – your application token (must be in quotes!)  
   - `minecraft_server_ip` – your server IP (must be in quotes!)  
   - `port_rcon` – RCON port (leave as default if unchanged, must be without quotes!)  
   - `password_rcon` – RCON password (must be in quotes!)  
4. Optional settings (adjust as desired):
   - `language` — the language of the program (en-US and ru-RU are available).  
   - `sendCommandFeedback` – sends executed commands to Minecraft chat (better to disable for aesthetics).  
   - `send_donate_info_in_minecraft_chat` – sends donation info to Minecraft chat (who donated and how much).  
   - `findLastSmaller` – if enabled (default), the program will look for the last smaller "donation" in the `donations` folder. For example, if there are `25.txt` and `35.txt` and a user donates 30, `25.txt` will be executed. If disabled, donations not matching exact amounts will be ignored.  
   - `currency` – currency in alfa-3 format. If a donation is in a different currency, it will be converted to yours. The selection logic for donation files follows the same rules as `findLastSmaller`.  

## Running the Program  
Launch `main.py`. If everything is set up correctly, you’ll need to authorize via DonationAlerts, and then you can finally play! If you encounter any issues, report them in **Issues**.  

# Additional Features  

### The `donations` Folder  
To add special conditions for donations, create a file named after the donation amount, like `250.txt`. Inside this file, add commands for fun!  

**IMPORTANT!** Keep in mind that all commands are executed as the server! So don’t forget to use `/execute as @a at @s` where needed.  

### Formats  
You can use various formats in donation files, for example:  
```give @a $randItem $randNum(1, 32)```  

Here are the available formats:  
- `$randFood` – selects random food from `minecraft-id.json`.  
- `$randItem` – selects a random item from `minecraft-id.json`.  
- `$randEffect` – selects a random effect from `minecraft-id.json`.  
- `$randNum(a, b)` – selects a random number between `a` and `b` (inclusive).  
- `$nickDonator` – replaces this placeholder with the donor’s name.  

There’s also a special format: if you want to "name" a donation, add this at the beginning of the file:  
```nameDonate=some very funny action```  
In chat, it will look like this:  
```Username donated 50 RUB **for some very funny action** with the message: text```  

### The `minecraft-id.json` File  
This file contains effects, food, and items. You can modify it as needed.  

by davidossss (@davidossss)
