# 🎨 Web UI User Guide

## Quick Start

1. **Install dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch the UI**:
   ```bash
   streamlit run app.py
   ```

   Or use the batch file (Windows):
   ```bash
   run_ui.bat
   ```

3. **Access the UI**: The application will automatically open in your default web browser at `http://localhost:8501`

## Features

### 🏠 Main Interface

The UI has four main sections accessible via the sidebar:

1. **💬 Natural Language** - Process requests in plain English
2. **⚡ Quick Actions** - Direct access to all functions
3. **📋 Audit Logs** - View compliance logs
4. **ℹ️ About** - System information

### 💬 Natural Language Page

**How to use:**
1. Initialize the agent from the sidebar (click "🚀 Initialize Agent")
2. Enter your request in natural language, for example:
   - "Schedule a cardiology follow-up for patient Ravi Kumar next week and check insurance eligibility"
   - "Find patient Ravi Kumar"
   - "Check insurance eligibility for patient Ravi Kumar"
3. Click "🚀 Process Request"
4. View the structured results with detailed information

**Features:**
- Example request buttons for quick testing
- Response history showing recent requests
- Detailed step-by-step results
- Beautiful formatted output

### ⚡ Quick Actions Page

Direct access to all functions with dedicated tabs:

#### 🔍 Search Patient
- Enter patient name
- Click "Search Patient"
- View patient information in FHIR format

#### 💳 Check Insurance
- Enter patient ID (e.g., PAT001)
- Click "Check Eligibility"
- View insurance status, provider, policy details, and copay

#### 📅 Find Slots
- Select specialty (Cardiology, Neurology, General Medicine)
- Set number of days ahead to search
- Click "Find Slots"
- View available appointment slots in a table

#### 📋 Book Appointment
- Enter patient ID
- Select specialty
- Enter slot ID
- Optionally add reason
- Click "Book Appointment"
- View confirmation with appointment details

### 📋 Audit Logs Page

**Features:**
- View all system actions with timestamps
- Filter by action type
- Adjust number of entries to display
- Download full audit log as JSON
- Search and review compliance data

### ⚙️ Sidebar Configuration

- **HuggingFace API Key**: Enter your API key (default provided)
- **🔒 Dry-Run Mode**: Toggle to simulate actions without executing
- **🚀 Initialize Agent**: Start the agent with current settings
- **📊 Quick Stats**: View audit log count and current mode

## UI Design Highlights

- 🎨 **Modern Gradient Design**: Beautiful color schemes
- 📱 **Responsive Layout**: Works on different screen sizes
- 🎯 **Intuitive Navigation**: Easy-to-use sidebar and tabs
- ✅ **Visual Feedback**: Success/error indicators
- 📊 **Data Visualization**: Tables and formatted displays
- 🎭 **Smooth Interactions**: Buttons and animations

## Tips

1. **Always initialize the agent first** before processing requests
2. **Use Dry-Run mode** to test workflows without making changes
3. **Check Audit Logs** for compliance tracking
4. **Try example requests** to see the system in action
5. **Use Quick Actions** for direct function access
6. **Download audit logs** for record keeping

## Troubleshooting

**Issue**: "Please initialize the agent from the sidebar first"
- **Solution**: Click "🚀 Initialize Agent" button in the sidebar

**Issue**: UI not loading
- **Solution**: Make sure Streamlit is installed: `pip install streamlit`

**Issue**: Agent initialization fails
- **Solution**: Check that the HuggingFace API key is correct

**Issue**: No results showing
- **Solution**: Check that you've entered valid input and clicked the process button

## Keyboard Shortcuts

- Press `R` to rerun the app
- Press `C` to clear cache
- Press `?` to see keyboard shortcuts in Streamlit

---

Enjoy using the Clinical Workflow Automation Agent! 🏥✨
