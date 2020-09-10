from collections import OrderedDict
from typing import Any, List, Optional, Union


class ObjectLoader(object):
    _total_object_count = 0

    def __init__(
        self,
        objects: Optional[List[Any]] = None,
        unique: bool = False,
    ):

        self._objects: OrderedDict = OrderedDict()

        if objects:
            self.add_list(objects, unique)

    def __iter__(self):
        yield from self.values()

    def __repr__(self):
        return self._objects.__repr__()

    def __len__(self):
        return len(self._objects)

    def __setitem__(
        self,
        key: Optional[Union[str, int]],
        value: Any,
    ):

        self.add(key, value)

    def __getitem__(self, key):
        return self._objects[key]

    def values(self):
        yield from self._objects.values()

    def keys(self):
        yield from self._objects.keys()

    def items(self):
        yield from self._objects.items()

    def add(
        self,
        key: Optional[Union[str, int]],
        value: Any,
        unique: bool = False,
    ):

        if key is None:
            key = str(self._total_object_count)

        if value is None:
            self.del_if_exists(key)
        else:
            if unique:
                object_type = type(value)

                self.del_by_type(object_type)

            self._objects[key] = value

            self._total_object_count += 1

    def add_list(
        self,
        objects: List[Any],
        unique: bool = False,
    ):

        for obj in objects:
            if isinstance(obj, tuple):
                key, value = obj
            else:
                key, value = None, obj

            self.add(key, value, unique)

    def add_unique(
        self,
        key: Optional[Union[str, int]],
        value: Any,
    ):

        self.add(key, value, True)

    def add_unique_list(self, objects: List[Any]):
        self.add_list(objects, True)

    def del_if_exists(self, key):
        key = str(key)

        if key in self._objects:
            del self._objects[key]

    def del_by_type(self, object_type: Any):
        keys_to_delete = []

        for key, value in self._objects.items():
            if isinstance(value, object_type):
                keys_to_delete.append(key)

        for key_to_delete in keys_to_delete:
            del self._objects[key_to_delete]

    def del_by_type_list(self, object_type_list: List[Any]):
        for object_type in object_type_list:
            self.del_by_type(object_type)
