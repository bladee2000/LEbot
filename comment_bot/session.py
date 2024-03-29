import requests
from ast import literal_eval
from bs4 import BeautifulSoup
from urllib import parse
import time


# document_srl(게시물 고유번호)를 받아 게시판(mid)을 리턴
def get_mid(document_srl):
    document_srl = str(document_srl)
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",

    }
    r = requests.get(url=f"https://hiphople.com/{document_srl}", headers=header)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup.find('div', {'id': "aplosboard"}).attrs['mid']


class create_post_session:
    with requests.Session() as s:
        def __init__(self, my_id, my_pw):
            self.csrf_token = ""
            self.__my_id = my_id
            self.__my_pw = my_pw
            self.my_nickname = ""

        # 1. HiphopLE 처음 GET 시 PHPSESSID, rx_sesskey1, rx_sesskey2, rx_uatype 발급받음(쿠키로)
        # 2. 그 후 동일 세션에서 로그인시 csrf-token 발급
        # 세션에 이미 쿠키 존재시 기존에 발급받은 self.csrf_token 리턴
        def login(self):
            if self.csrf_token:
                # print("쿠키값이 이미 존재합니다..")
                return self.csrf_token
            else:
                pass

            url = 'https://hiphople.com/'

            useragent_header = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
            }
            self.s.get(url=url, headers=useragent_header)

            login_header = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "ko-KR,ko;q=0.9",
                "cache-control": "max-age=0",
                "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
                "sec-ch-ua-platform": '"Windows"',
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "referer": "https://hiphople.com/"

            }

            login_data = f'error_return_url=%2F&mid=main&ruleset=%40login&act=procMemberLogin&success_return_url=%2F&user_id={self.__my_id}&password={self.__my_pw}'

            postlogin = self.s.post(url=url, data=login_data, headers=login_header)

            if postlogin.status_code == 429:
                time.sleep(0.5)
                self.login()

            if postlogin.status_code == 200:
                login_html = BeautifulSoup(postlogin.text, 'html.parser')
                csrf_token = login_html.select_one('meta[name="csrf-token"]')['content']
                print(csrf_token)

                assert csrf_token != '', "잘못된 아이디 혹은 비밀번호입니다..."

                # 닉네임 추출
                bs_nickname = BeautifulSoup(postlogin.text, 'html.parser')
                nick = bs_nickname.select_one("#nc_container > ul > li.nc_profile.fLeft > strong").get_text()
                print(nick)
                self.my_nickname = nick
                self.csrf_token = csrf_token

                return csrf_token

        # document_srl 만 들어올시 게시물에 댓글
        # document_srl 와 parent_srl 이 같이 들어오면 대댓글
        # document_srl : 게시물번호
        # comment : 내용
        # parent_srl : 댓글번호
        # mid : 게시판(선택)
        async def comment_write(self, document_srl, comment, parent_srl="", mid=None):
            csrf_token = self.login()
            # print(self.s.cookies.get_dict())

            if mid == None:
                mid = get_mid(document_srl)
            comment_data = {
                "_filter": "insert_comment",
                "error_return_url": f"/{str(document_srl)}",
                "member_nickname": self.my_nickname,
                "mid": str(mid),
                "document_srl": str(document_srl),
                "parent_srl": str(parent_srl),
                "use_html": "Y",
                "content": str(comment),  # 댓글 내용
                "_rx_csrf_token": str(csrf_token),
                "module": "board",
                "act": "procBoardInsertComment",
                "_rx_ajax_compat": "XMLRPC"
            }
            comment_data = parse.urlencode(comment_data)
            comment_header = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                # "x-csrf-token":f"{csrf_token}",
                "accept": "application/json, text/javascript, */*; q=0.01",
                "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"'
            }
            post_comment = self.s.post(url='https://hiphople.com/', data=comment_data, headers=comment_header)

            if post_comment.status_code == 429:
                time.sleep(0.5)
                await self.comment_write(document_srl=document_srl, comment=comment, parent_srl=parent_srl, mid=mid)
            if post_comment.status_code == 200:
                if literal_eval(post_comment.text)['error'] == -1:
                    time.sleep(0.5)
                    await self.comment_write(document_srl=document_srl, comment=comment, parent_srl=parent_srl, mid=mid)
                if literal_eval(post_comment.text)['error'] == 0:
                    return literal_eval(post_comment.text)

        # 문서 수정
        def doc_edit(self, url: str, title: str, content: str):
            csrf_token = self.login()

            url = url.replace("https://hiphople.com/", "")
            mid = url[:url.find("/")]
            document_srl = url[url.find("/") + 1:]

            if mid == "kboard":
                category = "6056078"
            elif mid == "fboard":
                category = "6056191"
            elif mid == "workroom":
                category = "197639"
            else:
                category = ""

            doc_data = {
                "_filter": "insert",
                "error_return_url": f"/index.php?mid={mid}&document_srl={document_srl}&act=dispBoardWrite",
                "act": "procBoardInsertDocument",
                "mid": mid,
                "content": content,
                "document_srl": document_srl,
                "comment_status": "ALLOW",
                "status": "PUBLIC",
                "category_srl": category,
                "title": title,
                "_rx_csrf_token": csrf_token,
                "use_editor": "Y",
                "use_html": "Y",
                "module": "board",
                "_rx_ajax_compat": "XMLRPC"
            }
            doc_data = parse.urlencode(doc_data)
            doc_header = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                # "x-csrf-token":f"{csrf_token}",
                "accept": "application/json, text/javascript, */*; q=0.01",
                "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"'
            }

            post_doc = self.s.post(url="https://hiphople.com/", data=doc_data, headers=doc_header)
            print(literal_eval(post_doc.text))


        def doc_write(self, mid: str, title: str, content: str):
            csrf_token = self.login()

            if mid == "kboard":
                category = "6056078"
            elif mid == "fboard":
                category = "6056191"
            elif mid == "workroom":
                category = "197639"
            else:
                category = ""

            doc_data = {
                "_filter": "insert",
                "error_return_url": f"/index.php?mid={mid}&act=dispBoardWrite",
                "act": "procBoardInsertDocument",
                "mid": mid,
                "content": content,
                "comment_status": "ALLOW",
                "status": "PUBLIC",
                "category_srl": category,
                "title": title,
                "_rx_csrf_token": csrf_token,
                "use_editor": "Y",
                "use_html": "Y",
                "module": "board",
                "_rx_ajax_compat": "XMLRPC"
            }
            doc_data = parse.urlencode(doc_data)
            doc_header = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                # "x-csrf-token":f"{csrf_token}",
                "accept": "application/json, text/javascript, */*; q=0.01",
                "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"'
            }
            post_doc = self.s.post(url="https://hiphople.com/", data=doc_data, headers=doc_header)
            print(literal_eval(post_doc.text))
