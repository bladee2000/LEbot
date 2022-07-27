import json


async def filter(command, args: list, nickname):
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

    if command in ["사클","싸클"]:
        if args:
            return soundcloud_embed(args[0])
        else:
            return div_template("링크를 입력해 주세요..")

    return div_template("잘못된 명령어 같아요...<br> 명령어 이름을 정확히 입력해주세요!")

# 출처 : https://kimmychuchu.tistory.com/78
def div_template(content: str):
    return f'<br><div style="border-radius: 5px;padding: 0.6em 1em; margin-top: 15px;' \
           f'background:#F1F1F3; display: inline-block; max-width: 90%;">{content}</div>'

# 사클 embed 플레이어
def soundcloud_embed(url):
    return f'<iframe width="100%" height="300" scrolling="no" ' \
           f'src="https://w.soundcloud.com/player/?url={url}?;' \
           f'auto_play=false&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false&amp;show_teaser=true&amp;visual=true"></iframe>'