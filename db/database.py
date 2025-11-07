import sqlite3
from contextlib import contextmanager

from models.incident_model import Incident, IncidentStatus, IncidentSource, IncidentField
# __________________________________________________________________________

class Database:
    def __init__(self, db_path="incidents.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS incidents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    source TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    # ______________________________________________________________________

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    # ______________________________________________________________________

    def create_incident(self, incident):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            fields = [field.value for field in IncidentField]
            fields.pop(0)
            quests = ['?'] * (len(IncidentField) - 1)
            request = f"INSERT INTO incidents ({','.join(fields)}) VALUES ({','.join(quests)})"

            cursor.execute(
                request, (
                    incident.description,
                    incident.type.value,
                    incident.status.value,
                    incident.source.value,
                    incident.created_at
                )
            )
            conn.commit()
            return cursor.lastrowid
    # ______________________________________________________________________

    def get_incidents(self, status=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            fields = [field.value for field in IncidentField]

            if status:
                cursor.execute(
                    f"SELECT {','.join(fields)} FROM incidents WHERE {IncidentField.STATUS.value} = ? ORDER BY {IncidentField.CREATEDAT.value} DESC",
                    (status.value if isinstance(status, IncidentStatus) else status,)
                )
            else:
                cursor.execute(f"SELECT {','.join(fields)} FROM incidents ORDER BY {IncidentField.CREATEDAT.value} DESC")
            rows = cursor.fetchall()

            return [Incident.from_row(row) for row in rows]
    # ______________________________________________________________________

    def update_incident_status(self, incident_id, new_status):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE incidents SET {IncidentField.STATUS.value} = ? WHERE {IncidentField.ID.value} = ?",
                (new_status.value if isinstance(new_status, IncidentStatus) else new_status, incident_id)
            )
            conn.commit()
            return cursor.rowcount > 0
    # ______________________________________________________________________

    def get_incident_by_id(self, incident_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            fields = [field.value for field in IncidentField]

            cursor.execute(
                f"SELECT {','.join(fields)} FROM incidents WHERE {IncidentField.ID.value} = ?",
                (incident_id,)
            )
            row = cursor.fetchone()
            return Incident.from_row(row) if row else None

