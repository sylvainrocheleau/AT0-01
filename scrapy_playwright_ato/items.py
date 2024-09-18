import scrapy


class ScrapersItem(scrapy.Item):
    Sport = scrapy.Field()
    Competition = scrapy.Field()
    Home_Team = scrapy.Field()
    Away_Team = scrapy.Field()
    Date = scrapy.Field()
    Bets = scrapy.Field()
    Match_Url = scrapy.Field()
    Competition_Url = scrapy.Field()
    Sport_Url = scrapy.Field()
    extraction_time_utc = scrapy.Field()
    date_confidence = scrapy.Field()
    error_message = scrapy.Field()
    error_details = scrapy.Field()
    proxy_ip = scrapy.Field()
    browser = scrapy.Field()
    proxy_ip = scrapy.Field()
    updated_on = scrapy.Field()
    user_agent_hash = scrapy.Field()
    pass
