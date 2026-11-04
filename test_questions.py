import time
from rag_core import search

tests = [
    ("Where is the Bayil Arena and what is it used for?", "Bayil Arena"),
    ("Where was Golborne South railway station located?", "Golborne South railway station"),
    ("Which insect species in the genus Hemipeplus is named after Heisenberg?", "Hemipeplus heisenbergi"),
    ("Who co-authored The Future We Choose with Christiana Figueres?", "Tom Rivett-Carnac"),
    ("Where does the ruddy tody-flycatcher live?", "Ruddy tody-flycatcher"),
    ("Who is Harold V. Jones II?", "Harold V. Jones II"),
    ("Where is the Rombro Building located?", "Rombro Building"),
    ("What is the population of the municipality of Utuado?", "Utuado, Puerto Rico"),
    ("What is the Irish science outreach programme Discover Science and Engineering?", "Discover Science & Engineering"),
    ("Who directed the 2025 horror film Dolly?", "Dolly (2025 film)"),
    ("Who is Marco Carparelli?", "Marco Carparelli"),
    ("Who is Hermogenes Dolganyov?", "Hermogenes Dolganyov"),
    ("Where is the village of Oud Sluis?", "Oud Sluis"),
    ("Who is Hans Ave Lallemant?", "Hans Avé Lallemant"),
    ("What is the Charak fair of faith?", "Charak: Fair of Faith"),
    ("Where does Peterson Creek flow into the Cataraqui River?", "Peterson Creek (Cataraqui River tributary)"),
    ("What was Curtis Stigers' 1991 debut album?", "Curtis Stigers (album)"),
    ("What are the Qwartz Electronic Music Awards?", "Qwartz Electronic Music Awards"),
    ("Who was Erastus J. Turner?", "Erastus J. Turner"),
    ("Who is Sarath Mandava?", "Sarath Mandava"),
]

hits = 0
for q, expected in tests:
    t0 = time.time()
    names = search(q, k=5)["name"].tolist()
    ok = expected in names
    hits += ok
    print("OK  " if ok else "MISS", f"{time.time()-t0:.1f}s", q, "->", names[:3])

print(f"\nTop-5 hit rate: {hits}/{len(tests)}")