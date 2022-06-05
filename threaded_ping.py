from concurrent import futures
import requests
import time
import threading

local = threading.local()

def get(url: str):
    if not hasattr(local, "session"):
        local.session = requests.Session()
    session: requests.Session = local.session
    
    with session.get(url) as response:
        return url, response.elapsed.microseconds / 1000

def get_pings(urls, max_workers):
    with futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
        elapsed = pool.map(get, urls)
    return {url: el for url, el in elapsed}


if __name__ == "__main__":
    urls = [
        "https://google.com",
        "https://yahoo.com",
        "https://wikipedia.com",
        "https://www.pythonlikeyoumeanit.com/",
        "https://aslvrstn.com/",
        "https://www.smithfieldfoods.com/",
        "https://www.t-sg.jp/en/",
    ]
    start = time.time()
    res = get_pings(urls, max_workers=10)
    end = time.time()

    print(res)
    print(
        f"Got {len(urls)} pings in {end-start}s.\nSum of elapsed (s): {sum(res.values())/1000}\nMax elapsed (s): {max(res.values())/1000}"
    )
