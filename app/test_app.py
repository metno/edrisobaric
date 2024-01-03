import unittest
import os
from datetime import datetime
import uvicorn
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


class TestApp(unittest.TestCase):
    def test_read_main(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("EDR isobaric from Grib", response.text)


if __name__ == "__main__":
    unittest.main()
