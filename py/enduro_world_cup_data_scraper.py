import ewsbattlemap as batmap
import json

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, batmap.DataRecord) or isinstance(o, batmap.StageRecord):
            return o.asDict()

res = batmap.fetchData()

with open("data/data.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(res, cls=JSONEncoder, ensure_ascii=False, indent=4))
