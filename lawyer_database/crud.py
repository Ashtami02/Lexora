from .database import get_connection


# ==========================================
# Add Lawyer
# ==========================================

def add_lawyer(
    full_name,
    email,
    mobile_number,
    office_address,
    bar_council_enrolment_number,
    state_bar_council,
    years_of_experience,
    primary_practice_area,
    bar_council_id_card,
    certificate_of_practice,
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO lawyers(

            full_name,
            email,
            mobile_number,
            office_address,
            bar_council_enrolment_number,
            state_bar_council,
            years_of_experience,
            primary_practice_area,
            bar_council_id_card,
            certificate_of_practice

        )

        VALUES(?,?,?,?,?,?,?,?,?,?)
        """,
        (
            full_name,
            email,
            mobile_number,
            office_address,
            bar_council_enrolment_number,
            state_bar_council,
            years_of_experience,
            primary_practice_area,
            bar_council_id_card,
            certificate_of_practice,
        ),
    )

    conn.commit()
    conn.close()


# ==========================================
# Get All Lawyers
# ==========================================

def get_all_lawyers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM lawyers")

    lawyers = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return lawyers


# ==========================================
# Get Verified Lawyers
# ==========================================

def get_verified_lawyers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM lawyers
        WHERE verification_status='Approved'
        """
    )

    lawyers = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return lawyers


# ==========================================
# Get Lawyers By Practice Area
# ==========================================

def get_lawyers_by_practice_area(practice_area):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM lawyers
        WHERE primary_practice_area=?
        AND verification_status='Approved'
        """,
        (practice_area,),
    )

    lawyers = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return lawyers


# ==========================================
# Get Lawyers By State
# ==========================================

def get_lawyers_by_state(state):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM lawyers
        WHERE state_bar_council=?
        AND verification_status='Approved'
        """,
        (state,),
    )

    lawyers = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return lawyers


# ==========================================
# Get Lawyers By Practice Area + State
# ==========================================

def get_lawyers(practice_area, state):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM lawyers
        WHERE primary_practice_area=?
        AND state_bar_council=?
        AND verification_status='Approved'
        """,
        (practice_area, state),
    )

    lawyers = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return lawyers


# ==========================================
# AI Recommended Lawyers
# ==========================================

def get_recommended_lawyers(practice_area, state):

    conn = get_connection()
    cursor = conn.cursor()

    # First try:
    # Same specialization + same state

    cursor.execute(
        """
        SELECT
            id,
            full_name,
            office_address,
            years_of_experience,
            primary_practice_area

        FROM lawyers

        WHERE verification_status='Approved'
        AND primary_practice_area=?
        AND state_bar_council=?

        ORDER BY years_of_experience DESC

        LIMIT 2
        """,
        (practice_area, state),
    )

    lawyers = [dict(row) for row in cursor.fetchall()]

    # Fallback:
    # Same specialization anywhere

    if len(lawyers) < 2:

        cursor.execute(
            """
            SELECT
                id,
                full_name,
                office_address,
                years_of_experience,
                primary_practice_area

            FROM lawyers

            WHERE verification_status='Approved'
            AND primary_practice_area=?

            ORDER BY years_of_experience DESC

            LIMIT 2
            """,
            (practice_area,),
        )

        lawyers = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return lawyers


# ==========================================
# Approve Lawyer
# ==========================================

def approve_lawyer(lawyer_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE lawyers
        SET verification_status='Approved'
        WHERE id=?
        """,
        (lawyer_id,),
    )

    conn.commit()
    conn.close()
    
# ==========================================
# Find Lawyers For Dashboard
# ==========================================

def find_lawyers(
    country=None,
    city=None,
    specialization=None,
    language=None,
    top_k=3,
):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT *
        FROM lawyers
        WHERE verification_status='Approved'
    """

    params = []

    # --------------------------------------
    # Specialization
    # --------------------------------------

    if specialization:
        query += """
            AND primary_practice_area=?
        """

        params.append(specialization)

    # --------------------------------------
    # City
    # --------------------------------------

    if city:
        query += """
            AND office_address LIKE ?
        """

        params.append(f"%{city}%")

    # --------------------------------------
    # State
    # --------------------------------------

    if country:
        # Currently no country column
        # so country is not filtered here.
        pass

    # --------------------------------------
    # Language
    # --------------------------------------

    # Currently your database does not appear
    # to have a languages column.
    #
    # We will add this later if needed.

    query += """
        ORDER BY
            years_of_experience DESC
        LIMIT ?
    """

    params.append(top_k)

    cursor.execute(
        query,
        params,
    )

    lawyers = [
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return lawyers