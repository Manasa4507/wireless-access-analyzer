import os
import sqlite3
from datetime import datetime

# Use a path relative to this file, independent of cwd
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'analysis.db')

def get_conn():
    return sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)

def init_db():
    os.makedirs(os.path.join(BASE_DIR, 'database'), exist_ok=True)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            total_bw_mhz REAL,
            num_users INTEGER,
            per_user_rate_mbps REAL,
            snr_db REAL,
            network_condition TEXT,
            channel_model TEXT,
            results TEXT
        )
        '''
    )
    conn.commit()
    conn.close()

def insert_analysis(total_bw_mhz, num_users, per_user_rate_mbps, snr_db, network_condition, channel_model, results):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        '''
        INSERT INTO analyses (timestamp, total_bw_mhz, num_users, per_user_rate_mbps, snr_db, network_condition, channel_model, results)
        VALUES (?,?,?,?,?,?,?,?)
        ''',
        (
            datetime.now().isoformat(),
            total_bw_mhz,
            num_users,
            per_user_rate_mbps,
            snr_db,
            network_condition,
            channel_model,
            results,
        ),
    )
    analysis_id = cur.lastrowid
    conn.commit()
    conn.close()
    return analysis_id

def get_all_analyses():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM analyses ORDER BY id DESC')
    rows = cur.fetchall()
    conn.close()
    # Map to dicts
    cols = ["id", "timestamp", "total_bw_mhz", "num_users", "per_user_rate_mbps", "snr_db", "network_condition", "channel_model", "results"]
    return [dict(zip(cols, row)) for row in rows]

def get_analysis(analysis_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM analyses WHERE id = ?', (analysis_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    cols = ["id", "timestamp", "total_bw_mhz", "num_users", "per_user_rate_mbps", "snr_db", "network_condition", "channel_model", "results"]
    return dict(zip(cols, row))

def delete_analysis(analysis_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('DELETE FROM analyses WHERE id = ?', (analysis_id,))
    conn.commit()
    conn.close()

def clear_history():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('DELETE FROM analyses')
    conn.commit()
    conn.close()
