import sys
import os
import random
from datetime import date, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_connection import get_connection
from utils.random_data import random_name

QUALIFICATIONS = [
    "GNM",
    "B.Sc Nursing",
    "M.Sc Nursing",
    "Post Basic B.Sc Nursing"
]

SHIFT_TYPES = [
    "Morning",
    "Evening",
    "Night"
]

STATUS = [
    "Active",
    "Active",
    "Active",
    "On Leave"
]


def random_phone():
    return "9" + "".join(random.choices("0123456789", k=9))


def random_joining_date():
    start = date(2016, 1, 1)
    end = date(2026, 1, 1)

    days = (end - start).days

    return start + timedelta(days=random.randint(0, days))


def generate_nurses():

    connection = get_connection()
    cursor = connection.cursor()

    nurses = []

    for i in range(1, 1501):

        nurses.append((
            f"NUR{i:05}",
            random_name(),
            random.choice(["Male", "Female"]),
            random.randint(1, 10),
            random.choice(QUALIFICATIONS),
            random_phone(),
            f"nurse{i}@medintel.com",
            random.randint(1, 20),
            random.choice(SHIFT_TYPES),
            random_joining_date(),
            random.choice(STATUS)
        ))

    query = """
    INSERT INTO nurses
    (
        nurse_code,
        nurse_name,
        gender,
        department_id,
        qualification,
        phone,
        email,
        experience_years,
        shift_type,
        joining_date,
        status
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.executemany(query, nurses)

    connection.commit()

    print(f"✅ {len(nurses)} Nurses Inserted Successfully")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_nurses()