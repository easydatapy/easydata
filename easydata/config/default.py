from typing import List, Optional, Union

from easydata.exceptions import DropItem

# Config attributes used by multiple parsers
ED_LANGUAGE: str = "en"

ED_DROP_ITEM_EXCEPTION = DropItem

# Config attributes used by date time parsers
ED_DATETIME_FORMAT: str = "%m/%d/%Y %H:%M:%S"

ED_DATE_FORMAT: str = "%m/%d/%Y"

ED_TIME_FORMAT: str = "%H:%M:%S"

ED_DATETIME_FORMATS: Optional[List[str]] = None

ED_DATETIME_LANGUAGE: Optional[str] = None

ED_DATETIME_LOCALES: Optional[List[str]] = None

ED_DATETIME_REGION: Optional[str] = None

# Config attributes used by url parsers
ED_URL_DOMAIN: Optional[str] = None

ED_URL_PROTOCOL: str = "https"

# Config attributes used by number parsers
ED_NUMBER_DECIMALS: Union[int, bool] = False

ED_NUMBER_MIN_VALUE: Optional[Union[int, float]] = None

ED_NUMBER_MAX_VALUE: Optional[Union[int, float]] = None

# Config attributes used by price parsers
ED_PRICE_DECIMALS: Union[int, bool] = 2

ED_PRICE_MIN_VALUE: Optional[Union[int, float]] = None

ED_PRICE_MAX_VALUE: Optional[Union[int, float]] = None

# Config attributes used by DataXmlToDictProcessor
ED_DATA_XML_TO_DICT_ITEM_DEPTH: int = 0

# Config attributes used by ItemDiscountProcessor
ED_ITEM_DISCOUNT_ITEM_PRICE_KEY: str = "price"

ED_ITEM_DISCOUNT_ITEM_SALE_PRICE_KEY: str = "sale_price"

ED_ITEM_DISCOUNT_ITEM_DISCOUNT_KEY: str = "discount"

ED_ITEM_DISCOUNT_DECIMALS: int = 2

ED_ITEM_DISCOUNT_NO_DECIMALS: bool = False

ED_ITEM_DISCOUNT_REMOVE_ITEM_SALE_PRICE_KEY: bool = False
