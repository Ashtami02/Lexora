import sqlite3

DB = "chat_memory.db"


class ChatMemory:

    def __init__(self):

        self.conn = sqlite3.connect(
            DB,
            check_same_thread=False,
        )

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            session_id TEXT NOT NULL,

            role TEXT NOT NULL,

            message TEXT NOT NULL

        )
        """)

        self.conn.commit()

    # ----------------------------------------
    # Add Message
    # ----------------------------------------

    def add_message(
        self,
        session_id,
        role,
        message,
    ):

        self.conn.execute(
            """
            INSERT INTO conversations(
                session_id,
                role,
                message
            )

            VALUES(?,?,?)
            """,
            (
                session_id,
                role,
                message,
            ),
        )

        self.conn.commit()

    # Backward compatibility
    save = add_message

    # ----------------------------------------
    # Get Conversation
    # ----------------------------------------

    def get_history(
        self,
        session_id,
        limit=10,
    ):

        cursor = self.conn.execute(
            """
            SELECT role, message

            FROM conversations

            WHERE session_id=?

            ORDER BY id DESC

            LIMIT ?
            """,
            (
                session_id,
                limit,
            ),
        )

        rows = cursor.fetchall()

        rows.reverse()

        return [
            {
                "role": role,
                "message": message,
            }
            for role, message in rows
        ]

    # ----------------------------------------
    # Delete Conversation
    # ----------------------------------------

    def clear_history(
        self,
        session_id,
    ):

        self.conn.execute(
            """
            DELETE FROM conversations
            WHERE session_id=?
            """,
            (session_id,),
        )

        self.conn.commit()

    # ----------------------------------------
    # List Sessions
    # ----------------------------------------

    def get_sessions(self):

        cursor = self.conn.execute(
            """
            SELECT DISTINCT session_id
            FROM conversations
            ORDER BY id DESC
            """
        )

        return [row[0] for row in cursor.fetchall()]


chat_memory = ChatMemory()