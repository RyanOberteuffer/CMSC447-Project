from app.backend.db import DB
from app.backend.table_object_classes.feedback import Feedback
from app.backend.table_object_classes.user import User

class DBFeedbackFunctions:
    def __init__(self, db_:DB):
        self.db = db_

    def add_feedback(self, feedback:Feedback):
        """
        Takes a feedback object and adds it to the database.
        """
        query = "INSERT INTO FeedbackForms (type, content, user_id) VALUES (?, ?, ?)"
        params = (feedback.type, feedback.content, feedback.user_id)
        self.db.execute_command(query, params)

    def get_last_feedback(self, user:User) -> Feedback | None:
        """
        Given a User object, searches the database and returns the Feedback object with the most recent timestamp. If no matches are found, returns None
        """
        query = "SELECT * FROM FeedbackForms WHERE user_id = ? ORDER BY submission_time DESC LIMIT 1"
        params = (user.id,)
        result = self.db.get_one(query, params)
        print(result)
        if result:
            return Feedback.from_row(result)
        else:
            return None