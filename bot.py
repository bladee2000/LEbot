import json

async def filter(command, arg, nickname):
    if command in ["안녕","인사","반가워"]:
        return f"{nickname} 님도 반가워요!!"

    if command in ["명령어"]:
        with open('setting.json', encoding='UTF-8') as f:
            setting = json.load(f)
        return setting["bot_readme"]

    if command in ["스티커"]:
        with open('setting.json', encoding='UTF-8') as f:
            setting = json.load(f)
        return setting["sticker_readme"]


    return "잘못된 명령어같아요.."