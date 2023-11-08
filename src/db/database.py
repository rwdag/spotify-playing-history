import sqlite3

TABLE_NAME = 'playing_history'

def init_db() -> None:

    conn = sqlite3.connect('db/database.db')
    cur = conn.cursor()
    table_exists = cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{TABLE_NAME}';").fetchall()

    if not table_exists:
        query = f"""CREATE TABLE {TABLE_NAME} (
                    id TEXT,
                    name TEXT,
                    artist TEXT,
                    featured_artists TEXT,
                    duration_ms INTEGER,
                    release_date TEXT,
                    popularity INTEGER,
                    started_at TEXT,
                    ms_played INTEGER
                );"""

        cur.execute(query)
    conn.close()


def insert_track(track: dict) -> None:
    columns = ','.join(track.keys())
    values = list(track.values())

    conn = sqlite3.connect('db/database.db')
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {TABLE_NAME}({columns}) VALUES (?,?,?,?,?,?,?,?,?)", values)
    conn.commit()

    conn.close()