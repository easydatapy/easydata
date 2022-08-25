import json

from easydata.contrib.requests.utils import response_to_data_bag
from tests.factory.requests import fake_response


def test_response_to_data_bag():
    data = response_to_data_bag(fake_response(text=json.dumps({"name": "Easybook 15"})))

    assert json.loads(data["main"]) == {"name": "Easybook 15"}


def test_response_to_data_bag_with_to_json():
    data = response_to_data_bag(
        fake_response(text=json.dumps({"name": "Easybook 15"})),
        to_json=True,
    )

    assert data["main"] == {"name": "Easybook 15"}


def test_response_to_data_bag_with_cb_kwargs():
    data = response_to_data_bag(
        fake_response(text=json.dumps({"name": "Easybook 15"})),
        brand_info={"name": "EasyData"},
        empty_info=None,
    )

    assert json.loads(data["main"]) == {"name": "Easybook 15"}

    assert data["brand_info"] == {"name": "EasyData"}

    assert data["empty_info"] is None
