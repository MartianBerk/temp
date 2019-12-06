from unittest import TestCase, main
from unittest.mock import Mock, call, patch

from asyncio import get_event_loop

from async import AsyncClass


def AsyncMock(*args, **kwargs):
    m = Mock(*args, **kwargs)

    async def mock_coroutine(*args, **kwargs):
        return m(*args, **kwargs)

    mock_coroutine.mock = m
    return mock_coroutine()


def _run(coro):
    return get_event_loop().run_until_complete(coro)


class AsyncClassTests(TestCase):
    @patch(f"async.ThreadPoolExecutor.__enter__")
    @patch(f"async.gather")
    @patch(f"async.get_event_loop")
    def test_collect_urls(self, mock_event_loop, mock_gather, mock_executor):
        mock_gather.side_effect = AsyncMock
        mock_event_loop.return_value.run_in_executor.side_effect = ["task1", "task2"]

        mock_self = Mock()
        mock_self._collect_urls = Mock()

        _run(AsyncClass._collect_urls(mock_self, ["https://url.com", "https://url2.com"]))

        mock_event_loop.return_value.run_in_executor.assert_has_calls([
            call(mock_executor.return_value, mock_self._call_url, "https://url.com"),
            call(mock_executor.return_value, mock_self._call_url, "https://url2.com")
        ])
        mock_gather.assert_called_once_with("task1", "task2")


if __name__ == '__main__':
    main()
