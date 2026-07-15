from generate_departments import *
from generate_wards import *
from generate_doctors import *
from generate_nurses import *
from generate_patients import *
from generate_beds import *
from generate_suppliers import *
from generate_medicines import *

print("=" * 60)
print("🏥 MedIntel AI - Master Data Generator")
print("=" * 60)

print("\nGenerating Departments...")
generate_departments()

print("\nGenerating Wards...")
generate_wards()

print("\nGenerating Doctors...")
generate_doctors()

print("\nGenerating Nurses...")
generate_nurses()

print("\nGenerating Patients...")
generate_patients()

print("\nGenerating Beds...")
generate_beds()

print("\nGenerating Suppliers...")
generate_suppliers()

print("\nGenerating Medicines...")
generate_medicines()

print("\n✅ Master Data Generation Completed Successfully!")