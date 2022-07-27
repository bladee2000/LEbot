import json
import sticker
import datetime
import session

# sticker_list.json 을 불러와서 스티커 목록(엘이 게시물)을 업데이트
# 스티커 목록 = sticker_list_doc
def sticker_readme_update():
    now = datetime.datetime.now()
    html_content = f"<p>최종수정 {now.year}년 {now.month}월 {now.day}일</p><br>" \
                   f'<a href="https://dccon.dcinside.com/hot/1/nick_name/%E3%84%B1%E3%85%87%E3%84%B7#54988" target="_blank">칸예 디시콘 by ㄱㅇㄷ</a><br>' \
                   f'<a href="https://dccon.dcinside.com/hot/1/title/%EB%A6%B4%EB%B9%84#103148" target="_blank">릴비 디시콘 by 바훈우니JR</a><br>' \
                   f'<br>'
    with open("./../sticker_list.json", encoding='UTF-8') as f:
        sticker_list = json.load(f)
    with open('./../setting.json', encoding='UTF-8') as f:
        setting = json.load(f)

    for i in range(len(sticker_list["sticker"])):
        html_content += "<h2>"
        for keyword in sticker_list["sticker"][i]["keyword"]:
            html_content += f"~{keyword} "
        html_content += "</h2>"
        html_content += sticker.html_imgtag(sticker_list["sticker"][i]["path"], setting)
        html_content += "<br><br>"

    s = session.create_post_session(setting["id"], setting["pw"])
    s.doc_edit(setting["sticker_list_doc"], "스티커 목록 📋", html_content)

if __name__ == '__main__':
    sticker_readme_update()