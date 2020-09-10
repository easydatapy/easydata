from easydata.loaders import ObjectLoader
from easydata.processors.data import DataJsonToDictProcessor, DataToPqProcessor


def test_object_manager():
    test_data_processors = [
        ("data_to_json", DataJsonToDictProcessor()),
        DataToPqProcessor(),
    ]

    om = ObjectLoader(test_data_processors)

    assert len(om) == 2
    assert isinstance(list(om)[0], DataJsonToDictProcessor)
    assert isinstance(list(om)[1], DataToPqProcessor)

    om.add("data_to_json2", DataJsonToDictProcessor())

    assert len(om) == 3
    assert isinstance(list(om)[2], DataJsonToDictProcessor)

    assert isinstance(om["data_to_json2"], DataJsonToDictProcessor)
    assert isinstance(om["1"], DataToPqProcessor)

    assert list(om.keys()) == ["data_to_json", "1", "data_to_json2"]

    om.del_if_exists("4")

    assert len(om) == 3

    om.del_if_exists("data_to_json2")

    assert len(om) == 2

    om.del_by_type(DataToPqProcessor)

    assert len(om) == 1

    assert isinstance(list(om)[0], DataJsonToDictProcessor)

    om.add(None, DataJsonToDictProcessor())
    om.add(None, DataJsonToDictProcessor())

    assert len(om) == 3

    om.add(None, DataJsonToDictProcessor(), unique=True)

    assert len(om) == 1

    om.add_list([DataJsonToDictProcessor(), DataJsonToDictProcessor()])

    assert len(om) == 3

    om.add(None, DataToPqProcessor())

    om.add_list([DataToPqProcessor()])

    assert len(om) == 5

    om.add_list([DataToPqProcessor(), DataJsonToDictProcessor()], unique=True)

    assert len(om) == 2
