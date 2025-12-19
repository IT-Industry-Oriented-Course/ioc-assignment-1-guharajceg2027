# Clinical Workflow Automation Agent

A function-calling LLM agent designed for clinical workflow automation, specifically for appointment scheduling and care coordination. The agent safely interprets natural language requests and executes validated actions through structured function calls.

## 🎯 Purpose

This agent acts as an intelligent coordinator between clinicians and healthcare systems. It helps with:
- Patient lookup and information retrieval
- Insurance eligibility verification
- Appointment slot discovery
- Appointment booking and scheduling

**Important**: This agent does NOT provide medical advice, diagnosis, or treatment recommendations. It only performs workflow orchestration tasks.

## 🔑 Features

- ✅ Natural language processing for clinical requests
- ✅ Function calling with JSON schemas (FHIR-style)
- ✅ Input validation and safety checks
- ✅ Comprehensive audit logging
- ✅ Dry-run mode for testing
- ✅ Refusal mechanism for unsafe requests
- ✅ Dictionary-based mock data store

## 📋 Prerequisites

- Python 3.8 or higher
- HuggingFace API key (provided in code)

## 🚀 Installation

1. Clone or navigate to the project directory:
```bash
cd "C:\Users\Guharaj Muralitharan\Desktop\IOC"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🎨 Web UI (Recommended)

Launch the beautiful Streamlit web interface:

```bash
streamlit run app.py
```

The UI will open in your default web browser at `http://localhost:8501`

### UI Features:
- 💬 **Natural Language Processing**: Enter requests in plain English
- ⚡ **Quick Actions**: Direct access to all functions
- 📋 **Audit Logs**: View and download compliance logs
- 🎨 **Modern Design**: Beautiful, intuitive interface
- 🔒 **Dry-Run Mode**: Test without making changes

## 📖 Usage

### Interactive Mode (Recommended)

Start the agent in interactive mode:
```bash
python main.py
```

Or in dry-run mode (simulates actions without executing):
```bash
python main.py --dry-run
```

### Single Request Mode

Process a single request:
```bash
python main.py --request "Schedule a cardiology follow-up for patient Ravi Kumar next week and check insurance eligibility"
```

### Example Requests

1. **Search for a patient:**
   ```
   Find patient Ravi Kumar
   ```

2. **Check insurance eligibility:**
   ```
   Check insurance eligibility for patient Ravi Kumar
   ```

3. **Find available slots:**
   ```
   Find available cardiology appointments next week
   ```

4. **Complete workflow (recommended):**
   ```
   Schedule a cardiology follow-up for patient Ravi Kumar next week and check insurance eligibility
   ```

## 🏗️ Architecture

### Project Structure

```
.
├── main.py              # CLI interface
├── agent.py             # Main agent implementation
├── functions.py         # Function definitions and schemas
├── data_store.py        # Mock data store (dictionary-based)
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── clinical_agent.log  # Audit log (generated at runtime)
```

### Components

1. **ClinicalAgent** (`agent.py`): 
   - Processes natural language requests
   - Validates requests for safety
   - Orchestrates function calls
   - Maintains audit logs

2. **Functions** (`functions.py`):
   - `search_patient(name)`: Search patients by name
   - `check_insurance_eligibility(patient_id)`: Check insurance status
   - `find_available_slots(specialty, start_date, days_ahead)`: Find appointments
   - `book_appointment(patient_id, slot_id, specialty, reason)`: Book appointments

3. **Data Store** (`data_store.py`):
   - In-memory dictionary storage
   - Sample patient, insurance, and appointment data
   - Slot management

## 🔒 Safety Features

The agent includes multiple safety mechanisms:

1. **Request Validation**: Blocks medical advice and unsafe actions
2. **Input Schema Validation**: Validates all function inputs
3. **Error Handling**: Graceful error handling with clear messages
4. **Audit Logging**: All actions are logged to `clinical_agent.log`
5. **Refusal Mechanism**: Agent refuses unsafe requests with justification

## 📊 Data Format

The agent uses FHIR-style JSON schemas for patient data:

```json
{
  "resourceType": "Patient",
  "id": "PAT001",
  "name": [{"family": "Kumar", "given": ["Ravi"]}],
  "telecom": [{"system": "phone", "value": "+91-9876543210"}],
  "birthDate": "1985-03-15"
}
```

## 🧪 Testing

### Dry-Run Mode

Test the agent without making actual changes:
```bash
python main.py --dry-run
```

### Sample Data

The agent includes sample data:
- **Patients**: Ravi Kumar (PAT001), Priya Sharma (PAT002), Amit Patel (PAT003)
- **Specialties**: Cardiology, Neurology, General Medicine
- **Insurance**: All patients have active insurance

## 📝 Audit Logging

All actions are logged to `clinical_agent.log` with timestamps. The log includes:
- Request received
- Function calls
- Function results
- Errors
- Request completion

View recent log entries in interactive mode by typing 'y' when prompted.

## ⚠️ Limitations

- This is a POC (Proof of Concept) implementation
- Uses mock data store (dictionary-based, not persistent)
- HuggingFace API integration may have rate limits
- Some edge cases in natural language parsing may require refinement

## 🔮 Future Enhancements

- Persistent database integration
- Real FHIR API integration
- More sophisticated intent recognition
- Multi-turn conversation support
- Integration with Electronic Health Records (EHR) systems

## 📄 License

This is an educational project for clinical workflow automation demonstration.

## 👤 Author

Created as part of a clinical workflow automation assignment demonstrating function-calling LLM agents in healthcare contexts.

---

**Note**: This agent is designed for workflow orchestration only. It does not provide medical advice, diagnosis, or treatment recommendations. Always consult with healthcare professionals for medical decisions.
