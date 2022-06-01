import json


async def filter(command, arg, nickname):
    if command in ["안녕","인사","반가워"]:
        content = f"{nickname} 님도 반가워요!!"
        return div_template(content)

    if command in ["명령어"]:
        with open('setting.json', encoding='UTF-8') as f:
            setting = json.load(f)
        content = setting["bot_readme"]
        return div_template(content)

    if command in ["스티커"]:
        with open('setting.json', encoding='UTF-8') as f:
            setting = json.load(f)
        sticker_list_doc = setting['sticker_list_doc']
        content = f"<h2>스티커봇 사용법</h2><br>" \
                  f"댓글에 ~[스티커이름] 을 달아주세요!<br>" \
                  f"ex) ~칸예따봉, ~젓딧소고<br>" \
                  f'<br><a href="{sticker_list_doc}" target="_blank">스티커 목록 📋 바로가기</a>'
        return div_template(content)

    if command in ["스티커목록"]:
        with open('setting.json', encoding='UTF-8') as f:
            setting = json.load(f)
        sticker_list_doc = setting['sticker_list_doc']
        content = f'<a href="{sticker_list_doc}" target="_blank">스티커 목록 📋 바로가기</a>'
        return div_template(content)

    return div_template("잘못된 명령어같아요..")

# 출처 : https://kimmychuchu.tistory.com/78
def div_template(content: str):
    return f'<br><div style="border-radius: 5px;padding: 0.6em 1em; margin-top: 15px;' \
           f'background:#F1F1F3; display: inline-block; max-width: 90%;">{content}</div>'