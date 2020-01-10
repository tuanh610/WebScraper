import unittest
from backend.scraping.PhoneData import PhoneData
from backend.scraping.PhoneData import PhoneDataInvalidException

class TestPhoneData(unittest.TestCase):

    def test_init_string(self):
        phone = PhoneData("testPhone", "500000 VND")
        self.assertEqual(phone.getPrice(), 500000)
        self.assertEqual(phone.getName(), "testPhone")

        phone2 = PhoneData("testPhone2", "300000 VND", {"url": "https:/testURL.com"})
        self.assertEqual(phone2.getPrice(), 300000)
        self.assertEqual(phone2.getName(), "testPhone2")
        self.assertEqual(phone2.getInfo()["url"], "https:/testURL.com")

        phone3 = PhoneData("testPhone3", "$SGD 300000")
        self.assertEqual(phone3.getPrice(), 300000)
        self.assertEqual(phone3.getName(), "testPhone3")

        with self.assertRaises(PhoneDataInvalidException):
            phone4 = PhoneData("testPhone4", "hello test")


    def test_init_decimal(self):
        phone = PhoneData("testPhone", 300000)
        self.assertEqual(phone.getPrice(), 300000)
        self.assertEqual(phone.getName(), "testPhone")

        phone2 = PhoneData("testPhone2", 300.123, {"url": "https:/testURL.com", "currency": "VND"})
        self.assertEqual(phone2.getPrice(), 300.123)
        self.assertEqual(phone2.getName(), "testPhone2")
        self.assertEqual(phone2.getInfo()["url"], "https:/testURL.com")
        self.assertEqual(phone2.getInfo()["currency"], "VND")

        with self.assertRaises(PhoneDataInvalidException):
            phone3 = PhoneData("testPhone3", -100)

    def test_equal(self):
        phone1 = PhoneData("test", "3000 VND", {"url":"https://test.html"})
        phone2 = PhoneData("test", 3000, {"currency": "VND", "url":"https://test.html"})
        self.assertEqual(phone1, phone2)

if __name__ == '__main__':
    unittest.main()
