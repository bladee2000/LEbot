async def filter(command, arg, nickname):
    if command in ["안녕","인사"]:
        return f"{nickname} 님도 반가워요!!"


    return "잘못된 명령어같아요.."