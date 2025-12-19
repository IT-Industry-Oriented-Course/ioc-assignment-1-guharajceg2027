"""
Mock data store for clinical workflow automation.
Uses dictionaries to store patients, appointments, insurance, and slots.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import random

class ClinicalDataStore:
    """In-memory data store for clinical data using dictionaries."""
    
    def __init__(self):
        # Initialize with sample data - expanded dataset
        
        # Generate 30+ patients
        patient_names = [
            ("Ravi Kumar", "1985-03-15", "MRN-001"),
            ("Priya Sharma", "1990-07-22", "MRN-002"),
            ("Amit Patel", "1978-11-08", "MRN-003"),
            ("Sunita Reddy", "1988-05-12", "MRN-004"),
            ("Rajesh Verma", "1982-09-25", "MRN-005"),
            ("Anjali Mehta", "1992-02-18", "MRN-006"),
            ("Vikram Singh", "1987-08-30", "MRN-007"),
            ("Kavita Nair", "1991-12-05", "MRN-008"),
            ("Deepak Joshi", "1984-04-22", "MRN-009"),
            ("Meera Desai", "1989-06-14", "MRN-010"),
            ("Arjun Iyer", "1986-10-03", "MRN-011"),
            ("Sneha Gupta", "1993-01-28", "MRN-012"),
            ("Rohan Kapoor", "1983-07-19", "MRN-013"),
            ("Neha Malhotra", "1990-11-07", "MRN-014"),
            ("Siddharth Rao", "1985-09-15", "MRN-015"),
            ("Divya Chawla", "1992-03-21", "MRN-016"),
            ("Karan Sharma", "1988-12-09", "MRN-017"),
            ("Pooja Agarwal", "1991-05-26", "MRN-018"),
            ("Rahul Nair", "1987-02-13", "MRN-019"),
            ("Anita Krishnan", "1989-08-04", "MRN-020"),
            ("Varun Menon", "1986-04-17", "MRN-021"),
            ("Shreya Pillai", "1993-10-29", "MRN-022"),
            ("Aryan Bhatt", "1984-01-11", "MRN-023"),
            ("Isha Patel", "1990-06-23", "MRN-024"),
            ("Aditya Khanna", "1988-11-16", "MRN-025"),
            ("Riya Sen", "1992-07-08", "MRN-026"),
            ("Nikhil Das", "1987-03-02", "MRN-027"),
            ("Sanya Kohli", "1991-09-20", "MRN-028"),
            ("Kunal Shah", "1985-12-31", "MRN-029"),
            ("Tanya Oberoi", "1989-05-14", "MRN-030"),
            ("Rohit Yadav", "1986-08-27", "MRN-031"),
            ("Aisha Khan", "1993-02-09", "MRN-032"),
            ("Manish Tiwari", "1988-10-18", "MRN-033"),
            ("Kritika Bansal", "1990-04-05", "MRN-034"),
            ("Vivek Pandey", "1987-01-24", "MRN-035"),
        ]
        
        cities = [
            ("Bangalore", "Karnataka", "+91-9876543210"),
            ("Mumbai", "Maharashtra", "+91-9876543211"),
            ("Delhi", "NCR", "+91-9876543212"),
            ("Chennai", "Tamil Nadu", "+91-9876543213"),
            ("Hyderabad", "Telangana", "+91-9876543214"),
            ("Pune", "Maharashtra", "+91-9876543215"),
            ("Kolkata", "West Bengal", "+91-9876543216"),
            ("Ahmedabad", "Gujarat", "+91-9876543217"),
        ]
        
        self.patients: Dict[str, Dict] = {}
        for i, (name, dob, mrn) in enumerate(patient_names):
            patient_id = f"PAT{i+1:03d}"
            city, state, phone_base = cities[i % len(cities)]
            phone = f"+91-{int(phone_base.split('-')[1]) + i}"
            street_num = 100 + i
            
            self.patients[patient_id] = {
                "patient_id": patient_id,
                "name": name,
                "date_of_birth": dob,
                "phone": phone,
                "email": name.lower().replace(" ", ".") + "@example.com",
                "address": f"{street_num} Medical Street, {city}, {state}",
                "medical_record_number": mrn
            }
        
        # Insurance providers and types
        insurance_providers = [
            "MediCare Insurance",
            "Health Shield",
            "WellCare Plus",
            "Prime Health Insurance",
            "Global Medical Coverage",
            "SecureHealth",
            "LifeCare Insurance",
        ]
        
        coverage_types = ["Comprehensive", "Standard", "Premium", "Basic"]
        
        self.insurance: Dict[str, Dict] = {}
        for patient_id, patient in self.patients.items():
            provider = random.choice(insurance_providers)
            coverage = random.choice(coverage_types)
            copay_amounts = {"Premium": 300, "Comprehensive": 500, "Standard": 750, "Basic": 1000}
            
            # Valid until date (1-3 years from now)
            valid_until = (datetime.now() + timedelta(days=random.randint(365, 1095))).strftime("%Y-%m-%d")
            
            self.insurance[patient_id] = {
                "patient_id": patient_id,
                "insurance_provider": provider,
                "policy_number": f"POL-{random.randint(100000, 999999)}",
                "coverage_type": coverage,
                "eligibility_status": "Active",
                "copay": copay_amounts[coverage],
                "valid_until": valid_until
            }
        
        self.appointments: Dict[str, Dict] = {}
        
        # Generate many appointment slots across multiple specialties and dates
        specialties_config = {
            "Cardiology": {
                "doctors": ["Dr. Anil Reddy", "Dr. Meera Singh", "Dr. Karthik Nair"],
                "duration": 30,
                "slot_count": 25
            },
            "Neurology": {
                "doctors": ["Dr. Rajesh Kumar", "Dr. Priya Sharma", "Dr. Sanjay Verma"],
                "duration": 45,
                "slot_count": 20
            },
            "General Medicine": {
                "doctors": ["Dr. Sunita Devi", "Dr. Ramesh Iyer", "Dr. Lakshmi Menon"],
                "duration": 20,
                "slot_count": 30
            },
            "Orthopedics": {
                "doctors": ["Dr. Vikram Patel", "Dr. Anjali Desai"],
                "duration": 30,
                "slot_count": 18
            },
            "Dermatology": {
                "doctors": ["Dr. Sneha Reddy", "Dr. Arjun Mehta"],
                "duration": 25,
                "slot_count": 15
            },
            "Pediatrics": {
                "doctors": ["Dr. Kavita Nair", "Dr. Rohit Joshi"],
                "duration": 30,
                "slot_count": 20
            },
        }
        
        today = datetime.now()
        self.available_slots: Dict[str, List[Dict]] = {}
        slot_id_counter = 1
        
        # Generate slots for next 4 weeks
        for specialty, config in specialties_config.items():
            self.available_slots[specialty] = []
            doctors = config["doctors"]
            duration = config["duration"]
            
            for day_offset in range(1, 29):  # Next 4 weeks
                slot_date = (today + timedelta(days=day_offset)).strftime("%Y-%m-%d")
                
                # Skip weekends
                date_obj = today + timedelta(days=day_offset)
                if date_obj.weekday() >= 5:  # Saturday = 5, Sunday = 6
                    continue
                
                # Generate 1-3 slots per day per doctor
                slots_per_doctor = random.randint(1, 2)
                for doctor in doctors:
                    for slot_num in range(slots_per_doctor):
                        # Different times: morning (8-12), afternoon (13-17)
                        if slot_num == 0:
                            hour = random.choice([9, 10, 11])
                        else:
                            hour = random.choice([14, 15, 16])
                        minute = random.choice([0, 30])
                        time_str = f"{hour:02d}:{minute:02d}"
                        
                        slot_id = f"SLOT-{slot_id_counter:04d}"
                        slot_id_counter += 1
                        
                        self.available_slots[specialty].append({
                            "slot_id": slot_id,
                            "date": slot_date,
                            "time": time_str,
                            "doctor": doctor,
                            "duration_minutes": duration
                        })
                        
                        # Limit total slots per specialty
                        if len(self.available_slots[specialty]) >= config["slot_count"]:
                            break
                    if len(self.available_slots[specialty]) >= config["slot_count"]:
                        break
        
        self.appointment_counter = 1
    
    def get_patient_by_name(self, name: str) -> Optional[Dict]:
        """Search patient by name (case-insensitive partial match)."""
        name_lower = name.lower()
        for patient in self.patients.values():
            if name_lower in patient["name"].lower():
                return patient
        return None
    
    def get_patient_by_id(self, patient_id: str) -> Optional[Dict]:
        """Get patient by ID."""
        return self.patients.get(patient_id)
    
    def get_insurance(self, patient_id: str) -> Optional[Dict]:
        """Get insurance information for a patient."""
        return self.insurance.get(patient_id)
    
    def get_available_slots(self, specialty: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict]:
        """Get available slots for a specialty, optionally filtered by date range."""
        slots = self.available_slots.get(specialty, [])
        
        if start_date or end_date:
            filtered_slots = []
            for slot in slots:
                slot_date = slot["date"]
                if start_date and slot_date < start_date:
                    continue
                if end_date and slot_date > end_date:
                    continue
                filtered_slots.append(slot)
            return filtered_slots
        
        return slots
    
    def book_slot(self, slot_id: str) -> bool:
        """Mark a slot as booked (remove from available slots)."""
        for specialty_slots in self.available_slots.values():
            for i, slot in enumerate(specialty_slots):
                if slot["slot_id"] == slot_id:
                    specialty_slots.pop(i)
                    return True
        return False
    
    def create_appointment(self, appointment_data: Dict) -> Dict:
        """Create a new appointment and return the appointment record."""
        appointment_id = f"APT-{self.appointment_counter:04d}"
        self.appointment_counter += 1
        
        appointment = {
            "appointment_id": appointment_id,
            "created_at": datetime.now().isoformat(),
            **appointment_data
        }
        
        self.appointments[appointment_id] = appointment
        return appointment
    
    def get_appointment(self, appointment_id: str) -> Optional[Dict]:
        """Get appointment by ID."""
        return self.appointments.get(appointment_id)

# Global data store instance
data_store = ClinicalDataStore()
