import requests
import time
from main import create_post_session
useragent_header = {
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
            }
s = time.time()


for i in range(2):
    p = create_post_session()
    a = requests.get("https://hiphople.com/kboard",headers=useragent_header)
    print(p.__my_pw)
    p.__my_pw = "hi!"
    print(p.__my_pw)

print(time.time() - s)