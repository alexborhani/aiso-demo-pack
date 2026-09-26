#!/usr/bin/env python3
"""
Export the rows the music-store and pet-store knowledge stores index, as JSON files beside the
databases. AISO no longer reads databases from a knowledge store (1.11.0): the stores index these
files, and questions that need the live data go to the demo-data MCP server (data/toolbox/tools.yaml).

Run after changing either database:  python3 scripts/export-demo-rows.py
"""
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "data"

MUSIC = """
SELECT
  t.TrackId AS track_id, t.Name AS track_name, COALESCE(t.Composer, '') AS composer,
  t.Milliseconds AS duration_ms, t.UnitPrice AS price,
  a.AlbumId AS album_id, a.Title AS album_title, ar.ArtistId AS artist_id, ar.Name AS artist_name,
  g.GenreId AS genre_id, g.Name AS genre_name,
  t.Name || ' by ' || COALESCE(ar.Name, 'Unknown') || ' on album ' || a.Title
    || ' [' || COALESCE(g.Name, 'Unknown') || ']'
    || ' (' || (t.Milliseconds / 60000) || ':' || printf('%02d', (t.Milliseconds % 60000) / 1000) || ')'
    || CASE WHEN t.Composer IS NOT NULL AND t.Composer <> '' THEN '. Composed by ' || t.Composer ELSE '' END
  AS summary
FROM Track t
JOIN Album a ON t.AlbumId = a.AlbumId
JOIN Artist ar ON a.ArtistId = ar.ArtistId
LEFT JOIN Genre g ON t.GenreId = g.GenreId
ORDER BY t.TrackId
LIMIT 500
"""

PETS = """
SELECT
  p.id AS pet_id, p.name AS pet_name, p.age, p.price, p.status, p.description AS summary,
  b.id AS breed_id, b.name AS breed_name, b.size, b.temperament, b.avg_lifespan,
  s.id AS species_id, s.name AS species_name
FROM pets p
JOIN breeds b ON p.breed_id = b.id
JOIN species s ON b.species_id = s.id
ORDER BY p.id
"""


def export(db: Path, query: str, out: Path) -> int:
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    rows = [dict(r) for r in con.execute(query)]
    con.close()
    out.write_text(json.dumps(rows, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return len(rows)


if __name__ == "__main__":
    n = export(ROOT / "music-store" / "musicstore.sqlite", MUSIC, ROOT / "music-store" / "tracks.json")
    print(f"music-store/tracks.json: {n} rows")
    n = export(ROOT / "pet-store" / "pet-store.db", PETS, ROOT / "pet-store" / "pets.json")
    print(f"pet-store/pets.json: {n} rows")
