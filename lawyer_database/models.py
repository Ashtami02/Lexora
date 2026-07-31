from .database import get_connection


def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lawyers (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        full_name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        mobile_number TEXT NOT NULL,

        office_address TEXT NOT NULL,

        bar_council_enrolment_number TEXT UNIQUE NOT NULL,

        state_bar_council TEXT NOT NULL,

        years_of_experience INTEGER NOT NULL,

        primary_practice_area TEXT NOT NULL,

        bar_council_id_card TEXT,

        certificate_of_practice TEXT,

        verification_status TEXT DEFAULT 'Pending',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()

    conn.close()


if __name__ == "__main__":
    create_tables()

    print("Database created.")