import json

class myTable():
    def get_data(self):
        json_table = {"id":"123", "name": "abc"}
        return json.dumps(json_table)