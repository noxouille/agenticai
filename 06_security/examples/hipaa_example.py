# Example implementation of HIPAA compliance for healthcare AI applications

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json

# Import the HIPAAComplianceManager class from hipaa.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.hipaa import HIPAAComplianceManager

def create_mock_patient_data():
    """
    Create mock patient data for HIPAA compliance demonstration.
    """
    np.random.seed(42)  # For reproducible results
    
    # Generate 50 mock patient records
    n_patients = 50
    
    patients = []
    for i in range(n_patients):
        patient = {
            "patient_id": f"PT{i+1:03d}",
            "name": f"Patient {i+1}",
            "date_of_birth": (datetime.now() - timedelta(days=np.random.randint(365*20, 365*90))).isoformat(),
            "ssn": f"{np.random.randint(100,999)}-{np.random.randint(10,99)}-{np.random.randint(1000,9999)}",
            "address": f"{np.random.randint(100,9999)} Main St",
            "city": "Healthcare City",
            "state": "HC",
            "zip": f"{np.random.randint(10000,99999)}",
            "phone": f"555-{np.random.randint(100,999)}-{np.random.randint(1000,9999)}",
            "email": f"patient{i+1}@email.com",
            "mrn": f"MRN{i+1:06d}",
            "diagnosis": np.random.choice(["Diabetes", "Hypertension", "Asthma", "Depression", "Arthritis"]),
            "medications": np.random.choice(["Metformin", "Lisinopril", "Albuterol", "Sertraline", "Ibuprofen"]),
            "allergies": np.random.choice(["None", "Penicillin", "Peanuts", "Shellfish", "Latex"]),
            "vital_signs": {
                "blood_pressure": f"{np.random.randint(90,180)}/{np.random.randint(60,120)}",
                "heart_rate": np.random.randint(60, 100),
                "temperature": round(np.random.uniform(97.0, 101.0), 1)
            },
            "insurance_info": f"INS{np.random.randint(100000,999999)}",
            "provider_id": f"DR{np.random.randint(1,20):03d}"
        }
        patients.append(patient)
    
    return patients

