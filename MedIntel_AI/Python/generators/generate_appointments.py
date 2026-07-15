import sys
import os
import random
from datetime import date, time, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database_connection import get_connection
from utils.batch_insert import chunk_data

TOTAL_APPOINTMENTS = 50000

CONSULTATION_TYPES = [
    "In-Person",
    "Video",
    "Follow-Up"
]

STATUS = [
    "Scheduled",
    "Completed",
    "Cancelled",
    "No-Show"
]

BOOKING_CHANNELS = [
    "Online",
    "Phone",
    "Walk-In",
    "Referral"
]

REASONS = [
    "Fever",
    "Headache",
    "Diabetes Review",
    "Heart Checkup",
    "Blood Pressure",
    "Skin Allergy",
    "Routine Checkup",
    "Chest Pain",
    "Back Pain",
    "Vaccination"
]


def random_date():
    start = date(2024, 1, 1)
    end = date.today()

    days = (end - start).days
    return start + timedelta(days=random.randint(0, days))


def random_time():
    hour = random.randint(9, 17)
    minute = random.choice([0, 15, 30, 45])
    return time(hour, minute)


def generate_appointments():

    connection = get_connection()
    cursor = connection.cursor()

    print("Loading Patients...")
    cursor.execute("SELECT patient_id FROM patients")
    patient_ids = [row[0] for row in cursor.fetchall()]

    print("Loading Doctors...")
    cursor.execute("SELECT doctor_id, department_id FROM doctors")
    doctor_rows = cursor.fetchall()

    if not patient_ids:
        print("❌ No patients found.")
        return

    if not doctor_rows:
        print("❌ No doctors found.")
        return

    appointments = []

    print("Generating Appointments...")

    for i in range(1, TOTAL_APPOINTMENTS + 1):

        doctor_id, department_id = random.choice(doctor_rows)

        appointments.append(
            (
                f"APT{i:07}",
                random.choice(patient_ids),
                doctor_id,
                department_id,
                random_date(),
                random_time(),
                random.choice(CONSULTATION_TYPES),
                random.choice(STATUS),
                random.choice(BOOKING_CHANNELS),
                random.choice(REASONS)
            )
        )

    print(f"Generated {len(appointments)} appointments")

    query = """
    INSERT INTO appointments
    (
        appointment_code,
        patient_id,
        doctor_id,
        department_id,
        appointment_date,
        appointment_time,
        consultation_type,
        appointment_status,
        booking_channel,
        reason_for_visit
    )
    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    batch_no = 1

    for batch in chunk_data(appointments, 5000):

        cursor.executemany(query, batch)
        connection.commit()

        print(f"✅ Batch {batch_no} inserted ({len(batch)} appointments)")
        batch_no += 1

    print(f"\n🎉 {TOTAL_APPOINTMENTS} Appointments Inserted Successfully")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    generate_appointments()