import session
import sqlite3
import random
import json


def who_today_bday(board, date="now"):
    con = sqlite3.connect("./db/hiphop.db")
    cur = con.cursor()

    cur.execute(
        f'SELECT * FROM {board} WHERE birthday like "%" || strftime("-%m-%d", "{date}", "+9 hour") ORDER by popularity DESC;')
    all_list = cur.fetchall()
    con.close()
    print(all_list)
    return all_list


def today():
    con = sqlite3.connect("./db/hiphop.db")
    cur = con.cursor()

    cur.execute(
        f"select strftime('%Y-%m-%d %H:%M:%S', 'now', '+9 hour') as strftime;")

    all_list = cur.fetchall()
    con.close()
    print(all_list)
    return all_list


def run(db, post_board):
    today_brithday_list = who_today_bday(db, "now")
    print(today_brithday_list)

    with open('secret.json', encoding='UTF-8') as f:
        secret = json.load(f)

    if today_brithday_list:
        http_session = session.create_post_session(secret["id"], secret["pw"])
        title = make_title(today_brithday_list[0][1])
        print(title)
        content = make_content(today_brithday_list)
        print(content)

        http_session.doc_write(post_board, title, content)


def make_title(artist: str):
    rand = [
        f'{artist}의 생일입니다! ',
        f'오늘은 {artist}의 생일입니다! ',
        f'생일 축하해 {artist}! '
    ]
    rand_emoji = ["🎁", "🎉", "🥳", "💖", "😍"]
    return rand[random.randint(0, len(rand) - 1)] + rand_emoji[random.randint(0, len(rand_emoji) - 1)]


def make_content(today_list: list):
    content = ""

    with open('pictures.json', encoding='UTF-8') as f:
        pictures = json.load(f)

    content += f"<strong>{today_list[0][1]}</strong>({today_list[0][2]}) 생일 축하해~ <br><br>"

    if len(today_list) >= 2:
        content += "또한 오늘은 <br>"
        for i in range(1, len(today_list)):
            content += f'<strong>{today_list[i][1]}</strong>({today_list[i][2]})<br>'
        content += "<br>의 생일이기도 합니다! <br><br> 모두들 생일 축하해~<br><br>"

    content += f'<div style="width:270px; height:270px;">' \
               f'{pictures["end_content"][random.randint(0, len(pictures["end_content"]) - 1)]}' \
               f'</div>'

    return content


def lambda_handler(event, context):
    run("fboard", "workroom")
    run("kboard", "workroom")


if __name__ == '__main__':
    run("fboard", "workroom")
    run("kboard", "workroom")

