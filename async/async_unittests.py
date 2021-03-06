from unittest import TestCase, main
from unittest.mock import Mock, call, patch

from asyncio import get_event_loop

from testasync import AsyncClass


def AsyncMock(*args, **kwargs):
    m = Mock(*args, **kwargs)

    async def mock_coroutine(*args, **kwargs):
        return m(*args, **kwargs)

    mock_coroutine.mock = m
    return mock_coroutine()


def _run(coro):
    return get_event_loop().run_until_complete(coro)


class AsyncClassTests(TestCase):
    @patch(f"testasync.ThreadPoolExecutor.__enter__")
    @patch(f"testasync.gather")
    @patch(f"testasync.get_event_loop")
    def test_collect_urls(self, mock_event_loop, mock_gather, mock_executor):
        mock_gather.side_effect = AsyncMock
        mock_event_loop.return_value.run_in_executor.side_effect = ["task1", "task2", "task3", "task4"]

        mock_self = Mock()
        mock_self.repeat = 2
        mock_self._collect_urls = Mock()

        _run(AsyncClass._collect_urls(mock_self, ["https://url.com", "https://url2.com"]))

        mock_event_loop.return_value.run_in_executor.assert_has_calls([
            call(mock_executor.return_value, mock_self._call_url, "https://url.com", 0),
            call(mock_executor.return_value, mock_self._call_url, "https://url.com", 1),
            call(mock_executor.return_value, mock_self._call_url, "https://url2.com", 0),
            call(mock_executor.return_value, mock_self._call_url, "https://url2.com", 1)
        ])
        mock_gather.assert_called_once_with("task1", "task2", "task3", "task4")


if __name__ == '__main__':
    main()
