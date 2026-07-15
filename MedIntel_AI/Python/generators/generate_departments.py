import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_connection import get_connection


def generate_wards():

    wards = [
        ("Cardiac ICU", "W001", "ICU", 1, 30, 22, 2, "Station A", "Active"),
        ("General Cardiology", "W002", "General", 1, 50, 35, 2, "Station B", "Active"),
        ("Neuro ICU", "W003", "ICU", 2, 25, 18, 3, "Station A", "Active"),
        ("General Neurology", "W004", "General", 2, 40, 28, 3, "Station B", "Active"),
        ("Orthopedic Ward", "W005", "General", 3, 60, 45, 4, "Station A", "Active"),
        ("Pediatric Ward", "W006", "General", 4, 35, 20, 1, "Station A", "Active"),
        ("Emergency Ward", "W007", "Emergency", 5, 50, 41, 0, "Station ER", "Active"),
        ("Radiology Unit", "W008", "Diagnostic", 6, 20, 12, 1, "Station R", "Active"),
        ("Oncology Ward", "W009", "Special", 7, 45, 33, 5, "Station O", "Active"),
        ("ENT Ward", "W010", "General", 8, 25, 14, 2, "Station ENT", "Active"),
        ("Dermatology Ward", "W011", "General", 9, 20, 11, 3, "Station D", "Active"),
        ("Central ICU", "W012", "ICU", 10, 40, 31, 0, "Station ICU", "Active")
    ]

    connection = get_connection()

    cursor = connection.cursor()

    query = """
    INSERT INTO wards
    (
        ward_name,
        ward_code,
        ward_type,
        department_id,
        total_beds,
        occupied_beds,
        floor_number,
        nurse_station,
        status
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.executemany(query, wards)

    connection.commit()

    print("✅ Wards Inserted Successfully")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_wards()