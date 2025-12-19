# Quick Start Guide

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Agent

### Option 1: Interactive Mode (Recommended)

Start the agent and enter requests interactively:

```bash
python main.py
```

Example interaction:
```
> Schedule a cardiology follow-up for patient Ravi Kumar next week and check insurance eligibility
```

### Option 2: Single Request Mode

Process one request and exit:

```bash
python main.py --request "Find patient Ravi Kumar"
```

### Option 3: Dry-Run Mode

Test without making actual changes:

```bash
python main.py --dry-run
```

## Example Requests

### 1. Search for a Patient
```
Find patient Ravi Kumar
```

### 2. Check Insurance Eligibility
```
Check insurance eligibility for patient Ravi Kumar
```

### 3. Find Available Appointments
```
Find available cardiology appointments next week
```

### 4. Complete Workflow (Recommended)
```
Schedule a cardiology follow-up for patient Ravi Kumar next week and check insurance eligibility
```

## Testing

Run the test suite:

```bash
python test_agent.py
```

## Sample Data

The agent comes with pre-loaded sample data:

**Patients:**
- Ravi Kumar (PAT001)
- Priya Sharma (PAT002)
- Amit Patel (PAT003)

**Specialties:**
- Cardiology
- Neurology
- General Medicine

**Insurance:**
- All patients have active insurance coverage

## Troubleshooting

### Issue: Import errors
**Solution:** Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: API key errors
**Solution:** The API key is hardcoded in the code. If you need to change it, modify `main.py` or use the `--api-key` parameter.

### Issue: No slots found
**Solution:** The sample data includes slots for the next week. Try requests without date restrictions.

## Next Steps

1. Review the audit log: `clinical_agent.log`
2. Experiment with different requests
3. Modify the data store to add more patients/slots
4. Extend function schemas for additional capabilities

## For Evaluators

To demonstrate the POC:

1. Run: `python main.py`
2. Enter: `Schedule a cardiology follow-up for patient Ravi Kumar next week and check insurance eligibility`
3. Review the structured response showing:
   - Patient found
   - Insurance eligibility checked
   - Slots found
   - Appointment booked
4. Check the audit log for compliance tracking
