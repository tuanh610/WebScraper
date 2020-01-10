from backend.database.DatabaseEngine import DynamoElement
from backend.scraping.HoangHaMobileScraper import HoangHaMobileScraper

sourceElements = [DynamoElement('NAME', 'HASH', 'S'), DynamoElement('TYPE', 'RANGE', 'S')]
sourceTableName = "Source"
phoneElements = [DynamoElement('NAME', 'HASH', 'S'), DynamoElement('BRAND', 'RANGE', 'S')]

parser = {"hoanghaMobile": HoangHaMobileScraper}
