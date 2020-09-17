from typing import List, Optional, Tuple


def get_key_from_query(
    query: str,
    separator: str = "::",
) -> Tuple[Optional[str], str]:

    query_parts = query.split(separator)

    new_query = None if query.startswith(separator) else query_parts[0]

    return new_query, query_parts[-1]


def get_extension_value(
    pseudo_key: str,
    pseudo_keys_with_separator_value: Optional[List[str]] = None,
    separator: str = "-",
):

    if not has_extension(pseudo_key, pseudo_keys_with_separator_value, separator):
        return pseudo_key, None

    pseudo_key_parts = pseudo_key.split("-")

    # If split by - produces more than 2 list items that means that we are dealing
    # with value that has - in it.
    if len(pseudo_key_parts) > 2:
        pseudo_key = "-".join(pseudo_key_parts[:-1])
    else:
        pseudo_key = pseudo_key_parts[0]

    return pseudo_key, pseudo_key_parts[-1]


def has_extension(
    pseudo_key: str,
    pseudo_keys_with_separator_value: Optional[List[str]] = None,
    separator: str = "-",
):

    pkwsv = pseudo_keys_with_separator_value

    if pkwsv and any(pseudo_key.startswith(pks) for pks in pkwsv):
        if "){}".format(separator) not in pseudo_key:
            return False

    if separator in pseudo_key:
        return True

    return False
