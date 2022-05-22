async def filter(command, arg, nickname):
    if command in ["안녕","인사"]:
        return f"{nickname} 님도 반가워요!!"

    if command in ["명령어"]:
        return "https://hiphople.com/workroom/23088801"

    if command in ["이미지"]:
        return '<img src="https://img.hiphople.com/files/attach/images/283/765/986/022/9fc5bea604aa2939bd83a6b5c30250b4.png">'

    return "잘못된 명령어같아요.."