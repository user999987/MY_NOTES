Django how to patch and mock 
```python
from django import urls
from django.test import TestCase, override_settings
from mock import patch
from rest_framework.test import APIClient
from common.logger import logger
from insula.core.tier.services.address_services import get_info_for_zip_code
from insula.core.tier.models import DeliveryTier
from insula.core.tier.views import GetZIPCodeInfoView
from insula.geocoder.tests.geocoder_mock import OFFICE_LOCATION
from insula.tiers_and_zones.geoshapes.test.zip_code_mock import OFFICE_LOCATION_ZIPCODE


class TestGetZIPCodeInfoView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.make_client()


    @classmethod
    def make_client(cls):
        cls._client = APIClient()

    @classmethod
    def get(cls, view_name, kwargs={}, query_params={}):
        url = urls.reverse(view_name, kwargs=kwargs)
        return cls._client.get(
            url,
            query_params,
            content_type='application/json',
            accept='application/json',
        )

    # case 1: not deliverable, no zipcode info in DB, no geo result
    @patch('insula.core.tier.services.address_services.geocode')
    @patch('insula.core.tier.services.address_services.ZipCode')
    def test_get_geocode_null(self, zipCodeObj, geocode):
        geocode.return_value = None
        zipCodeObj.objects.filter.return_value.first.return_value = None

        return_result = self.get("core:get_zip_code_info", kwargs={"zip_code": 10001})

        self.assertEqual(return_result.data['is_deliverable'],False)
        self.assertEqual(return_result.data['latitude'],90.0)
        self.assertEqual(return_result.data['longitude'],0.0)

    # case 2:deliverable and zipcode found in Db, tier object is in cache
    @patch('insula.core.tier.services.address_services.caches')
    @patch('insula.core.tier.services.address_services.ZipCode')
    def test_get_zipcode_found_in_DB(self, zipCodeObj, caches):
        caches['tier_cache'].get.return_value = DeliveryTier(name='T1', facility_id=1, is_active=True, id=36)
        # DeliveryTierObj.objects.filter.return_value.first.return_value = DeliveryTier(name='T1', facility_id=1, is_active=True, id=36)
        zipCodeObj.objects.filter.return_value.first.return_value = OFFICE_LOCATION_ZIPCODE

        return_result = self.get("core:get_zip_code_info", kwargs={"zip_code": 10001})
        tier, zip_geo = get_info_for_zip_code("10001")
        logger.info("unit test:", extra={
            'return_result': return_result.data,
            'tier': tier,
            'zip_geo': zip_geo,
        })

        self.assertEqual(return_result.data['is_deliverable'], True)
        self.assertEqual(return_result.data['latitude'], 40.7483005)
        self.assertEqual(return_result.data['longitude'], -73.99065499999999)

    # case 3: not deliverable and zipcode not found in Db, but get geo info from gmaps
    @patch('insula.core.tier.services.address_services.geocode')
    @patch('insula.core.tier.services.address_services.ZipCode')
    @patch('insula.core.tier.services.address_services.DeliveryTier')
    def test_get_zipcode_info_from_gmaps(self, deliveryTierObj, zipCodeObj, geocode):
        geocode.return_value = OFFICE_LOCATION
        # DeliveryTierObj.objects.filter.return_value.first.return_value = DeliveryTier(name='T1', facility_id=1, is_active=True, id=36)
        zipCodeObj.objects.filter.return_value.first.return_value = None
        deliveryTierObj.objects.filter.return_value.first.return_value = None

        return_result = self.get("core:get_zip_code_info", kwargs={"zip_code": 10001})
        tier, zip_geo = get_info_for_zip_code("10001")
        logger.info("unit test:", extra={
            'return_result': return_result.data,
            'tier': tier,
            'zip_geo': zip_geo,
        })

        self.assertEqual(return_result.data['is_deliverable'], False)
        self.assertEqual(return_result.data['latitude'], 40.7483005)
        self.assertEqual(return_result.data['longitude'], -73.99065499999999)

```