import random
from datetime import date, timedelta

FIRST_NAMES = [
    "Arjun","Rahul","Priya","Ananya","Karthik","Sneha","Vikram","Deepa",
    "Rohit","Meera","Sanjay","Nisha","Akhil","Divya","Harish","Pooja",
    "Amit","Neha","Rakesh","Swathi","Ashwin","Keerthana","Suresh","Lavanya"
]

LAST_NAMES = [
    "Kumar","Sharma","Iyer","Reddy","Patel","Singh","Nair","Verma",
    "Gupta","Mishra","Joshi","Menon","Rao","Das","Chandra","Kapoor"
]

CITIES = [
    "Chennai",
    "Bangalore",
    "Hyderabad",
    "Coimbatore",
    "Madurai",
    "Delhi",
    "Mumbai",
    "Pune",
    "Kochi",
    "Mysore"
]

STATES = {
    "Chennai":"Tamil Nadu",
    "Coimbatore":"Tamil Nadu",
    "Madurai":"Tamil Nadu",
    "Bangalore":"Karnataka",
    "Mysore":"Karnataka",
    "Hyderabad":"Telangana",
    "Delhi":"Delhi",
    "Mumbai":"Maharashtra",
    "Pune":"Maharashtra",
    "Kochi":"Kerala"
}

BLOOD_GROUPS = [
    "A+","A-","B+","B-","AB+","AB-","O+","O-"
]

MARITAL_STATUS = [
    "Single",
    "Married",
    "Divorced"
]

INSURANCE_STATUS = [
    "Insured",
    "Not Insured"
]

NATIONALITY = "Indian"


def random_name():
    return random.choice(FIRST_NAMES) + " " + random.choice(LAST_NAMES)


def random_gender():
    return random.choice(["Male","Female"])


def random_phone():
    return "9" + "".join(random.choices("0123456789",k=9))


def random_city():
    city = random.choice(CITIES)
    return city, STATES[city]


def random_blood_group():
    return random.choice(BLOOD_GROUPS)


def random_marital_status():
    return random.choice(MARITAL_STATUS)


def random_insurance():
    return random.choice(INSURANCE_STATUS)


def random_dob():

    start = date(1945,1,1)
    end = date(2025,1,1)

    days = (end-start).days

    return start + timedelta(days=random.randint(0,days))


def random_pincode():
    return str(random.randint(600001,699999))


def random_address():
    return f"{random.randint(1,999)}, Main Road"