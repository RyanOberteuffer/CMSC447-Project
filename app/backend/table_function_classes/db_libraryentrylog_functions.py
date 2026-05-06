from app.backend.db import DB

class DBLELFunctions:
    def __init__(self, db_:DB):
        self.db = db_

    def get_library_entry_log(self):
        query = """
        SELECT
            id,
            entry_time,
            entry_count
        FROM LibraryEntryLog
        ORDER BY entry_time ASC
        """
        params = ()
        return self.db.get_all(query, params)

    def get_total_entries_today(self):
        query = """
        SELECT COALESCE(SUM(entry_count), 0)
        FROM LibraryEntryLog
        WHERE DATE(entry_time) = DATE('now')
        """
        params = ()
        result = self.db.get_all(query, params)
        return result[0][0] if result else 0

    def get_peak_hour_today(self):
        query = """
        SELECT entry_time, entry_count
        FROM LibraryEntryLog
        WHERE DATE(entry_time) = DATE('now')
        ORDER BY entry_count DESC
        LIMIT 1
        """
        params = ()
        result = self.db.get_all(query, params)
        return result[0] if result else None