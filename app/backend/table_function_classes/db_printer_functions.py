from app.backend.db import DB

class DBPrinterFunctions:
    def __init__(self, db_:DB):
        self.db = db_

    def get_printers(self):
        query = """
        SELECT
            id,
            name,
            location,
            model,
            curr_status,
            toner_level,
            paper_level,
            last_maintenance
        FROM Printer
        ORDER BY name ASC
        """
        params = ()
        return self.db.get_all(query, params)

    def get_printers_needing_attention_count(self):
        query = """
        SELECT COUNT(*)
        FROM Printer
        WHERE toner_level <= 20
        OR paper_level <= 20
        OR curr_status IN ('Offline', 'Maintenance')
        """
        params = ()
        result = self.db.get_one(query, params)
        return result[0] if result else 0