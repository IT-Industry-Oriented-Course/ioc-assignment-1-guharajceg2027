"""
Main entry point for the Clinical Workflow Automation Agent.
Supports interactive mode, single request mode, and dry-run mode.
"""

import argparse
import sys
from agent import ClinicalAgent

# Default API key
DEFAULT_API_KEY = "guha_key"

def print_response(response: dict):
    """Pretty print the agent response."""
    print("\n" + "="*70)
    print("AGENT RESPONSE")
    print("="*70)
    
    if response.get("refused"):
        print(f"[REFUSED] Request Refused: {response.get('error', 'Unknown reason')}")
        return
    
    if response.get("success"):
        print("[SUCCESS] Request Completed Successfully")
    else:
        print(f"[FAILED] Request Failed: {response.get('error', 'Unknown error')}")
    
    if response.get("summary"):
        print(f"\nSummary: {response['summary']}")
    
    if response.get("results"):
        print("\n" + "-"*70)
        print("DETAILED RESULTS")
        print("-"*70)
        for i, step_result in enumerate(response["results"], 1):
            step = step_result.get("step", "unknown")
            result = step_result.get("result", {})
            print(f"\n[{i}] Step: {step}")
            if result.get("success"):
                print("   [OK] Success")
                # Print key information based on step type
                if step == "search_patient" and result.get("patient"):
                    patient = result["patient"]
                    name_parts = patient.get("name", [])
                    if name_parts and len(name_parts) > 0:
                        name_obj = name_parts[0]
                        given = name_obj.get("given", [""])
                        family = name_obj.get("family", "")
                        name = " ".join(given) + " " + family if family else " ".join(given)
                        print(f"   Patient: {name.strip()}")
                    print(f"   ID: {patient.get('id', 'N/A')}")
                
                elif step == "check_insurance_eligibility" and result.get("eligibility"):
                    elig = result["eligibility"]
                    print(f"   Status: {elig.get('status', 'N/A')}")
                    print(f"   Provider: {elig.get('provider', 'N/A')}")
                    print(f"   Policy: {elig.get('policy_number', 'N/A')}")
                
                elif step == "find_available_slots" and result.get("available_slots"):
                    slots = result["available_slots"]
                    print(f"   Found {len(slots)} available slots")
                    for slot in slots[:3]:  # Show first 3
                        print(f"   • {slot['date']} at {slot['time']} with {slot['doctor']}")
                    if len(slots) > 3:
                        print(f"   ... and {len(slots) - 3} more")
                
                elif step == "book_appointment" and result.get("appointment"):
                    apt = result["appointment"]
                    print(f"   Appointment ID: {apt.get('appointment_id', 'N/A')}")
                    print(f"   Date: {apt.get('date', 'N/A')} at {apt.get('time', 'N/A')}")
                    print(f"   Doctor: {apt.get('doctor', 'N/A')}")
            else:
                print(f"   [FAIL] Failed: {result.get('error', 'Unknown error')}")
    
    print("\n" + "="*70 + "\n")

def main():
    parser = argparse.ArgumentParser(
        description="Clinical Workflow Automation Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py
  python main.py --request "Find patient Ravi Kumar"
  python main.py --request "Schedule a cardiology follow-up for patient Ravi Kumar next week and check insurance eligibility"
  python main.py --dry-run
  python main.py --api-key YOUR_API_KEY
        """
    )
    
    parser.add_argument(
        "--request",
        type=str,
        help="Process a single request and exit"
    )
    
    parser.add_argument(
        "--api-key",
        type=str,
        default=DEFAULT_API_KEY,
        help=f"HuggingFace API key (default: uses built-in key)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run in dry-run mode (simulate actions without executing)"
    )
    
    args = parser.parse_args()
    
    # Initialize agent
    print("Clinical Workflow Automation Agent")
    print("="*70)
    print(f"Initializing agent...")
    if args.dry_run:
        print("[DRY-RUN] DRY-RUN MODE: Actions will be simulated, not executed")
    
    try:
        agent = ClinicalAgent(hf_api_key=args.api_key, dry_run=args.dry_run)
        print("[OK] Agent initialized successfully\n")
    except Exception as e:
        print(f"[ERROR] Failed to initialize agent: {str(e)}")
        sys.exit(1)
    
    # Single request mode
    if args.request:
        response = agent.process_request(args.request)
        print_response(response)
        return
    
    # Interactive mode
    print("Enter requests in natural language (or 'quit'/'exit' to stop):")
    print("Example: Schedule a cardiology follow-up for patient Ravi Kumar next week and check insurance eligibility")
    print("-"*70)
    
    while True:
        try:
            request = input("\n> ").strip()
            
            if not request:
                continue
            
            if request.lower() in ["quit", "exit", "q"]:
                print("\nGoodbye!")
                break
            
            response = agent.process_request(request)
            print_response(response)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n[ERROR] Error: {str(e)}")

if __name__ == "__main__":
    main()
