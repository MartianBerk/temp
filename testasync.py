import requests

from asyncio import coroutine, ensure_future, gather, get_event_loop
from concurrent.futures import ThreadPoolExecutor


class AsyncClass:
    def __init__(self, urls, repeat=2):
        self.urls = urls
        self.repeat = repeat

        self.response = 0

    @coroutine
    async def _collect_urls(self, urls):
        with ThreadPoolExecutor(max_workers=20) as executor:
            loop = get_event_loop()
            tasks = [
                loop.run_in_executor(executor, self._call_url, u, i)
                for u in urls
                    for i in range(self.repeat)
            ]

            await gather(*tasks)

    def _call_url(self, url, n):
        try:
            response = requests.get(url)
            print(f"{url}:[{n}] returned {response.status_code}")
            self.response += 1
        except Exception:
            print(f"--ISSUE WITH {url}:[{n}]--")

        return True

    def main(self):
        loop = get_event_loop()
        future = ensure_future(self._collect_urls(self.urls))
        loop.run_until_complete(future)

        print(f"called {self.response} urls")


if __name__ == "__main__":
    urls = [
        "https://www.google.co.uk",
        "https://www.facebook.com",
        "https://www.twitter.com",
        "https://www.bbc.co.uk",
        "https://www.skysports.com"
    ]

    asy = AsyncClass(urls, repeat=10)
    asy.main()
