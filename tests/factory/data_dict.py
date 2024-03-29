import json

item_with_options = {
    "id": 123,
    "url_path": "easybook-pro-15",
    "title": "EasyBook pro 15",
    "info": {"name": "EasyBook pro 15"},
    "brand": {"name": "EasyData", "origin": "Slovenia"},
    "price": 99.99,
    "sale_price": 49.99,
    "color": "",
    "multi": False,
    "in_stock": True,
    "name_key": "name",
    "option_name_contains": "Moni",
    "image_data": [
        {"zoom": "https://demo.com/img1.jpg"},
        {"zoom": "https://demo.com/img2.jpg"},
    ],
    "images": [
        "https://demo.com/img1.jpg",
        "https://demo.com/img2.jpg",
        "https://demo.com/img3.jpg",
    ],
    "options": [
        {
            "name": "Monitor",
            "availability": {"value": "yes"},
            "quantity": "3 units",
        },
        {
            "name": "Mouse",
            "availability": {"value": "no"},
            "quantity": "no units",
        },
    ],
}

item_with_options_text = json.dumps(item_with_options)

variants_data = {
    "id": 123,
    "title": "EasyData Pro 13",
    "variants": [
        {"color": "Black", "stock": True},
        {"color": "Gray", "stock": False},
    ],
}

variants_data_multi = {
    "data": {
        "id": 123,
        "title": "EasyData Pro",
        "variants": [
            {"color": "Black", "size": "13", "stock": True},
            {"color": "Black", "size": "15", "stock": True},
            {"color": "Gray", "size": "13", "stock": False},
            {"color": "Gray", "size": "15", "stock": True},
        ],
    }
}

variants_data_multi_complex = {
    "id": 123,
    "title": "EasyData Pro",
    "images": {
        "Black": [{"assetId": "33019_B_PRIMARY"}, {"assetId": "33020_B_ALT1"}],
        "Gray": [{"assetId": "33021_G_PRIMARY"}, {"assetId": "33022_G_ALT2"}],
    },
    "stock_data": [
        {"id": 1, "stock": True},
        {"id": 2, "stock": True},
        {"id": 3, "stock": False},
        {"id": 4, "stock": True},
    ],
    "variants": [
        {"color": "Black", "size": "13", "stock_id": 1},
        {"color": "Black", "size": "15", "stock_id": 2},
        {"color": "Gray", "size": "13", "stock_id": 3},
        {"color": "Gray", "size": "15", "stock_id": 4},
    ],
}

multi_items = {
    "data": {
        "items": [
            {
                "id": 1,
                "title": "EasyData Pro",
                "variants": [
                    {"color": "Black", "size": "13", "stock": True},
                    {"color": "Black", "size": "15", "stock": True},
                    {"color": "Gray", "size": "13", "stock": False},
                    {"color": "Gray", "size": "15", "stock": True},
                ],
            },
            {
                "id": 2,
                "title": "EasyPod",
                "variants": [
                    {"color": "Black", "size": "8", "stock": True},
                    {"color": "Gray", "size": "8", "stock": False},
                    {"color": "Gray", "size": "10", "stock": True},
                ],
            },
        ]
    }
}

sizes = {"sizes": {"l": True, "xl": False, "xxl": True}}

title = {"title": "Easybook Pro 13"}

name = {"name": "EasyCELL 15"}

stock = {"stock": True}

images = {
    "images": [
        {"src": "https://demo.com/imgs/1.jpg"},
        {"src": "https://demo.com/imgs/2.jpg"},
        {"src": "https://demo.com/imgs/3.jpg"},
    ]
}
