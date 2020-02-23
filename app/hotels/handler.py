from re import escape

from flask import current_app

from app.db import get_db


class HotelsHandler:
    def __init__(self):
        self.db = get_db()

    def get_all_hotels(self, data):
        skip = data.get('skip', 0)
        limit = data.get('limit', 0)
        pipeline = [
            {
                '$match': {
                    'name': {'$regex': escape(data.get('search_key', '')), '$options': 'i'},
                    'neighbourhood_group': {'$regex': escape(data.get('region', '')), '$options': 'i'},
                }
            }, {
                '$addFields': {
                    'price': {'$toDouble': '$price'}
                }
            },
            {
                '$sort': {
                    data.get('sort_key', 'name'): data.get('sort_value', 1)
                }
            },
            {'$skip': skip},
            {'$limit': limit}
        ]
        hotels = list(self.db.aggregate_docs(current_app.config['MONGO_DBNAME'], current_app.config['MONGO_COL_HOTELS'],
                                             pipeline))
        total = len(
            list(self.db.aggregate_docs(current_app.config['MONGO_DBNAME'], current_app.config['MONGO_COL_HOTELS'],
                                        pipeline[:-2])))
        return {'status_id': 1, 'hotels': hotels, 'total': total, 'filters': data}

    def get_all_regions(self):
        res = list(self.db.filter_docs(current_app.config['MONGO_DBNAME'], current_app.config['MONGO_COL_HOTELS'], {},
                                       {'neighbourhood_group': 1}))
        regions = list()
        for region in res:
            regions.append(region.get('neighbourhood_group'))
        return {'status_id': 1, 'regions': list(set(regions))}
