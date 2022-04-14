from pymongo import MongoClient, UpdateOne
from datetime import datetime
from bson.son import SON


class ParkingsDbHelper:
    def __init__(self, host, port):
        self.client = MongoClient(host, port)
        self.db = self.client.ahuzot

    def get_all_lots(self):
        lots = self.db.parkings.find({})
        return [self._parse_lot(lot) for lot in lots]

    def get_near_lots(self, point, distance):
        query = {'location': SON(
            [("$near", point), ("$maxDistance", distance)])}
        lots = self.db.parkings.find(query)
        return [self._parse_lot(lot) for lot in lots]

    def upsert_parking_lots(self, lots):
        upserts = [self._upsert_lot(lot) for lot in lots]
        self.db.parkings.bulk_write(upserts)

    def _upsert_lot(self, lot):
        lot['lastUpdateTime'] = datetime.utcnow()
        return UpdateOne({'name': lot['name']}, {'$set': lot, '$setOnInsert': {'createTime': datetime.utcnow()}}, upsert=True)

    def _parse_lot(self, lot):
        lot['id'] = str(lot['_id'])
        del lot['_id']
        lot['lastUpdateTime'] = lot['lastUpdateTime'].strftime(
            "%m/%d/%Y, %H:%M:%S")
        lot['createTime'] = lot['createTime'].strftime(
            "%m/%d/%Y, %H:%M:%S")
        return lot
