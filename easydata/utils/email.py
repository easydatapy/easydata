import re
from typing import Generator, Optional

EMAIL_SEARCH_REGEX = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"


def search(text: str) -> Generator:
    results = re.finditer(EMAIL_SEARCH_REGEX, text)

    for result in results:
        yield result.group(1)


def search_one(text: str) -> Optional[str]:
    for result in search(text):
        return result

    return None
