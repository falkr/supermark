from pathlib import Path

b = b"docs"

p = Path(b.decode("utf-8"))
print(p)

p = Path("docs")
print(p)