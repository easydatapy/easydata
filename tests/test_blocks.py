import pytest

import easydata as ed

test_data = {
    "brand": {"name": "EasyData"},
    "name": "EB Pro 15",
    "bad_name": "EB   Pro   15",
    "price": 124.99,
    "sale_price": 99,
    "f_price": "124.99$",
    "f_sale_price": "99$",
}


@pytest.mark.parametrize(
    "block_parser_model, result",
    [
        (
            ed.BlockParserModel(
                ed.Text(uppercase=True),
                brand=ed.jp("brand.name"),
                name=ed.jp("name"),
            ),
            {
                "brand": "EASYDATA",
                "name": "EB PRO 15",
            },
        ),
        (
            ed.BlockParserModel(
                ed.Text(lowercase=True),
                query_prefix="brand.",
                brand=ed.jp("name"),
            ),
            {
                "brand": "easydata",
            },
        ),
    ],
)
def test_block_parser_model(block_parser_model, result):
    assert block_parser_model.parse_item(test_data) == result


@pytest.mark.parametrize(
    "block_simple_model, result",
    [
        (
            ed.BlockSimpleDataModel(
                name=ed.jp("name"),
                bad_name=ed.jp("bad_name"),
                brand=ed.jp("brand.name"),
            ),
            {
                "name": "EB Pro 15",
                "bad_name": "EB   Pro   15",
                "brand": "EasyData",
            },
        ),
        (
            ed.BlockSimpleDataModel(
                query_prefix="brand.",
                brand=ed.jp("name"),
            ),
            {
                "brand": "EasyData",
            },
        ),
        (
            ed.BlockSimpleTextModel(
                name=ed.jp("name"),
                bad_name=ed.jp("bad_name"),
                brand=ed.jp("brand.name"),
            ),
            {
                "name": "EB Pro 15",
                "bad_name": "EB Pro 15",
                "brand": "EasyData",
            },
        ),
        (
            ed.BlockSimpleFloatModel(
                price=ed.jp("price"),
                sale_price=ed.jp("sale_price"),
            ),
            {
                "price": 124.99,
                "sale_price": 99.0,
            },
        ),
        (
            ed.BlockSimpleIntModel(
                price=ed.jp("price"),
                sale_price=ed.jp("sale_price"),
            ),
            {
                "price": 124,
                "sale_price": 99,
            },
        ),
        (
            ed.BlockSimplePriceFloatModel(
                price=ed.jp("price"),
                sale_price=ed.jp("sale_price"),
            ),
            {
                "price": 124.99,
                "sale_price": 99.0,
            },
        ),
        (
            ed.BlockSimplePriceIntModel(
                price=ed.jp("price"),
                sale_price=ed.jp("sale_price"),
            ),
            {
                "price": 124,
                "sale_price": 99,
            },
        ),
        (
            ed.BlockSimplePriceTextModel(
                price=ed.jp("price"),
                sale_price=ed.jp("sale_price"),
            ),
            {
                "price": "124.99",
                "sale_price": "99.0",
            },
        ),
    ],
)
def test_block_simple_model(block_simple_model, result):
    assert block_simple_model.parse_item(test_data) == result
