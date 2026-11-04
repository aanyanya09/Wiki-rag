import lancedb

t = lancedb.connect(r"C:\rag\wiki_index").open_table("wiki")
df = t.search().select(["name", "source"]).limit(2_000_000).to_pandas()

dups = df[df["name"].duplicated(keep=False)]
files_per_name = dups.groupby("name")["source"].nunique()

print("names that repeat:", dups["name"].nunique())
print("copies sit in DIFFERENT source files:", (files_per_name > 1).sum())
print("copies sit in the SAME source file:", (files_per_name == 1).sum())
print("\nSample repeated names:")
for n in dups["name"].drop_duplicates().head(10):
    print(" -", n)