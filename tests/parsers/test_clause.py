from easydata import parsers
from easydata.queries import jp, pq
from tests import factory

db = factory.load_data_bag_with_pq("product")


def test_union():
    test_html = """
        <p class="brand">EasyData</p>
    """

    union_parser = parsers.Union(
        parsers.Text(pq(".brand-wrong::text")),
        parsers.Text(pq(".brand::text")),
    )
    assert union_parser.parse(test_html) == "EasyData"


def test_union_first():
    test_html = """
        <p class="brand">EasyData</p>
        <p id="name">Easybook Pro 13</p>
    """

    union_parser = parsers.Union(
        parsers.Text(pq(".brand::text")),
        parsers.Text(pq("#name::text")),
    )
    assert union_parser.parse(test_html) == "EasyData"


def test_union_none():
    test_html = """
        <p class="brand">EasyData</p>
    """

    union_parser = parsers.Union(
        parsers.Text(pq(".brand-wrong::text")),
        parsers.Text(pq(".brand-wrong-again::text")),
    )
    assert union_parser.parse(test_html) is None


def test_with():
    test_html = """
        <div id="description">
            <ul class="features">
                <li>Material: aluminium <span>MATERIAL</span></li>
                <li>style: <strong>elegant</strong> is this</li>
                <li>Date added: Fri, 12 Dec 2018 10:55</li>
            </ul>
        </div>
    """

    with_parser = parsers.With(
        parsers.Sentences(pq("#description .features::text"), allow=["date added"]),
        parsers.DateTimeSearch(),
    )
    assert with_parser.parse(test_html) == "12/12/2018 10:55:00"

    with_parser = parsers.With(
        parsers.Sentences(pq("#description .features::text"), allow=["date added"]),
        parsers.Text(split_key=("added:", -1)),
        parsers.DateTime(),
    )
    assert with_parser.parse(test_html) == "12/12/2018 10:55:00"


def test_join_text():
    test_html = """
        <p class="brand">EasyData</p>
        <p id="name">Easybook Pro 13</p>
    """

    join_text_parser = parsers.JoinText(
        parsers.Text(pq(".brand::text")), parsers.Text(pq("#name::text"))
    )
    assert join_text_parser.parse(test_html) == "EasyData Easybook Pro 13"

    join_text_parser = parsers.JoinText(
        parsers.Text(pq(".brand-wrong-selector::text")), parsers.Text(pq("#name::text"))
    )
    assert join_text_parser.parse(test_html) == "Easybook Pro 13"


def test_join_text_custom_separator():
    test_html = """
        <p class="brand">EasyData</p>
        <p id="name">Easybook Pro 13</p>
    """

    join_text_parser = parsers.JoinText(
        parsers.Text(pq(".brand::text")), parsers.Text(pq("#name::text")), separator="-"
    )
    assert join_text_parser.parse(test_html) == "EasyData-Easybook Pro 13"


def test_join_list():
    test_dict = {"features": ["gold color", "retina"], "specs": ["i7 proc", "16 gb"]}

    join_list_parser = parsers.JoinList(
        parsers.List(jp("features"), parser=parsers.Text()),
        parsers.List(jp("specs"), parser=parsers.Text()),
    )

    expected_result = ["gold color", "retina", "i7 proc", "16 gb"]
    assert join_list_parser.parse(test_dict) == expected_result


def test_join_dict():
    test_dict = {
        "features": {"color": "gold", "display": "retina"},
        "specs": {"proc": "i7", "ram": "16 gb"},
    }

    join_dict_parser = parsers.JoinDict(
        parsers.Dict(
            jp("features"), key_parser=parsers.Text(), value_parser=parsers.Text()
        ),
        parsers.Dict(
            jp("specs"), key_parser=parsers.Text(), value_parser=parsers.Text()
        ),
    )

    expected_result = {
        "color": "gold",
        "display": "retina",
        "proc": "i7",
        "ram": "16 gb",
    }
    assert join_dict_parser.parse(test_dict) == expected_result
