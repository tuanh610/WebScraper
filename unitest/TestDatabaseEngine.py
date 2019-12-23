import unittest
import DatabaseEngine
from DatabaseEngine import ClientError
from DatabaseEngine import dynammoDBAdapter
from PhoneData import PhoneData

class TestDatabaseCreation(unittest.TestCase):
    def test_dbCreation(self):
        tableName = "test_table"
        outputCreate = "Create table " + tableName + "successfully"
        outputDelete = "Delete table " + tableName + " successfully"
        self.assertEqual(outputCreate, DatabaseEngine.createTable(tableName))
        self.assertEqual(outputDelete, DatabaseEngine.deleteTable(tableName))

class TestDatabaseFunctional(unittest.TestCase):

    def setUp(self) -> None:
        self.phone = PhoneData("testPhone", "500000 VND")
        self.phone2 = PhoneData("testPhone2", "300000 VND", {"url": "https:/testURL.com"})
        self.phone3 = PhoneData("testPhone3", "$SGD 300000")
        self.data = [self.phone, self.phone2, self.phone3]
        self.tableName = "test_table"
        DatabaseEngine.createTable(self.tableName)
        self.db = dynammoDBAdapter(self.tableName)

    def tearDown(self) -> None:
        DatabaseEngine.deleteTable(self.tableName)
        
    def test_insert_update_deleteData(self):
        # Insert
        self.db.pushAllDataToDB(self.data)
        retriveData = self.db.getAllDataFromTable()
        ok = True
        for item in self.data:
            if item not in retriveData:
                ok = False
                break
        self.assertTrue(ok, "Push data failed")
        # Update
        self.phone.price = 12345
        self.phone.info["currency"] = "Yolo Dollar"
        self.db.updateItemToDB(self.phone)
        try:
            result = self.db.getItemFromDB(self.phone.name)
            self.assertIsNotNone(result)
        except ClientError as e:
            self.fail("update Data failed")
        # Delete
        self.db.deleteItemFromDB(self.phone)
        self.assertIsNone(self.db.getItemFromDB(self.phone.name))



if __name__ == '__main__':
    unittest.main()
