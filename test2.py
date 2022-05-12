import requests
import time
import asyncio
from functools import partial
from bs4 import BeautifulSoup
import bot

useragent_header = {
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
            }

tasks = []
error_count = 0
sus_count = 0
all_comment_doc_count = 0
mid = "workroom" # 필터링할 게시판

# 워크룸 한페이당 게시물 30개
async def get_page(i):
    global useragent_header,mid
    print(f'{i}번째 실행시작...')

    url = f"https://hiphople.com/{mid}?page={i}"

    r = partial(requests.get, url=url,headers=useragent_header)
    a = await loop.run_in_executor(None, r)
    soup = BeautifulSoup(a.text,"html.parser")

    soup = soup.select("#flagList > table > tbody > tr:not(.notice) > td.title")

    await document_filter(soup)



    print(f'{i}번째 페이지 완료')


async def document_filter(soup): # 댓글이 있는 게시물을 걸러냄 -> comment_filter로 보냄
    global all_comment_doc_count
    for x in range(0,len(soup)):
        comment = BeautifulSoup(str(soup[x]),"html.parser")
        if comment.find_all("a",attrs={"title":"댓글"}):
            all_comment_doc_count += 1
            await comment_filter("https://hiphople.com"+comment.find("a")["href"])

            #await asyncio.sleep(0.05)
            #time.sleep(0.05)
# 필요한거
# 댓글번호(parent_srl), 댓글내용, 댓글작성자
async def comment_filter(url): # 게시물을 GET해옴 그리고 댓글 필터링
    global useragent_header,error_count, sus_count
    print(url)
    par_t = partial(requests.get, url=url,headers=useragent_header)
    res = await loop.run_in_executor(None, par_t)
    print(res.status_code)
    if res.status_code == 429: # 429(너무 많은 요청)일때 재시도
        print("error... 재시도")
        error_count += 1
        #await asyncio.sleep(0.1)
        time.sleep(0.05)
        await comment_filter(url)
    if res.status_code == 200:
        comments_list = BeautifulSoup(res.text,"html.parser")
        comments_list = comments_list.select('#comment > ul > li')
        for x in range(len(comments_list)):
            comment = BeautifulSoup(str(comments_list[x]), "html.parser")

            comment_text = comment.select('.comment-body > div ')
            if len(comment_text) == 2:
                comment_text = comment.select('.comment-body > div:nth-child(2)')
            comment_text = BeautifulSoup(str(comment_text),"html.parser")

            try:
                comment_text = str(comment_text.find('p').get_text()) + " "

            except:
                # 스티커는 <class 'NoneType'> 반환
                # <class 'NoneType'>에는 get_text()가 없어 오류..
                comment_text = " "

            if comment_text[0] == "!": # !가 붙은 댓글만 필터링
                bot_command = comment_text[1:comment_text.find(" ")]
                space_pos = [pos for pos, char in enumerate(comment_text) if char == " "]
                bot_arg = []

                for ii in range(len(space_pos)-1):
                    bot_arg.append(comment_text[space_pos[ii]+1:space_pos[ii+1]])
                print(bot_command,bot_arg)
                print(bot.filter(bot_command,bot_arg))




            comment_nickname = comment.select_one('div:nth-child(1) > div:nth-child(1) > a').get_text()
            comment_srl = comments_list[x]["id"][8:]




        print("성공..!")
        sus_count += 1

def made_taks():
    global tasks
    for i in range(1,20):
        tasks.append(asyncio.create_task(get_page(i)))
    #print(tasks)
    return tasks

async def run():
    global error_count,sus_count, all_comment_doc_count
    tasks = made_taks()

    tasks_results = await asyncio.gather(*tasks)
    print(f"댓글이 있는 문서 수 : {all_comment_doc_count}")
    print(f"실패한 리퀘스트 : {error_count}\n성공한 리퀘스트 : {sus_count}")
    return tasks_results




set_t = time.time()
loop = asyncio.get_event_loop()

result = loop.run_until_complete(run())

end_t = time.time()
print(end_t - set_t)
