import random, json, uuid
from donationalerts import DonationAlerts
from dataclasses import dataclass
from rcon.source import Client
from os import path, listdir

@dataclass
class FormatDonation:
    name: str
    array: list[str]

class Minecraft(DonationAlerts):
    """
    Инициализация класса Minecraft.
    """
    def __init__(self, configData, languageData) -> None:
        self.configData = configData
        self.languageData = languageData

        super().__init__(configData["app_id"], configData["app_token"], languageData)

        self.donations = {}

        with open(path.abspath("resources/minecraft-id.json"), "r") as textfile:
            data = json.load(textfile)

            self.listFoodId = data["food"]
            self.listItemId = data["item"]
            self.listEffectId = data["effect"]
        
        self.listFormats = [FormatDonation("$randFood", self.listFoodId), 
                            FormatDonation("$randItem", self.listItemId), 
                            FormatDonation("$randNum", None),
                            FormatDonation("$nickDonator", None),
                            FormatDonation("$randEffect", self.listEffectId)]

        donationsTXTList = listdir(path.abspath("resources/donations"))
        
        for donationTXT in donationsTXTList:
            with open(path.abspath("resources/donations/" + donationTXT), encoding="utf-8") as textfile:
                commands = [line.rstrip('\n') for line in textfile]

                self.donations[int(donationTXT[:-4])] = commands

                if "nameDonate=" in commands[0]:
                    self.donations[int(donationTXT[:-4])] = []
                    
                    self.donations[int(donationTXT[:-4])].append(commands[0][11:])
                    self.donations[int(donationTXT[:-4])].append(commands[1:])
                
        try:
            with Client(self.configData["minecraft_server_ip"], self.configData["port_rcon"], passwd=self.configData["password_rcon"]) as client:
                print(self.languageData["connected.minecraft"])

                client.run(f'gamerule sendCommandFeedback {str(self.configData["sendCommandFeedback"]).lower()}')

                self.type_text(client, f"by davidossss (github: @davidossss, version: {configData["version"]})")
                self.type_text(client, self.languageData["connected.minecraft"], "green")
        except Exception as e:
            print(self.languageData["message.error"], e)
            pass
    
    """
    Получение данных о донате.
    """
    async def get_donation(self, donation):
        random.seed(uuid.uuid4().int)

        donationAmount = round(donation["amount_in_user_currency"])
        
        if self.configData["findLastSmaller"] == True or donation["currency"] != self.configData["currency"]:
            donationAmount = self.binary_search(sorted(list(self.donations)), donationAmount)

        if (donationAmount in self.donations) == False:
            return

        textDonate1 = f'{donation["username"]} {self.languageData["message.donated.1"]} {donation["amount"]} {donation["currency"]}'
        textDonate2 = f" ({round(donation["amount_in_user_currency"])} {self.configData["currency"]}) " if donation["currency"] != self.configData["currency"] else " "
        textDonate3 = (f'{self.languageData["message.donated.2"]} {donation["message"]}' if len(donation["message"]) > 0 else self.languageData["message.donated.3"])

        textDonate = textDonate1 + textDonate2
        
        commands = self.donations[donationAmount]

        if len(commands) == 2:
            textDonate += f"{commands[0]} "
            commands = commands[1]
        
        textDonate += textDonate3
        textDonate = textDonate.replace('"', '\\"').replace('\n', ' ').replace('\r', '')

        print(textDonate)

        with Client(self.configData["minecraft_server_ip"], self.configData["port_rcon"], passwd=self.configData["password_rcon"]) as client:
            for command in commands:
                """
                Этот момент думаю мне стоит объяснить...
                Так как форматов может быть много (например их две), то мы делаем следующее:
                
                * Создаём переменную, где у нас лежит команда с изменённым первым форматом;
                * Затем создадим ещё одну, в которой лежит первоначальная команда;
                * Создаём цикл;
                * Пока первая переменная не равна второй, мы приравниваем вторую переменную с первой и "применяем" формат первой.
                
                Таким образом, у нас изменятся все форматы.
                Да, знаю, костыльно... и... если у нас всего лишь будет один формат, то из-за цикла один и тот же формат применится дважды... но, оно работает, так что...
                """

                new_form_of_command = self.applying_format(command, donation)
                old_form_of_command = command

                while new_form_of_command != old_form_of_command:
                    old_form_of_command = new_form_of_command
                    new_form_of_command = self.applying_format(new_form_of_command, donation)

                print(self.languageData["message.commandExecuted"], new_form_of_command)
                client.run(new_form_of_command)

            print("—")

            if self.configData["send_donate_info_in_minecraft_chat"] == True:
                self.type_text(client, textDonate)

    """
    Бинарный поиск, для того чтобы быстро найти последний меньший в массиве
    """
    def binary_search(self, array, num):
        l = 0
        r = len(array) - 1

        while r - l > 1:
            m = (r + l) // 2
            if array[m] >= num:
                r = m
            else:
                l = m

        if array[r] <= num:
            return array[r]
        
        if array[l] >= num:
            return num
        
        return array[l]



    """
    Применяем формат и удаляем его, если он конечно есть.
    """
    def applying_format(self, command, donation):
        for format in self.listFormats:
            if format.array != None:
                command = self.removing_format(command, format.name, donation, format.array)
            else:
                command = self.removing_format(command, format.name, donation)
        
        return command

    """
    Удаляем формат и возвращаем "реальную" команду для Minecraft.
    """
    def removing_format(self, command: str, format: str, donation, array = None):
        if format in command:
            match format:
                case "$randFood" | "$randItem" | "$randEffect":
                    random.shuffle(array)
                    command = command.replace(format, array[0], 1)
                case "$randNum":
                    left_index = command.find("$randNum(")
                    right_index = command.find(")", left_index) + 1

                    numbers = command[left_index:right_index].replace("$randNum(", "", 1).replace(")", "", 1).split(", ")
                    
                    randomNumbers = [i for i in range(int(numbers[0]), int(numbers[1]) + 1)]
                    random.shuffle(randomNumbers)

                    command = command.replace(command[left_index:right_index], str(randomNumbers[0]), 1)
                case "$nickDonator":
                    command = command.replace(format, donation["username"], 1)

        return command

    """
    Красивое напечатание текста для Minecraft.
    """
    def type_text(self, client, text, color = "white") -> None:
        client.run('tellraw @a {"text":"', f'{text}"', f',"color":"{color}"', '}')
        client.run(f'execute as @a at @s run playsound minecraft:block.note_block.bit player @s ~ ~ ~ 1 {random.uniform(0.001, 2)} 1')