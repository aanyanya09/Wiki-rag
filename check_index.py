import lancedb

db = lancedb.connect(r"C:\rag\wiki_index")
t = db.open_table("wiki")
print("total rows:", t.count_rows())

df = t.search().select(["name", "source"]).limit(2_000_000).to_pandas()
print("duplicate names:", df["name"].duplicated().sum())
print("rows with no source:", df["source"].isna().sum())
print("files covered:", df["source"].nunique())

print("\nRandom articles you can write test questions about:")
for n in df["name"].sample(30, random_state=1).tolist():
    print(" -", n)