def demonstrate_minimum_necessary():
    """
    Demonstrate HIPAA minimum necessary standard compliance.
    """
    print("=== HIPAA Minimum Necessary Standard Demo ===\n")
    
    # Initialize HIPAA compliance manager
    hipaa_manager = HIPAAComplianceManager("HealthcareAI Corp", "CE001")
    
    # Test different access scenarios
    scenarios = [
        {
            "purpose": "treatment",
            "requested_data": ["patient_id", "diagnosis", "medications", "allergies", "vital_signs", "ssn", "address"],
            "user": "Dr. Smith"
        },
        {
            "purpose": "payment",
            "requested_data": ["patient_id", "insurance_info", "billing_codes", "service_dates", "diagnosis"],
            "user": "Billing Clerk"
        },
        {
            "purpose": "research",
            "requested_data": ["age_range", "diagnosis_category", "treatment_response", "name", "ssn"],
            "user": "Research Team"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"--- Scenario {i}: {scenario['purpose'].title()} Access ---")
        print(f"User: {scenario['user']}")
        print(f"Requested data: {scenario['requested_data']}")
        
        validation = hipaa_manager.validate_minimum_necessary(
            scenario["requested_data"], 
            scenario["purpose"]
        )
        
        print(f"Compliant: {'✓' if validation['compliant'] else '✗'}")
        print(f"Approved fields: {validation['approved_fields']}")
        if validation['denied_fields']:
            print(f"Denied fields: {validation['denied_fields']}")
        print(f"Justification: {validation['justification']}\n")

def demonstrate_deidentification():
    """
    Demonstrate HIPAA Safe Harbor de-identification.
    """
    print("=== HIPAA Safe Harbor De-identification Demo ===\n")
    
    # Initialize HIPAA compliance manager
    hipaa_manager = HIPAAComplianceManager("HealthcareAI Corp", "CE001")
    
    # Create sample patient data
    patients = create_mock_patient_data()
    sample_patient = patients[0]
    
    print("1. Original Patient Data (contains PHI):")
    print(json.dumps(sample_patient, indent=2))
    print("\n" + "="*60 + "\n")
    
    print("2. De-identified Patient Data (Safe Harbor method):")
    deidentified_patient = hipaa_manager.deidentify_data(sample_patient)
    print(json.dumps(deidentified_patient, indent=2))
    print("\n" + "="*60 + "\n")
    
    print("3. De-identification Summary:")
    deident_info = deidentified_patient["_deidentification_info"]
    print(f"Method: {deident_info['method']}")
    print(f"Removed identifiers: {deident_info['removed_identifiers']}")
    print(f"Processing timestamp: {deident_info['timestamp']}")

def demonstrate_consent_management():
    """
    Demonstrate patient consent management.
    """
    print("=== HIPAA Patient Consent Management Demo ===\n")
    
    # Initialize HIPAA compliance manager
    hipaa_manager = HIPAAComplianceManager("HealthcareAI Corp", "CE001")
    
    # Sample patient
    patient_id = "PT001"
    
    print("1. Recording Patient Consents:")
    
    # Record various types of consent
    consent_types = [
        ("treatment", True, None),
        ("research", True, (datetime.now() + timedelta(days=365)).isoformat()),
        ("marketing", False, None),
        ("data_sharing", True, (datetime.now() + timedelta(days=180)).isoformat())
    ]
    
    for consent_type, granted, expiration in consent_types:
        consent_record = hipaa_manager.manage_patient_consent(
            patient_id, consent_type, granted, expiration
        )
        status = "GRANTED" if granted else "DENIED"
        expiry_info = f" (expires: {expiration})" if expiration else " (no expiration)"
        print(f"   • {consent_type.title()}: {status}{expiry_info}")
    
    print("\n2. Checking Consent Status:")
    
    for consent_type, _, _ in consent_types:
        is_valid = hipaa_manager.check_patient_consent(patient_id, consent_type)
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"   • {consent_type.title()}: {status}")

def demonstrate_audit_logging():
    """
    Demonstrate HIPAA audit logging and reporting.
    """
    print("=== HIPAA Audit Logging Demo ===\n")
    
    # Initialize HIPAA compliance manager
    hipaa_manager = HIPAAComplianceManager("HealthcareAI Corp", "CE001")
    
    print("1. Logging PHI Access Events:")
    
    # Simulate various access events
    access_events = [
        ("DR001", "PT001", ["diagnosis", "medications"], "treatment", True),
        ("NR002", "PT001", ["vital_signs", "allergies"], "treatment", True),
        ("BL003", "PT002", ["insurance_info", "billing_codes"], "payment", True),
        ("RS004", "PT003", ["age_range", "diagnosis_category"], "research", True),
        ("DR005", "PT004", ["ssn", "address"], "treatment", False)  # Unauthorized access
    ]
    
    for user_id, patient_id, data_accessed, purpose, success in access_events:
        hipaa_manager.log_phi_access(user_id, patient_id, data_accessed, purpose, success)
        status = "SUCCESS" if success else "FAILED"
        print(f"   • User {user_id} accessed {data_accessed} for {purpose}: {status}")
    
    print("\n2. Generating Audit Report:")
    
    # Generate audit report for the last 30 days
    start_date = (datetime.now() - timedelta(days=30)).isoformat()
    end_date = datetime.now().isoformat()
    
    audit_report = hipaa_manager.generate_audit_report(start_date, end_date)
    
    print(f"   Report ID: {audit_report['report_id']}")
    print(f"   Period: {audit_report['report_period']['start_date']} to {audit_report['report_period']['end_date']}")
    print(f"   Total access attempts: {audit_report['summary']['total_access_attempts']}")
    print(f"   Successful accesses: {audit_report['summary']['successful_accesses']}")
    print(f"   Failed accesses: {audit_report['summary']['failed_accesses']}")
    print(f"   Unique users: {audit_report['summary']['unique_users']}")
    print(f"   Unique patients accessed: {audit_report['summary']['unique_patients_accessed']}")
    print(f"   Compliance status: {audit_report['compliance_status']}")

