"""Quick test to see if streamlit can run"""
import sys
print("Testing Streamlit import...")
try:
    import streamlit as st
    print(f"Streamlit version: {st.__version__}")
    print("Streamlit imported successfully!")
except Exception as e:
    print(f"Error importing streamlit: {e}")
    sys.exit(1)

print("\nTesting app imports...")
try:
    from agent import ClinicalAgent
    from functions import FUNCTION_MAP
    from data_store import data_store
    print("All imports successful!")
except Exception as e:
    print(f"Error importing app modules: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nAll tests passed! Streamlit should work.")

