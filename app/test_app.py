"""Mostly to check all URLs reply without crash after code changes."""

import unittest
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)
sample_coords = "coords=POINT(11.9384 60.1699)"


class TestApp(unittest.TestCase):
    def test_landingpage(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("EDR isobaric from Grib", response.text)

    def test_conformance(self):
        response = client.get("/conformance")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '{"conformsTo":["http://www.opengis.net/spec/ogcapi-common-1/1.0/conf/core",',
            response.text,
        )

    def test_collections(self):
        response = client.get("/collections")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '{"links":[{"href":"http://localhost:5000/","hreflang":"en","rel":"self","type":"aplication/json"}],"collections":[{"id":"isobaric","title":"',
            response.text,
        )

    def test_point(self):
        response = client.get(f"/collections/position?{sample_coords}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '"vertical":{"interval":[["850.0"],["100.0"]],"values":["850.0","750.0","700.0","600.0","500.0","450.0","400.0","350.0","300.0","275.0","250.0","225.0","200.0","150.0","100.0"],"vrs":"Vertical Reference System: PressureLevel"}},',
            response.text,
        )

    def test_instances(self):
        response = client.get("/collections/isobaric/instances")
        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        instance_id = json_response["instances"][0]["id"]

        self.assertIn(
            f"http://localhost:5000/collections/isobaric/instances/{instance_id}/position",
            response.text,
        )

        # Test instance
        response = client.get("/collections/isobaric/instances/{instance_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '"id":"isobaric","title":"',
            response.text,
        )

        # Test a point in instance
        response = client.get(
            f"/collections/isobaric/instances/{instance_id}/position?{sample_coords}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '"id":"isobaric","type":"Coverage","domain":{"type":"Domain","domainType":"VerticalProfile","axes":{"x":{"values',
            response.text,
        )


if __name__ == "__main__":
    unittest.main()
