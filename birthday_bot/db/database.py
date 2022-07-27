import sqlite3
import pprint

def insert(board, rapper_list: list):
    con = sqlite3.connect("hiphop.db")
    cur = con.cursor()
    query = f"insert or ignore into {board} values (" \
            ":spotify_id, :name, :birthday, " \
            ":popularity, :genres)"

    cur.executemany(query, rapper_list)
    con.commit()
    con.close()


def select_birthdayIsNull(board, limit=0):
    con = sqlite3.connect("hiphop.db")
    cur = con.cursor()
    if limit == 0 or type(limit) == str:
        limit = ""
    else:
        limit = "LIMIT " + str(int(limit))

    cur.execute(f"SELECT spotify_id, name, birthday FROM {board} WHERE birthday is NULL ORDER by popularity DESC {limit};")
    all_list = cur.fetchall()

    if limit != "":
        print(f"현재 {board}에 생일이 NULL 인 레코드 중 상위 {len(all_list)}개를 가져왓습니다...")
        print("-"*50)
    else:
        print(f"현재 {board}에 생일이 NULL 인 레코드 {len(all_list)}개를 전부 가져왓습니다...")
        print("-" * 50)

    con.close()
    return all_list


def update_birthday(board, rapper_list: list):
    con = sqlite3.connect("hiphop.db")
    cur = con.cursor()
    query = f"update {board} set birthday=:birthday where spotify_id=:spotify_id and name=:name"

    cur.executemany(query, rapper_list)
    con.commit()
    con.close()


if __name__ == '__main__':
    print(select_birthdayIsNull("kboard"))
    print(type("asdf") == int)