import requests

from asyncio import coroutine, ensure_future, gather, get_event_loop
from concurrent.futures import ThreadPoolExecutor


class AsyncClass:
    def __init__(self, urls):
        self.urls = urls

        self.response = []

    @coroutine
    async def _collect_urls(self, urls):
        with ThreadPoolExecutor(max_workers=3) as executor:
            loop = get_event_loop()
            tasks = [
                loop.run_in_executor(executor, self._call_url, u) for u in urls
            ]

            await gather(*tasks)

    def _call_url(self, url):
        print(f"calling {url}...")
        try:
            response = requests.get(url)
            self.response.append(f"{url} returned {response.status_code}")
        except Exception:
            print(f"--ISSUE WITH {url}--")

        return True

    def main(self):
        loop = get_event_loop()
        future = ensure_future(self._collect_urls(self.urls))
        loop.run_until_complete(future)

        for response in self.response:
            print(response)

        print("done")


if __name__ == "__main__":
    urls = [
        "https://www.google.co.uk",
        "https://www.facebook.com",
        "https://www.twitter.com",
        "https://www.bbc.co.uk",
        "https://www.skysports.com"
    ]

    asy = AsyncClass(urls)
    asy.main()
