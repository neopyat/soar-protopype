from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.incident import Incident


DB_PATH: Path = Path("backend/database/soar.db")


class Database:
    def __init__(self) -> None:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)

        self.conn: sqlite3.Connection = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row

        self._init_tables()

    # -------------------------
    # INIT
    # -------------------------
    def _init_tables(self) -> None:
        cursor = self.conn.cursor()

        # incidents
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id TEXT PRIMARY KEY,
            type TEXT,
            ip TEXT,
            severity TEXT,
            timestamp REAL,
            status TEXT,
            mitre TEXT,
            threat TEXT
        )
        """)

        # actions
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_id TEXT,
            action_type TEXT,
            target TEXT,
            timestamp REAL
        )
        """)

        # -------------------------
        # INDEXES (ВАЖНО)
        # -------------------------
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_incident_ip ON incidents(ip)
        """)

        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_actions_target ON actions(target)
        """)

        self.conn.commit()

    # -------------------------
    # INCIDENTS
    # -------------------------
    def insert_incident(self, inc: Incident) -> None:
        cursor = self.conn.cursor()

        cursor.execute("""
        INSERT OR IGNORE INTO incidents
        (id, type, ip, severity, timestamp, status, mitre, threat)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            inc.id,
            inc.type,
            inc.ip,
            inc.severity,
            float(inc.timestamp),
            inc.status,
            inc.mitre,
            inc.threat
        ))

        self.conn.commit()

    # -------------------------
    # ACTIONS
    # -------------------------
    def insert_action(
        self,
        incident_id: Optional[str],
        action_type: str,
        target: str,
        timestamp: float
    ) -> None:
        cursor = self.conn.cursor()

        cursor.execute("""
        INSERT INTO actions (incident_id, action_type, target, timestamp)
        VALUES (?, ?, ?, ?)
        """, (
            incident_id,
            action_type,
            target,
            timestamp
        ))

        self.conn.commit()

    # -------------------------
    # CHECKS
    # -------------------------
    def is_ip_blocked(self, ip: str) -> bool:
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT 1 FROM actions
        WHERE action_type = 'block_ip' AND target = ?
        LIMIT 1
        """, (ip,))

        return cursor.fetchone() is not None

    # -------------------------
    # UPDATE
    # -------------------------
    def update_incident_status(self, incident_id: str, status: str) -> None:
        cursor = self.conn.cursor()

        cursor.execute("""
        UPDATE incidents
        SET status = ?
        WHERE id = ?
        """, (status, incident_id))

        self.conn.commit()

    # -------------------------
    # CLOSE
    # -------------------------
    def close(self) -> None:
        self.conn.close()


# from __future__ import annotations

# import sqlite3
# from pathlib import Path
# from typing import Optional, TYPE_CHECKING

# if TYPE_CHECKING:
#     from models.incident import Incident


# DB_PATH: Path = Path("backend/database/soar.db")


# class Database:
#     def __init__(self) -> None:
#         DB_PATH.parent.mkdir(parents=True, exist_ok=True)

#         self.conn: sqlite3.Connection = sqlite3.connect(DB_PATH)
#         self.conn.row_factory = sqlite3.Row

#         self._init_tables()

#     def _init_tables(self) -> None:
#         cursor = self.conn.cursor()

#         cursor.execute("""
#         CREATE TABLE IF NOT EXISTS incidents (
#             id TEXT PRIMARY KEY,
#             type TEXT,
#             ip TEXT,
#             severity TEXT,
#             timestamp REAL,
#             status TEXT,
#             mitre TEXT,
#             threat TEXT
#         )
#         """)

#         cursor.execute("""
#         CREATE TABLE IF NOT EXISTS actions (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             incident_id TEXT,
#             action_type TEXT,
#             target TEXT,
#             timestamp REAL
#         )
#         """)

#         self.conn.commit()

#     def insert_incident(self, inc: Incident) -> None:
#         cursor = self.conn.cursor()

#         cursor.execute("""
#         INSERT OR IGNORE INTO incidents
#         (id, type, ip, severity, timestamp, status, mitre, threat)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#         """, (
#             inc.id,
#             inc.type,
#             inc.ip,
#             inc.severity,
#             float(inc.timestamp),
#             inc.status,
#             inc.mitre,
#             inc.threat
#         ))

#         self.conn.commit()

#     def insert_action(
#         self,
#         incident_id: Optional[str],
#         action_type: str,
#         target: str,
#         timestamp: float
#     ) -> None:
#         cursor = self.conn.cursor()

#         cursor.execute("""
#         INSERT INTO actions (incident_id, action_type, target, timestamp)
#         VALUES (?, ?, ?, ?)
#         """, (
#             incident_id,
#             action_type,
#             target,
#             timestamp
#         ))

#         self.conn.commit()

#     def is_ip_blocked(self, ip: str) -> bool:
#         cursor = self.conn.cursor()

#         cursor.execute("""
#         SELECT 1 FROM actions
#         WHERE action_type = 'block_ip' AND target = ?
#         LIMIT 1
#         """, (ip,))

#         return cursor.fetchone() is not None

#     def update_incident_status(self, incident_id: str, status: str) -> None:
#         cursor = self.conn.cursor()

#         cursor.execute("""
#         UPDATE incidents
#         SET status = ?
#         WHERE id = ?
#         """, (status, incident_id))

#         self.conn.commit()

# from __future__ import annotations

# import sqlite3
# from pathlib import Path
# from typing import Optional, TYPE_CHECKING

# if TYPE_CHECKING:
#     from models.incident import Incident


# DB_PATH: Path = Path("backend/database/soar.db")


# class Database:
#     def __init__(self) -> None:
#         DB_PATH.parent.mkdir(parents=True, exist_ok=True)

#         self.conn: sqlite3.Connection = sqlite3.connect(DB_PATH)
#         self.conn.row_factory = sqlite3.Row

#         self._init_tables()

#     def _init_tables(self) -> None:
#         cursor = self.conn.cursor()

#         cursor.execute("""
#         CREATE TABLE IF NOT EXISTS incidents (
#             id TEXT PRIMARY KEY,
#             type TEXT,
#             ip TEXT,
#             severity TEXT,
#             timestamp REAL,
#             status TEXT,
#             mitre TEXT,
#             threat TEXT
#         )
#         """)

#         cursor.execute("""
#         CREATE TABLE IF NOT EXISTS actions (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             incident_id TEXT,
#             action_type TEXT,
#             target TEXT,
#             timestamp REAL
#         )
#         """)

#         self.conn.commit()

#     def insert_incident(self, inc: Incident) -> None:
#         cursor = self.conn.cursor()

#         cursor.execute("""
#         INSERT OR IGNORE INTO incidents
#         (id, type, ip, severity, timestamp, status, mitre, threat)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#         """, (
#             inc.id,
#             inc.type,
#             inc.ip,
#             inc.severity,
#             float(inc.timestamp),
#             inc.status,
#             inc.mitre,
#             inc.threat
#         ))

#         self.conn.commit()

#     def insert_action(
#         self,
#         incident_id: Optional[str],
#         action_type: str,
#         target: str,
#         timestamp: float
#     ) -> None:
#         cursor = self.conn.cursor()

#         cursor.execute("""
#         INSERT INTO actions (incident_id, action_type, target, timestamp)
#         VALUES (?, ?, ?, ?)
#         """, (
#             incident_id,
#             action_type,
#             target,
#             timestamp
#         ))

#         self.conn.commit()
        