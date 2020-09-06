import json
import os

from pyquery import PyQuery

from easydata.data import DataBag

html_path = os.path.join(os.path.dirname(__file__), "html")
json_path = os.path.join(os.path.dirname(__file__), "json")


def get_html_filepath(file_name):
    return __get_filepath(html_path, file_name, "html")


def get_json_filepath(file_name):
    return __get_filepath(json_path, file_name, "json")


def load_html_text(file_name):
    filepath = get_html_filepath(file_name)

    with open(filepath, "r") as html_file:
        return html_file.read()


def load_json_text(file_name):
    filepath = get_json_filepath(file_name)

    with open(filepath, "r") as html_file:
        return html_file.read()


def load_html_with_pq(file_name):
    html_text = load_html_text(file_name)

    return PyQuery(html_text)


def load_json(file_name):
    json_text = load_json_text(file_name)

    return json.loads(json_text)


def load_data_bag_with_html_text(file_name):
    html_text = load_html_text(file_name)

    return DataBag(None, data=html_text)


def load_data_bag_with_pq(file_name):
    pq = load_html_with_pq(file_name)

    return DataBag(None, data=pq)


def load_data_bag_with_json(file_name):
    json_text = load_json(file_name)

    return DataBag(None, data=json_text)


def __get_filepath(path, file_name, ext):
    return "{}.{}".format(os.path.join(path, file_name), ext)
