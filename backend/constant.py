from backend.database.DatabaseEngine import DynamoElement, DynamoGSI
from backend.scraping.HoangHaMobileScraper import HoangHaMobileScraper
from backend.scraping.SourceData import SourceData, SourceInfo

phonePrimaryElements = [DynamoElement('BRAND', 'HASH', 'S'), DynamoElement('MODEL', 'RANGE', 'S')]
phoneSecondaryElements = [DynamoGSI("TypeIndex",
                                    [DynamoElement('TYPE', 'HASH', 'S'), DynamoElement('PRICE', 'RANGE', 'N')])]
dynamoDBTableName = "WebScraperDB"

parser = {"hoanghaMobile": HoangHaMobileScraper}

scrapingSources = [
    SourceData(url="https://hoanghamobile.com/dien-thoai-di-dong-c14.html", name="hoanghaMobile", info=SourceInfo(param="?sort=0&p=", ignoreTerm=["Chính hãng", "Chính Hãng", "-"]))
]