def demonstrate_breach_detection():
    """
    Demonstrate HIPAA breach detection and assessment.
    """
    print("=== HIPAA Breach Detection Demo ===\n")
    
    # Initialize HIPAA compliance manager
    hipaa_manager = HIPAAComplianceManager("HealthcareAI Corp", "CE001")
    
    print("1. Breach Scenario Assessment:")
    
    # Simulate different breach scenarios
    breach_scenarios = [
        {
            "description": "Laptop with patient files stolen from employee vehicle",
            "affected_individuals": 150,
            "data_types": ["name", "diagnosis", "treatment", "ssn"]
        },
        {
            "description": "Email with patient list sent to wrong recipient",
            "affected_individuals": 25,
            "data_types": ["name", "email", "appointment_date"]
        },
        {
            "description": "Database server breach exposing patient records",
            "affected_individuals": 10000,
            "data_types": ["name", "ssn", "diagnosis", "financial", "genetic"]
        }
    ]
    
    for i, scenario in enumerate(breach_scenarios, 1):
        print(f"--- Breach Scenario {i} ---")
        breach_assessment = hipaa_manager.detect_potential_breach(
            scenario["description"],
            scenario["affected_individuals"], 
            scenario["data_types"]
        )
        
        print(f"Description: {scenario['description']}")
        print(f"Affected individuals: {scenario['affected_individuals']}")
        print(f"Severity: {breach_assessment['severity'].upper()}")
        print(f"Requires OCR notification: {'Yes' if breach_assessment['requires_ocr_notification'] else 'No'}")
        print(f"Individual notification deadline: {breach_assessment['notification_deadline']}")
        print()

def demonstrate_hipaa_compliance_workflow():
    """
    Demonstrate complete HIPAA compliance workflow.
    """
    print("=== Complete HIPAA Compliance Workflow ===\n")
    
    print("This workflow demonstrates how all HIPAA components work together:")
    print("1. ✓ Minimum Necessary Standard - Validate data access requests")
    print("2. ✓ Patient Consent Management - Track and verify consent")
    print("3. ✓ De-identification - Remove PHI using Safe Harbor method")
    print("4. ✓ Audit Logging - Track all PHI access events")
    print("5. ✓ Breach Detection - Assess and respond to potential breaches")
    print("\nKey HIPAA Requirements Addressed:")
    print("• Administrative Safeguards - Access controls and audit procedures")
    print("• Physical Safeguards - Breach detection and response")
    print("• Technical Safeguards - De-identification and access logging")
    print("• Privacy Rule - Minimum necessary and consent management")
    print("• Security Rule - Audit trails and incident response")
    print("• Breach Notification Rule - Automated breach assessment")

if __name__ == "__main__":
    # Run all demonstrations
    demonstrate_minimum_necessary()
    print("\n" + "="*80 + "\n")
    
    demonstrate_deidentification()
    print("\n" + "="*80 + "\n")
    
    demonstrate_consent_management()
    print("\n" + "="*80 + "\n")
    
    demonstrate_audit_logging()
    print("\n" + "="*80 + "\n")
    
    demonstrate_breach_detection()
    print("\n" + "="*80 + "\n")
    
    demonstrate_hipaa_compliance_workflow()
    
    print("\n=== Production Implementation Notes ===")
    print("1. Encrypt all PHI at rest and in transit")
    print("2. Implement role-based access controls")
    print("3. Regular security risk assessments")
    print("4. Staff training on HIPAA compliance")
    print("5. Business associate agreements for third parties")
    print("6. Incident response procedures")
    print("7. Regular audit and monitoring procedures")