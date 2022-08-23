from scrapy.exceptions import NotConfigured

from easydata.utils import config


class EasyData:
    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        if not crawler.settings.getbool("EASYDATA_ENABLED"):
            raise NotConfigured

        config.from_dict(crawler.settings.copy_to_dict())

        return cls()
