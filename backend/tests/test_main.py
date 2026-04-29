import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app


class FakeConnection:
    def __init__(self, rows):
        self._rows = rows

    async def fetch(self, _query, *_args):
        return self._rows

    async def fetchrow(self, _query, *_args):
        if self._rows:
            return self._rows[0]
        return None


class FakeContextManager:
    def __init__(self, rows):
        self._conn = FakeConnection(rows)

    async def __aenter__(self):
        return self._conn

    async def __aexit__(self, exc_type, exc, tb):
        return False


class FailingContextManager:
    async def __aenter__(self):
        raise RuntimeError("db down")

    async def __aexit__(self, exc_type, exc, tb):
        return False


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.sample = [{
            "id": "x1", "title": "Licitación SEO", "description": "Servicio SEO",
            "cpv_code": "79342000", "score": 88, "priority": "top", "status": "Nueva",
            "budget": 10000, "deadline_at": None, "source_url": "https://example.com"
        }]

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Panel MVP", response.text)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)

    @patch("app.main.get_connection")
    def test_tenders(self, mock_get_connection: AsyncMock):
        mock_get_connection.return_value = FakeContextManager(self.sample)
        response = self.client.get("/tenders?status=Nueva&priority=top&min_score=70&limit=10&offset=0")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total"], 1)

    @patch("app.main.get_connection")
    def test_update_status(self, mock_get_connection: AsyncMock):
        updated = [dict(self.sample[0], status="Presentada")]
        mock_get_connection.return_value = FakeContextManager(updated)
        response = self.client.patch("/tenders/x1/status", json={"status": "Presentada"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "Presentada")

    @patch("app.main.get_connection")
    def test_tenders_db_unavailable(self, mock_get_connection: AsyncMock):
        mock_get_connection.return_value = FailingContextManager()
        response = self.client.get("/tenders")
        self.assertEqual(response.status_code, 503)


if __name__ == "__main__":
    unittest.main()
