"""
Read-only access to Jon's Classica Codex library.

The library is irreplaceable. It is opened with mode=ro and nothing here
writes to it. Do not open it any other way.
"""
import os
import sqlite3
from pathlib import Path


def database() -> str:
    if os.environ.get("CLASSICA_DB"):
        return os.environ["CLASSICA_DB"]
    base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local"))
    return str(base / "ClassicaCodex" / "classicacodex.db")


def library() -> sqlite3.Connection:
    """The library, read-only."""
    return sqlite3.connect(f"file:{database()}?mode=ro", uri=True)


def editions(author_like: str = None, title_like: str = None):
    """(EditionId, author, title, kind, language, translator, nodes)."""
    q = ("select e.EditionId, a.Name, w.Title, e.Kind, e.Language, e.Translator, "
         "(select count(*) from TextNodes t where t.EditionId=e.EditionId) "
         "from Works w join Authors a on a.AuthorId=w.AuthorId "
         "join Editions e on e.WorkId=w.WorkId where 1=1")
    args = []
    if author_like:
        q += " and a.Name like ?"; args.append(author_like)
    if title_like:
        q += " and w.Title like ?"; args.append(title_like)
    with library() as c:
        return list(c.execute(q, args))


def nodes(edition_id: int):
    """[(CitationRef, Text)] in reading order."""
    with library() as c:
        return list(c.execute(
            "select CitationRef, Text from TextNodes where EditionId=? order by SortOrder",
            (edition_id,)))


def export(edition_id: int, path) -> int:
    rows = nodes(edition_id)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for ref, text in rows:
            f.write(ref + "\t" + " ".join(text.split()) + "\n")
    return len(rows)


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3 and sys.argv[1] == "find":
        for r in editions(author_like=sys.argv[2] if sys.argv[2] != "-" else None,
                          title_like=sys.argv[3] if len(sys.argv) > 3 else None):
            print(r)
    elif len(sys.argv) == 4 and sys.argv[1] == "export":
        print(export(int(sys.argv[2]), sys.argv[3]), "rows")
    else:
        print("usage: py -m odybench.ccx find <author-like|-> [title-like]\n"
              "       py -m odybench.ccx export <EditionId> <out.tsv>")
