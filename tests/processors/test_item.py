import pytest

from easydata import processors


def test_item_merge_into_list_processor():
    test_item = {"category": "electronics", "subcategory": "phones"}

    item = processors.ItemKeysMergeIntoListProcessor(
        new_item_key="breadcrumbs", item_keys=["category", "subcategory"]
    ).parse(test_item)

    assert item["breadcrumbs"] == ["electronics", "phones"]

    # test that old parsers have been removed
    assert all(k not in item for k in ["category", "subcategory"])


def test_item_merge_into_list_processor_preserve_original():
    test_item = {"category": "electronics", "subcategory": "phones"}

    item = processors.ItemKeysMergeIntoListProcessor(
        new_item_key="breadcrumbs",
        item_keys=["category", "subcategory"],
        preserve_original=True,
    ).parse(test_item)

    assert item["breadcrumbs"] == ["electronics", "phones"]

    # test that old parsers remain
    assert all(k in item for k in ["category", "subcategory"])


def test_item_merge_into_list_processor_ignore_none():
    test_item = {"category": "electronics", "subcategory": "phones", "type": None}

    item = processors.ItemKeysMergeIntoListProcessor(
        new_item_key="breadcrumbs", item_keys=["category", "subcategory", "type"]
    ).parse(test_item)

    assert item["breadcrumbs"] == ["electronics", "phones"]


def test_item_merge_into_list_processor_ignore_none_false():
    test_item = {"category": "electronics", "subcategory": "phones", "type": None}

    item = processors.ItemKeysMergeIntoListProcessor(
        new_item_key="breadcrumbs",
        item_keys=["category", "subcategory", "type"],
        ignore_none=False,
    ).parse(test_item)

    assert item["breadcrumbs"] == ["electronics", "phones", None]


def test_item_merge_into_list_processor_wrong_field_exception():
    test_item = {"category": "electronics", "subcategory": "phones"}

    with pytest.raises(KeyError):
        processors.ItemKeysMergeIntoListProcessor(
            new_item_key="breadcrumbs", item_keys=["category", "subcategory", "type"]
        ).parse(test_item)


def test_item_merge_into_dict_processor():
    test_item = {"category": "electronics", "subcategory": "phones"}

    item = processors.ItemKeysMergeIntoDictProcessor(
        new_item_key="breadcrumbs", item_keys=["category", "subcategory"]
    ).parse(test_item)

    assert item["breadcrumbs"] == {"category": "electronics", "subcategory": "phones"}


def test_item_merge_processor():
    test_item = {"category": "electronics", "subcategory": "phones"}

    item = processors.ItemKeysMergeProcessor(
        new_item_key="breadcrumbs", item_keys=["category", "subcategory"]
    ).parse(test_item)

    assert item["breadcrumbs"] == "electronics phones"


def test_item_merge_processor_custom_separator():
    test_item = {"category": "electronics", "subcategory": "phones"}

    item = processors.ItemKeysMergeProcessor(
        new_item_key="breadcrumbs",
        item_keys=["category", "subcategory"],
        separator=" > ",
    ).parse(test_item)

    assert item["breadcrumbs"] == "electronics > phones"


def test_item_merge_processor_preserve_original():
    test_item = {"category": "electronics", "subcategory": "phones"}

    item = processors.ItemKeysMergeProcessor(
        new_item_key="breadcrumbs",
        item_keys=["category", "subcategory"],
        separator=" > ",
        preserve_original=True,
    ).parse(test_item)

    assert item["breadcrumbs"] == "electronics > phones"

    # test that old parsers remain
    assert all(k in item for k in ["category", "subcategory"])


def test_item_to_str_processor():
    test_item = {"price": 19.99, "price_int": 22, "price_none": None}

    item = processors.ItemValueToStrProcessor(
        item_keys=["price", "price_int", "price_none"]
    ).parse(test_item)

    assert item == {"price": "19.99", "price_int": "22", "price_none": ""}


def test_item_to_str_processor_none_as_empty_string_false():
    test_item = {"price_none": None}

    item = processors.ItemValueToStrProcessor(
        item_keys=["price_none"], none_as_empty_string=False
    ).parse(test_item)

    assert item == {"price_none": None}


