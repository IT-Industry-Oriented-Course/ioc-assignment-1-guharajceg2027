"""Display all data in the application"""
from data_store import data_store

print("="*60)
print("CLINICAL WORKFLOW AUTOMATION - DATA SUMMARY")
print("="*60)

# Patients
print(f"\nPATIENTS: {len(data_store.patients)}")
for patient_id, patient in data_store.patients.items():
    print(f"  • {patient['name']} ({patient_id})")
    print(f"    DOB: {patient['date_of_birth']}, MRN: {patient['medical_record_number']}")

# Insurance Records
print(f"\nINSURANCE RECORDS: {len(data_store.insurance)}")
for patient_id, insurance in data_store.insurance.items():
    patient_name = data_store.patients.get(patient_id, {}).get('name', 'Unknown')
    print(f"  • {patient_name} ({patient_id})")
    print(f"    Provider: {insurance['insurance_provider']}")
    print(f"    Policy: {insurance['policy_number']}, Status: {insurance['eligibility_status']}")
    print(f"    Copay: Rs.{insurance['copay']}, Valid until: {insurance['valid_until']}")

# Available Appointment Slots
print(f"\nAVAILABLE APPOINTMENT SLOTS:")
total_slots = 0
for specialty, slots in data_store.available_slots.items():
    slot_count = len(slots)
    total_slots += slot_count
    print(f"  • {specialty}: {slot_count} slots")
    for slot in slots:
        print(f"    - {slot['slot_id']}: {slot['date']} at {slot['time']} with {slot['doctor']}")

print(f"\n    TOTAL SLOTS: {total_slots}")

# Booked Appointments
print(f"\nBOOKED APPOINTMENTS: {len(data_store.appointments)}")
if data_store.appointments:
    for apt_id, apt in data_store.appointments.items():
        print(f"  • {apt_id}: {apt['patient_name']} ({apt['patient_id']})")
        print(f"    {apt['specialty']} - {apt['date']} at {apt['time']} with {apt['doctor']}")
        print(f"    Status: {apt['status']}")
else:
    print("  (No appointments booked yet)")

# Summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"Total Patients:        {len(data_store.patients)}")
print(f"Total Insurance:       {len(data_store.insurance)}")
print(f"Total Available Slots: {total_slots}")
print(f"Total Booked Apps:     {len(data_store.appointments)}")
print(f"\nGRAND TOTAL DATA RECORDS: {len(data_store.patients) + len(data_store.insurance) + total_slots + len(data_store.appointments)}")
print("="*60)

