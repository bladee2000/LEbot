import requests
from bs4 import BeautifulSoup
import database

def get_birthday_google(artist):
    url = f"https://www.google.com/search?q={artist}+birthday"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    date = birthday_html_parser(soup)

    if date != None:
        return date
    else:
        url = f"https://www.google.com/search?q={artist}+생일"
        res = requests.get(url)

        soup = BeautifulSoup(res.text, "html.parser")
        date = birthday_html_parser(soup)

        if date != None:
            return date
        else:
            return None


def birthday_html_parser(soup):
    selecter_list = [
        "#main > div:nth-child(5) > div > div:nth-child(3) >"
        " div > div > div > div > div:nth-child(1) > div > div > div > div > div",

        "#main > div:nth-child(5) > div > div:nth-child(3) > "
        "div > div > div > div > div > div > div > div > div",

        "#main > div:nth-child(6) > div > div:nth-child(3) > div >"
        " div > div > div > div:nth-child(1) > div > div > div > div > div",

        "#main > div:nth-child(5) > div > div.xpc > div:nth-child(1) >"
        " div.vbShOe.kCrYT > div:nth-child(1) > div > span:nth-child(2) > span",

        "#main > div:nth-child(5) > div >"
        " div:nth-child(1) > div > div > div > div > span",

        "#main > div:nth-child(6) > div > div.xpc > "
        "div:nth-child(1) > div.vbShOe.kCrYT > div:nth-child(1) > "
        "div > span:nth-child(2) > span"
    ]

    for select in selecter_list:
        date = soup.select_one(select)
        if date != None:
            return date_parser(date.get_text())

    print(None)
    return None


def date_parser(date: str):
    print(date)
    if date.find("년") == -1 or date.find("월") == -1 or date.find("일") == -1:
        return None

    date = date[:date.find("일")+1]
    year = int(date[:date.find("년")])
    month = int(date[date.find("년")+1:date.find("월")])
    day = int(date[date.find("월")+1:date.find("일")])

    if month < 10:
        month = "0" + str(month)
    if day < 10:
        day = "0" + str(day)
    date = f"{str(year)}-{str(month)}-{str(day)}"
    print(date)

    if len(date) == 10:
        return date
    else:
        return None


# 상위 {limit}개 만 업데이트
# limit == 0 이면 전부 업데이트
def update_database(board, limit=0):
    post_list = []
    rapper_list = database.select_birthdayIsNull(board, limit)
    for artist in rapper_list:
        print(artist[1])
        post_list.append({
            "spotify_id": artist[0],
            "name": artist[1],
            "birthday": get_birthday_google(artist[1])
        })

    database.update_birthday(board, post_list)


if __name__ == '__main__':
    update_database("kboard", 10)

