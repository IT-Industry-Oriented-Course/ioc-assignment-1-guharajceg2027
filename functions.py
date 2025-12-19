"""
Healthcare function definitions with JSON schemas for function calling.
These functions interact with the clinical data store and external APIs.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import logging
from data_store import data_store

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_patient(name: str) -> Dict[str, Any]:
    """
    Search for a patient by name.
    
    Args:
        name: Patient's full name or partial name
        
    Returns:
        Patient information in FHIR-style format
    """
    logger.info(f"[FUNCTION CALL] search_patient(name='{name}')")
    
    patient = data_store.get_patient_by_name(name)
    
    if not patient:
        return {
            "success": False,
            "error": f"Patient '{name}' not found",
            "patient": None
        }
    
    # Return in FHIR-style format
    result = {
        "success": True,
        "patient": {
            "resourceType": "Patient",
            "id": patient["patient_id"],
            "identifier": [
                {
                    "system": "http://hospital.example.org/patients",
                    "value": patient["medical_record_number"]
                }
            ],
            "name": [
                {
                    "family": patient["name"].split()[-1],
                    "given": patient["name"].split()[:-1] if len(patient["name"].split()) > 1 else [patient["name"]]
                }
            ],
            "telecom": [
                {"system": "phone", "value": patient["phone"]},
                {"system": "email", "value": patient["email"]}
            ],
            "birthDate": patient["date_of_birth"],
            "address": [
                {
                    "text": patient["address"]
                }
            ]
        }
    }
    
    logger.info(f"[RESULT] Found patient: {patient['patient_id']}")
    return result

def check_insurance_eligibility(patient_id: str) -> Dict[str, Any]:
    """
    Check insurance eligibility for a patient.
    
    Args:
        patient_id: Patient identifier (e.g., PAT001)
        
    Returns:
        Insurance eligibility information
    """
    logger.info(f"[FUNCTION CALL] check_insurance_eligibility(patient_id='{patient_id}')")
    
    insurance = data_store.get_insurance(patient_id)
    
    if not insurance:
        return {
            "success": False,
            "error": f"Insurance information not found for patient {patient_id}",
            "eligibility": None
        }
    
    result = {
        "success": True,
        "eligibility": {
            "patient_id": patient_id,
            "status": insurance["eligibility_status"],
            "provider": insurance["insurance_provider"],
            "policy_number": insurance["policy_number"],
            "coverage_type": insurance["coverage_type"],
            "copay_amount": insurance["copay"],
            "valid_until": insurance["valid_until"],
            "is_eligible": insurance["eligibility_status"] == "Active"
        }
    }
    
    logger.info(f"[RESULT] Insurance eligibility: {result['eligibility']['status']}")
    return result

def find_available_slots(specialty: str, start_date: Optional[str] = None, days_ahead: int = 7) -> Dict[str, Any]:
    """
    Find available appointment slots for a specialty.
    
    Args:
        specialty: Medical specialty (e.g., "Cardiology", "Neurology")
        start_date: Start date in YYYY-MM-DD format (default: today)
        days_ahead: Number of days ahead to search (default: 7)
        
    Returns:
        List of available appointment slots
    """
    logger.info(f"[FUNCTION CALL] find_available_slots(specialty='{specialty}', start_date={start_date}, days_ahead={days_ahead})")
    
    if not start_date:
        start_date = datetime.now().strftime("%Y-%m-%d")
    
    end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
    
    slots = data_store.get_available_slots(specialty, start_date, end_date)
    
    result = {
        "success": True,
        "specialty": specialty,
        "search_period": {
            "start": start_date,
            "end": end_date
        },
        "available_slots": [
            {
                "slot_id": slot["slot_id"],
                "date": slot["date"],
                "time": slot["time"],
                "doctor": slot["doctor"],
                "duration_minutes": slot["duration_minutes"]
            }
            for slot in slots
        ],
        "count": len(slots)
    }
    
    logger.info(f"[RESULT] Found {len(slots)} available slots")
    return result

def book_appointment(patient_id: str, slot_id: str, specialty: str, reason: Optional[str] = None) -> Dict[str, Any]:
    """
    Book an appointment for a patient.
    
    Args:
        patient_id: Patient identifier
        slot_id: Slot identifier to book
        specialty: Medical specialty
        reason: Reason for appointment (optional)
        
    Returns:
        Confirmed appointment details
    """
    logger.info(f"[FUNCTION CALL] book_appointment(patient_id='{patient_id}', slot_id='{slot_id}', specialty='{specialty}', reason={reason})")
    
    # Validate patient exists
    patient = data_store.get_patient_by_id(patient_id)
    if not patient:
        return {
            "success": False,
            "error": f"Patient {patient_id} not found",
            "appointment": None
        }
    
    # Find and validate slot
    slots = data_store.get_available_slots(specialty)
    slot = next((s for s in slots if s["slot_id"] == slot_id), None)
    
    if not slot:
        return {
            "success": False,
            "error": f"Slot {slot_id} not available for specialty {specialty}",
            "appointment": None
        }
    
    # Book the slot
    if not data_store.book_slot(slot_id):
        return {
            "success": False,
            "error": f"Failed to book slot {slot_id}",
            "appointment": None
        }
    
    # Create appointment record
    appointment_data = {
        "patient_id": patient_id,
        "patient_name": patient["name"],
        "slot_id": slot_id,
        "specialty": specialty,
        "date": slot["date"],
        "time": slot["time"],
        "doctor": slot["doctor"],
        "duration_minutes": slot["duration_minutes"],
        "reason": reason or "Follow-up appointment",
        "status": "Confirmed"
    }
    
    appointment = data_store.create_appointment(appointment_data)
    
    result = {
        "success": True,
        "appointment": {
            "appointment_id": appointment["appointment_id"],
            "patient_id": patient_id,
            "patient_name": patient["name"],
            "specialty": specialty,
            "date": slot["date"],
            "time": slot["time"],
            "doctor": slot["doctor"],
            "duration_minutes": slot["duration_minutes"],
            "reason": appointment["reason"],
            "status": "Confirmed",
            "created_at": appointment["created_at"]
        }
    }
    
    logger.info(f"[RESULT] Appointment booked: {appointment['appointment_id']}")
    return result

# Function schemas for LangChain tool definitions
FUNCTION_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search_patient",
            "description": "Search for a patient by their full name or partial name. Returns patient information in FHIR format including ID, name, contact details, and date of birth.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Patient's full name or partial name (e.g., 'Ravi Kumar' or 'Ravi')"
                    }
                },
                "required": ["name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_insurance_eligibility",
            "description": "Check insurance eligibility and coverage details for a patient. Returns eligibility status, provider, policy number, coverage type, and copay amount.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {
                        "type": "string",
                        "description": "Patient identifier (e.g., 'PAT001')"
                    }
                },
                "required": ["patient_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_available_slots",
            "description": "Find available appointment slots for a medical specialty within a date range. Returns list of slots with date, time, doctor name, and duration.",
            "parameters": {
                "type": "object",
                "properties": {
                    "specialty": {
                        "type": "string",
                        "description": "Medical specialty (e.g., 'Cardiology', 'Neurology', 'General Medicine')"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format (optional, defaults to today)"
                    },
                    "days_ahead": {
                        "type": "integer",
                        "description": "Number of days ahead to search (optional, defaults to 7)"
                    }
                },
                "required": ["specialty"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_appointment",
            "description": "Book an appointment for a patient in a specific slot. Validates patient and slot availability before booking. Returns confirmed appointment details.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {
                        "type": "string",
                        "description": "Patient identifier (e.g., 'PAT001')"
                    },
                    "slot_id": {
                        "type": "string",
                        "description": "Slot identifier to book (e.g., 'SLOT-001')"
                    },
                    "specialty": {
                        "type": "string",
                        "description": "Medical specialty (e.g., 'Cardiology')"
                    },
                    "reason": {
                        "type": "string",
                        "description": "Reason for appointment (optional)"
                    }
                },
                "required": ["patient_id", "slot_id", "specialty"]
            }
        }
    }
]

# Function mapping for execution
FUNCTION_MAP = {
    "search_patient": search_patient,
    "check_insurance_eligibility": check_insurance_eligibility,
    "find_available_slots": find_available_slots,
    "book_appointment": book_appointment
}
