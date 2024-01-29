"""Mostly to check all URLs reply without crash after code changes."""

import unittest
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)
sample_coords = "coords=POINT(11.9384 60.1699)"


class TestApp(unittest.TestCase):
    def test_landingpage(self) -> None:
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("EDR isobaric from Grib", response.text)

    def test_conformance(self) -> None:
        response = client.get("/conformance")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "http://www.opengis.net/spec/ogcapi-edr-1/1.0/conf/core" in response.text,
        )

    def test_collections(self) -> None:
        response = client.get("/collections")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["collections"][0]["id"] == "isobaric")

    def test_point(self) -> None:
        # Test various coord formats, which should all work
        response = client.get("/collections/isobaric/position?coords=POINT(11 60)")
        self.assertEqual(response.status_code, 200)
        response = client.get("/collections/isobaric/position?coords=POINT(11.0 60.0)")
        self.assertEqual(response.status_code, 200)
        response = client.get("/collections/isobaric/position?coords=POINT(11. 60.)")
        self.assertEqual(response.status_code, 200)

        response = client.get(f"/collections/isobaric/position?{sample_coords}")
        self.assertEqual(response.status_code, 200)
        # Test for values in range -> temperature
        self.assertTrue(
            len(str(response.json()["ranges"]["temperature"]["values"][0])) > 1
        )
        # Test for values in range -> wind_from_direction
        self.assertTrue(
            len(str(response.json()["ranges"]["wind_from_direction"]["values"][0])) > 1
        )
        # Test for values in range -> wind_speed
        self.assertTrue(
            len(str(response.json()["ranges"]["wind_speed"]["values"][0])) > 1
        )
        # Test for values in domain -> z -> values
        self.assertTrue(
            len(str(response.json()["domain"]["axes"]["z"]["values"][0])) > 1
        )
        # Test for null in data
        self.assertFalse("null" in response.text)

        # Test URL that shouldn't work
        response = client.get("/collections/isobaric/position?coords=POINT(1160)")
        self.assertEqual(response.status_code, 422)

        # Test redirect (can't test in normal way, as this isn't run on a webserver)
        response = client.get("/collections/isobaric/")
        self.assertEqual(response.status_code, 200)

    def test_api(self) -> None:
        response = client.get("/api", follow_redirects=False)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
