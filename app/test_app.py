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
        # '{"links":[{"href":"http://localhost:5000/collections/","hreflang":"en","rel":"self","type":"aplication/json"}],"collections":[{"id":"isobaric","title":"IsobaricGRIB - GRIB files"...

    def test_point(self) -> None:
        # Test various coord formats, which should all work
        response = client.get(f"/collections/isobaric/position?coords=POINT(11 60)")
        self.assertEqual(response.status_code, 200)
        response = client.get(f"/collections/isobaric/position?coords=POINT(11.0 60.0)")
        self.assertEqual(response.status_code, 200)
        response = client.get(f"/collections/isobaric/position?coords=POINT(11. 60.)")
        self.assertEqual(response.status_code, 200)

        response = client.get(f"/collections/isobaric/position?{sample_coords}")
        self.assertEqual(response.status_code, 200)
        # Test for values in range -> temperature
        self.assertTrue(
            len(str(response.json()["ranges"]["temperature"]["values"][0])) > 1
        )
        # Test for values in range -> uwind
        self.assertTrue(len(str(response.json()["ranges"]["uwind"]["values"][0])) > 1)
        # Test for values in range -> vwind
        self.assertTrue(len(str(response.json()["ranges"]["vwind"]["values"][0])) > 1)
        # Test for values in domain -> z -> values
        self.assertTrue(
            len(str(response.json()["domain"]["axes"]["z"]["values"][0])) > 1
        )
        # Test for null in data
        self.assertFalse("null" in response.text)

    def test_instances(self) -> None:
        """Test a variety of URLs related to instances."""
        # Test list of instances.
        response = client.get("/collections/isobaric/instances")
        self.assertEqual(response.status_code, 200)

        # Find current instance.
        json_response = response.json()
        instance_id = json_response["instances"][0]["id"]

        # Test link to current instance.
        self.assertTrue(
            json_response["instances"][0]["links"][0]["href"]
            == f"http://localhost:5000/collections/isobaric/instances/{instance_id}/"
        )

        # Test asking for a specific instance.
        response = client.get(f"/collections/isobaric/instances/{instance_id}")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["id"] == "isobaric")
        self.assertIn(instance_id, response.json()["links"][0]["href"])

        # Test asking for non-existing instance.
        response = client.get("/collections/isobaric/instances/1234567890/")
        self.assertEqual(response.status_code, 422)

        # Test asking for data in a non-existing instance.
        response = client.get(
            f"/collections/isobaric/instances/1234567890/position?{sample_coords}"
        )
        self.assertEqual(response.status_code, 422)

        # Test asking for a sample point in current instance.
        response = client.get(
            f"/collections/isobaric/instances/{instance_id}/position?{sample_coords}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '"id":"isobaric","type":"Coverage","domain":{"type":"Domain","domainType":"VerticalProfile","axes":{"x"',
            response.text,
        )

    def test_api(self) -> None:
        response = client.get("/api")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
