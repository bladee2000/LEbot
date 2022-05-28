async def filter(keyword, sticker_list):
    for i in range(len(sticker_list["sticker"])):
        if keyword in sticker_list["sticker"][i]["keyword"]:
            return html_imgtag(sticker_list["sticker"][i]["path"])

    return "스티커 이름을 정확히 입력해주세요!"

def html_imgtag(img_url):
    return f'<img src="{img_url}" width="130" height="130">'
