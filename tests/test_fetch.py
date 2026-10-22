import unittest
from unittest.mock import AsyncMock, patch

import httpx
from jihed_skills_mcp import server


class FetchContractTests(unittest.IsolatedAsyncioTestCase):
    async def directory_response(self, response):
        client = AsyncMock()
        client.get.return_value = response
        with patch.object(server.httpx, "AsyncClient") as factory:
            factory.return_value.__aenter__.return_value = client
            return await server.fetch_directory("domain")

    async def test_directory_list_is_returned(self):
        response = httpx.Response(200, json=[{"name": "demo", "type": "dir"}])
        self.assertEqual(await self.directory_response(response), [{"name": "demo", "type": "dir"}])

    async def test_file_response_is_not_a_directory(self):
        self.assertEqual(await self.directory_response(httpx.Response(200, json={"type": "file"})), [])

    async def test_rate_limit_returns_empty(self):
        self.assertEqual(await self.directory_response(httpx.Response(403)), [])

    async def test_invalid_json_returns_empty(self):
        for content in (b"not JSON", b"", b"\xff"):
            with self.subTest(content=content):
                self.assertEqual(await self.directory_response(httpx.Response(200, content=content)), [])

    async def test_network_failure_returns_empty(self):
        client = AsyncMock()
        client.get.side_effect = httpx.ConnectError("synthetic offline error")
        with patch.object(server.httpx, "AsyncClient") as factory:
            factory.return_value.__aenter__.return_value = client
            self.assertEqual(await server.fetch_directory("domain"), [])

    async def test_raw_text_is_returned_verbatim(self):
        text = "---\ntitle: Exemple\n---\nÉcriture synthétique\n"
        client = AsyncMock()
        client.get.return_value = httpx.Response(200, text=text)
        with patch.object(server.httpx, "AsyncClient") as factory:
            factory.return_value.__aenter__.return_value = client
            self.assertEqual(await server.fetch_raw("domain/skill/SKILL.md"), text)
            client.get.assert_awaited_once_with(server.RAW_BASE_URL + "/domain/skill/SKILL.md")


if __name__ == "__main__":
    unittest.main()
