import polars

df = polars.read_json("data/data.json")

print(df.head())
