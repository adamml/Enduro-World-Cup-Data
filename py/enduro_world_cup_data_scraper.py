import ewsbattlemap as batmap
import json

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, batmap.DataRecord):
            return o.asDict()

res = batmap.fetchData()
print(json.dumps(res, cls=JSONEncoder, indent=4))
