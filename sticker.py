import bot
import json

async def filter(keyword, sticker_list):
    with open('setting.json', encoding='UTF-8') as f:
        setting = json.load(f)

    for i in range(len(sticker_list["sticker"])):
        if keyword in sticker_list["sticker"][i]["keyword"]:
            return html_imgtag(sticker_list["sticker"][i]["path"], setting)

    sticker_list_doc = setting['sticker_list_doc']
    err_text = f"스티커 이름을 정확히 입력해주세요!<br>" \
               f'<br><a href="{sticker_list_doc}" target="_blank">스티커 목록 📋 바로가기</a>'
    return bot.div_template(err_text)


# 클릭시 스티커 목록 하이퍼링크
# 이미지크기 130 x 130
def html_imgtag(img_url, setting):
    sticker_list_doc = setting['sticker_list_doc']
    return f'<a href="{sticker_list_doc}" target="_blank"><img src="{img_url}" width="130" height="130"></a>'