def test_item_remove_processor():
    test_item = {"price": 19.99, "price_int": 22, "price_none": None}

    item = processors.ItemRemoveKeysProcessor(item_keys=["price", "price_none"]).parse(
        test_item
    )

    assert item == {"price_int": 22}


@pytest.mark.parametrize(
    "price, sale_price, result",
    [
        (29.99, 21.99, 26.68),
        ("29.99", "21.99", 26.68),
        ("29.99", 22, 26.64),
    ],
)
def test_item_discount_processor(price, sale_price, result):

    test_item = {"price": price, "sale_price": sale_price}

    item = processors.ItemDiscountProcessor().parse(test_item)

    assert item["discount"] == result


def test_item_discount_processor_custom_keys():
    test_item = {"old_price": "29.99", "price": 22}

    item = processors.ItemDiscountProcessor(
        item_price_key="old_price",
        item_sale_price_key="price",
        item_discount_key="pdiscount",
    ).parse(test_item)

    expected_result = {"old_price": "29.99", "price": 22, "pdiscount": 26.64}
    assert item == expected_result


def test_item_discount_processor_custom_keys_config():
    test_item = {"old_price": "29.99", "price": 22}

    # Test config setting
    config_params = {
        "ED_ITEM_DISCOUNT_ITEM_PRICE_KEY": "old_price",
        "ED_ITEM_DISCOUNT_ITEM_SALE_PRICE_KEY": "price",
        "ED_ITEM_DISCOUNT_ITEM_DISCOUNT_KEY": "pdiscount",
    }

    discount_processor = processors.ItemDiscountProcessor()
    discount_processor.init_config(config_params)

    item = discount_processor.parse(test_item)

    expected_result = {"old_price": "29.99", "price": 22, "pdiscount": 26.64}
    assert item == expected_result


@pytest.mark.parametrize(
    "price, sale_price, decimals, result",
    [
        (29.99, 21.99, 1, 26.7),
        (29.99, 21.99, 4, 26.6756),
    ],
)
def test_item_discount_processor_decimals(price, sale_price, decimals, result):

    test_item = {"price": price, "sale_price": sale_price}

    item = processors.ItemDiscountProcessor(decimals=decimals).parse(test_item)

    assert item["discount"] == result


def test_item_discount_processor_decimals_config():
    test_item = {"price": 29.99, "sale_price": 21.99}

    discount_processor = processors.ItemDiscountProcessor()
    discount_processor.init_config({"ED_ITEM_DISCOUNT_DECIMALS": 4})

    item = discount_processor.parse(test_item)

    assert item["discount"] == 26.6756


def test_item_discount_processor_no_decimals():
    test_item = {"price": 29.99, "sale_price": 21.99}

    item = processors.ItemDiscountProcessor(no_decimals=True).parse(test_item)

    assert item["discount"] == 27


def test_item_discount_processor_no_decimals_config():
    test_item = {"price": 29.99, "sale_price": 21.99}

    discount_processor = processors.ItemDiscountProcessor()
    discount_processor.init_config({"ED_ITEM_DISCOUNT_NO_DECIMALS": True})

    item = discount_processor.parse(test_item)

    assert item["discount"] == 27


def test_item_discount_processor_remove_item_sale_price_key():
    test_item = {"price": 29.99, "sale_price": 21.99}

    item = processors.ItemDiscountProcessor(remove_item_sale_price_key=True).parse(
        test_item
    )

    assert item == {"price": 29.99, "discount": 26.68}


def test_item_discount_processor_remove_item_sale_price_key_config():
    test_item = {"price": 29.99, "sale_price": 21.99}

    discount_processor = processors.ItemDiscountProcessor()

    custom_config = {"ED_ITEM_DISCOUNT_REMOVE_ITEM_SALE_PRICE_KEY": True}
    discount_processor.init_config(custom_config)

    item = discount_processor.parse(test_item)

    assert item == {"price": 29.99, "discount": 26.68}
