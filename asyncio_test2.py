import asyncio
import time

async def sleep(sec):
    await loop.run_in_executor(None, time.sleep, sec)  # time.sleep(sec)
    return sec

async def main():
    sec_list = [1, 2]
    tasks = [asyncio.create_task(sleep(sec)) for sec in sec_list]  # [Task 1 객체, Task 2 객체]
    print(tasks)
    tasks_results = await asyncio.gather(*tasks)  # [Task 1 객체의 결과 값, Task 2 객체의 결과 값]
    return tasks_results

start = time.time()

loop = asyncio.get_event_loop()
result = loop.run_until_complete(main())
loop.close()

end = time.time()

print('result : {}'.format(result))
print('total time : {0:.2f} sec'.format(end - start))