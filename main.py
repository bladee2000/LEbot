import requests
import time
import asyncio
from functools import partial
from bs4 import BeautifulSoup
import bot
import session
import json
from multiprocessing import Pool
import multiprocessing
import sticker

useragent_header = {
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
            }


async def get_page(i):
    global useragent_header,mid
    print(f'{i}번째 페이지 시작...')

    url = f"https://hiphople.com/{mid}?page={i}"

    r = partial(requests.get, url=url,headers=useragent_header)
    a = await loop.run_in_executor(None, r)

    assert a.status_code != 404 , f"mid 값을 정확하게 입력해주세요.. {a}"

    soup = BeautifulSoup(a.text,"html.parser")
    soup = soup.select("#flagList > table > tbody > tr:not(.notice) > td.title")

    await document_filter(soup)

    print(f'{i}번째 페이지 완료')

# 댓글이 있는 게시물을 걸러냄 -> comment_filter로 보냄
async def document_filter(soup):
    for x in range(0,len(soup)):
        comment = BeautifulSoup(str(soup[x]),"html.parser")
        if comment.find_all("a",attrs={"title":"댓글"}):

            document_srl = comment.find("a")["href"]
            document_srl = document_srl.replace(f'/{mid}/','')
            document_srl = document_srl[:document_srl.find("?")]

            await make_comment_list("https://hiphople.com"+comment.find("a")["href"],document_srl)

            time.sleep(0.05)


# 댓글 리스트 만들어서 comment_filter 로 보냄
async def make_comment_list(url, document_srl):
    global useragent_header

    # 게시물 GET
    par_t = partial(requests.get, url=url,headers=useragent_header)
    res = await loop.run_in_executor(None, par_t)

    if res.status_code == 429: # 429(너무 많은 요청)일때 재시도
        time.sleep(0.05)
        await make_comment_list(url, document_srl)
    if res.status_code == 200:
        comments_list = BeautifulSoup(res.text,"html.parser")
        comments_list = comments_list.select('#comment > ul > li')

        await comment_filter(comments_list,document_srl,url)


# 댓글 내용을 필터링함
async def comment_filter(comments_list, document_srl,url):
    for x in range(len(comments_list)):
        comment = BeautifulSoup(str(comments_list[x]), "html.parser")

        comment_text = comment.select('.comment-body > div ')
        if len(comment_text) == 2:
            comment_text = comment.select('.comment-body > div:nth-child(2)')
        comment_text = BeautifulSoup(str(comment_text), "html.parser")

        try:
            comment_text = str(comment_text.find('p').get_text()) + " "
        except:
            # 스티커는 <class 'NoneType'> 반환
            # <class 'NoneType'>에는 get_text()가 없어 오류..
            comment_text = " "

        if comment_text[0] == "!":  # !가 붙은 댓글 필터링

            if check_already_comment(comments_list[x:]):
                pass
            else:
                comment_nickname = comment.select_one('div:nth-child(1) > div:nth-child(1) > a').get_text()
                comment_srl = comments_list[x]["id"][8:]

                bot_command = comment_text[1:comment_text.find(" ")]
                space_pos = [pos for pos, char in enumerate(comment_text) if char == " "]
                bot_arg = []

                for ii in range(len(space_pos) - 1):
                    bot_arg.append(comment_text[space_pos[ii] + 1:space_pos[ii + 1]])

                bot_output = await bot.filter(bot_command, bot_arg, comment_nickname)

                comment_res =await s.comment_write(document_srl=document_srl,comment=bot_output,parent_srl=comment_srl,mid=mid)
                comment_res['redirect_url'] = f"https://hiphople.com/{mid}/{document_srl}?comment_srl={str(comment_res['comment_srl'])}#comment_{str(comment_res['comment_srl'])}"
                print('-' * 100)
                print(comment_res)
                print(f"original comment : {comment_text}")
                print(f"bot comment : {bot_output}")
                print('-' * 100)
        # 스티커
        if comment_text[0] == "~": # ~ 일때는 스티커
            if check_already_comment(comments_list[x:]):
                pass
            else:
                comment_srl = comments_list[x]["id"][8:]
                sticker_keyword = comment_text[1:comment_text.find(" ")]

                sticker_output = await sticker.filter(sticker_keyword, sticker_list)

                comment_res = await s.comment_write(document_srl=document_srl,comment=sticker_output,parent_srl=comment_srl,mid=mid)
                comment_res['redirect_url'] = f"https://hiphople.com/{mid}/{document_srl}?comment_srl={str(comment_res['comment_srl'])}#comment_{str(comment_res['comment_srl'])}"
                print('-'*100)
                print(comment_res)
                print(f"original comment : {comment_text}")
                print(f"bot comment : {sticker_output}")
                print('-' * 100)

# 이미 처리된 댓글인지 구분
def check_already_comment(comments_list):
    for i in range(len(comments_list)):
        comment = BeautifulSoup(str(comments_list[i]), "html.parser")
        comment_nickname = comment.select_one('div:nth-child(1) > div:nth-child(1) > a').get_text()
        if comment_nickname == my_nickname:
            return 1
    return 0


async def made_corutin_task(first_page, last_page):
    tasks = []
    for i in range(first_page, last_page):
        tasks.append(asyncio.create_task(get_page(i)))

    tasks_results = await asyncio.gather(*tasks)

    return tasks_results

# 코루틴 사이클을 시작하는 함수
# 1 사이클의 정의
# first_page번째 페이지 부터 last_page번째 페이지까지 스캔
# page_list 인자는 리스트 [first_page, last_page] 로 줘야댐
def start_cycle(page_list):
    global loop, mid, my_nickname, s, sticker_list, setting

    with open('setting.json', encoding='UTF-8') as f:
        setting = json.load(f)

    with open('sticker_list.json', encoding='UTF-8') as ff:
        sticker_list = json.load(ff)

    mid = setting["mid"]  # 필터링할 게시판
    s = session.create_post_session(setting["id"],setting["pw"])
    s.login()
    my_nickname = s.my_nickname

    first_page = page_list[0]
    last_page = page_list[1]
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(made_corutin_task(first_page, last_page+1))
    print("싸이클 끝..")

# 쓰레드에 페이지 범위를 균등하게 분배
# multi_page_list_ex = [[1,3],[4,6],[7,9],[10,12]] --> 1페이지부터 12페이지까지 4개의 스레드에 분배
def make_multiproces_page_list(page):
    task = page
    cpu = multiprocessing.cpu_count()
    pre_list = []
    page_list = []

    for i in range(task % cpu):
        pre_list.append(int(task/cpu)+1)
    for x in range(cpu - task % cpu):
        pre_list.append(int(task/cpu))
    for ii in range(len(pre_list)):
        sum_page_ = 0
        if pre_list[ii] == 0:
            pass
        else:
            for xx in range(ii+1):
                sum_page_ += pre_list[xx]
            page_list.append([sum_page_ - pre_list[ii] + 1, sum_page_])
    print(page_list)
    return page_list


# aws 람다용 실행함수
def lambda_handler(event, context):
    set_t = time.time()
    start_cycle([1, 5])
    end_t = time.time()
    print(end_t - set_t)


if __name__ == '__main__':

    set_t = time.time()

    pool = Pool()
    pool.map(start_cycle, make_multiproces_page_list(5))

    end_t = time.time()
    print(end_t - set_t)

