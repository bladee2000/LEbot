import session
import json

with open('./../setting.json', encoding='UTF-8') as f:
    setting = json.load(f)

s = session.create_post_session(setting["id"],setting["pw"])

s.doc_edit("https://hiphople.com/workroom/23121097","안녕하다","<h1>삐용삐용</h1>")