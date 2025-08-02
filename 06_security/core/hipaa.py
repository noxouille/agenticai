# HIPAA Compliance Module for Healthcare AI Applications

import hashlib
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json

class HIPAAComplianceManager:
    """
    HIPAA Compliance Manager for healthcare AI applications.
    
    Provides functionality to ensure HIPAA compliance including:
    - Minimum necessary standard
    - Access controls and audit logging
    - De-identification of PHI
    - Patient consent management
    - Breach notification requirements
    """
    
    def __init__(self, organization_name: str, covered_entity_id: str):
        """
        Initialize HIPAA Compliance Manager.
        
        Parameters:
        * organization_name: Name of the covered entity
        * covered_entity_id: Unique identifier for the covered entity
        """
        self.organization_name = organization_name
        self.covered_entity_id = covered_entity_id
        self.audit_log = []
        self.consent_records = {}
        self.access_log = []
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(f"HIPAA_{organization_name}")
    
    def validate_minimum_necessary(self, requested_data: List[str], purpose: str) -> Dict[str, Any]:
        """
        Validate that data access follows minimum necessary standard.
        
        Parameters:
        * requested_data: List of data fields being requested
        * purpose: Purpose for accessing the data
        
        Returns:
        * Dictionary with validation results and approved fields
        """
        # Define minimum necessary data for common purposes
        minimum_necessary_map = {
            "treatment": ["patient_id", "diagnosis", "medications", "allergies", "vital_signs"],
            "payment": ["patient_id", "insurance_info", "billing_codes", "service_dates"],
            "operations": ["patient_id", "provider_id", "service_type", "outcome_measures"],
            "research": ["age_range", "diagnosis_category", "treatment_response"],
            "quality_assurance": ["provider_id", "service_type", "outcome_measures", "compliance_metrics"]
        }
        
        approved_fields = minimum_necessary_map.get(purpose.lower(), [])
        
        # Check which requested fields are necessary
        necessary_fields = [field for field in requested_data if field in approved_fields]
        unnecessary_fields = [field for field in requested_data if field not in approved_fields]
        
        validation_result = {
            "timestamp": datetime.now().isoformat(),
            "purpose": purpose,
            "requested_fields": requested_data,
            "approved_fields": necessary_fields,
            "denied_fields": unnecessary_fields,
            "compliant": len(unnecessary_fields) == 0,
            "justification": f"Access approved for {purpose} purposes under minimum necessary standard"
        }
        
        # Log the validation
        self._log_access_attempt(validation_result)
        
        return validation_result
    
    def deidentify_data(self, data: Dict[str, Any], method: str = "safe_harbor") -> Dict[str, Any]:
        """
        De-identify healthcare data according to HIPAA Safe Harbor method.
        
        Parameters:
        * data: Dictionary containing potentially identifiable data
        * method: De-identification method ("safe_harbor" or "expert_determination")
        
        Returns:
        * De-identified data dictionary
        """
        if method != "safe_harbor":
            raise NotImplementedError("Only Safe Harbor method is currently implemented")
        
        # HIPAA Safe Harbor identifiers to remove/modify
        safe_harbor_identifiers = [
            "name", "address", "city", "state", "zip", "phone", "fax", "email",
            "ssn", "mrn", "account_number", "license_number", "vehicle_id",
            "device_id", "web_url", "ip_address", "biometric_id", "photo"
        ]
        
        deidentified_data = data.copy()
        removed_identifiers = []
        
        for identifier in safe_harbor_identifiers:
            if identifier in deidentified_data:
                if identifier == "zip":
                    # Keep first 3 digits of ZIP code if population > 20,000
                    zip_code = str(deidentified_data[identifier])
                    if len(zip_code) >= 3:
                        deidentified_data[identifier] = zip_code[:3] + "00"
                    else:
                        del deidentified_data[identifier]
                        removed_identifiers.append(identifier)
                elif identifier in ["name", "address", "city"]:
                    # Replace with generic identifiers
                    deidentified_data[identifier] = f"REDACTED_{identifier.upper()}"
                    removed_identifiers.append(identifier)
                else:
                    # Remove other identifiers completely
                    del deidentified_data[identifier]
                    removed_identifiers.append(identifier)
        
        # Handle dates - reduce to year only if over 89 years old
        if "date_of_birth" in deidentified_data:
            try:
                dob = datetime.fromisoformat(str(deidentified_data["date_of_birth"]))
                age = (datetime.now() - dob).days // 365
                if age > 89:
                    deidentified_data["age_category"] = "90+"
                else:
                    deidentified_data["age"] = age
                del deidentified_data["date_of_birth"]
                removed_identifiers.append("date_of_birth")
            except:
                del deidentified_data["date_of_birth"]
                removed_identifiers.append("date_of_birth")
        
        # Add de-identification metadata
        deidentified_data["_deidentification_info"] = {
            "method": method,
            "timestamp": datetime.now().isoformat(),
            "removed_identifiers": removed_identifiers,
            "organization": self.organization_name
        }
        
        self._log_deidentification(data, deidentified_data, removed_identifiers)
        
        return deidentified_data
    
    def manage_patient_consent(self, patient_id: str, consent_type: str, 
                              granted: bool, expiration_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Manage patient consent for data use.
        
        Parameters:
        * patient_id: Unique patient identifier
        * consent_type: Type of consent (treatment, research, marketing, etc.)
        * granted: Whether consent is granted
        * expiration_date: Optional expiration date for consent
        
        Returns:
        * Consent record dictionary
        """
        consent_id = str(uuid.uuid4())
        
        consent_record = {
            "consent_id": consent_id,
            "patient_id": self._hash_identifier(patient_id),
            "consent_type": consent_type,
            "granted": granted,
            "timestamp": datetime.now().isoformat(),
            "expiration_date": expiration_date,
            "organization": self.organization_name,
            "covered_entity_id": self.covered_entity_id
        }
        
        # Store consent record
        if patient_id not in self.consent_records:
            self.consent_records[patient_id] = {}
        
        self.consent_records[patient_id][consent_type] = consent_record
        
        self.logger.info(f"Consent {consent_type} {'granted' if granted else 'revoked'} for patient {self._hash_identifier(patient_id)}")
        
        return consent_record
    
    def check_patient_consent(self, patient_id: str, consent_type: str) -> bool:
        """
        Check if patient has valid consent for specified use.
        
        Parameters:
        * patient_id: Unique patient identifier
        * consent_type: Type of consent to check
        
        Returns:
        * Boolean indicating if valid consent exists
        """
        if patient_id not in self.consent_records:
            return False
        
        if consent_type not in self.consent_records[patient_id]:
            return False
        
        consent = self.consent_records[patient_id][consent_type]
        
        # Check if consent is granted
        if not consent["granted"]:
            return False
        
        # Check if consent has expired
        if consent["expiration_date"]:
            expiration = datetime.fromisoformat(consent["expiration_date"])
            if datetime.now() > expiration:
                return False
        
        return True
    
    def log_phi_access(self, user_id: str, patient_id: str, data_accessed: List[str], 
                      purpose: str, success: bool = True) -> None:
        """
        Log access to Protected Health Information (PHI).
        
        Parameters:
        * user_id: ID of user accessing data
        * patient_id: ID of patient whose data was accessed
        * data_accessed: List of data fields accessed
        * purpose: Purpose of data access
        * success: Whether access was successful
        """
        access_record = {
            "timestamp": datetime.now().isoformat(),
            "user_id": self._hash_identifier(user_id),
            "patient_id": self._hash_identifier(patient_id),
            "data_accessed": data_accessed,
            "purpose": purpose,
            "success": success,
            "organization": self.organization_name,
            "session_id": str(uuid.uuid4())
        }
        
        self.access_log.append(access_record)
        self.logger.info(f"PHI access logged: User {self._hash_identifier(user_id)} accessed data for patient {self._hash_identifier(patient_id)}")
    
    def detect_potential_breach(self, incident_description: str, affected_individuals: int,
                               data_types: List[str]) -> Dict[str, Any]:
        """
        Assess and document potential HIPAA breach.
        
        Parameters:
        * incident_description: Description of the incident
        * affected_individuals: Number of potentially affected individuals
        * data_types: Types of data potentially compromised
        
        Returns:
        * Breach assessment dictionary
        """
        breach_id = str(uuid.uuid4())
        
        # Determine breach severity
        severity = "low"
        if affected_individuals > 500:
            severity = "high"  # Requires OCR notification
        elif affected_individuals > 100:
            severity = "medium"
        
        # Check if sensitive data types are involved
        sensitive_types = ["ssn", "financial", "diagnosis", "treatment", "genetic"]
        has_sensitive_data = any(data_type in sensitive_types for data_type in data_types)
        
        if has_sensitive_data:
            if severity == "low":
                severity = "medium"
            elif severity == "medium":
                severity = "high"
        
        breach_assessment = {
            "breach_id": breach_id,
            "timestamp": datetime.now().isoformat(),
            "incident_description": incident_description,
            "affected_individuals": affected_individuals,
            "data_types": data_types,
            "severity": severity,
            "requires_ocr_notification": severity == "high",
            "requires_individual_notification": True,
            "notification_deadline": (datetime.now() + timedelta(days=60)).isoformat(),
            "investigation_status": "pending",
            "organization": self.organization_name
        }
        
        self.logger.warning(f"Potential HIPAA breach detected: {breach_id} - Severity: {severity}")
        
        return breach_assessment
    
    def generate_audit_report(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Generate HIPAA audit report for specified date range.
        
        Parameters:
        * start_date: Start date for audit report (ISO format)
        * end_date: End date for audit report (ISO format)
        
        Returns:
        * Comprehensive audit report dictionary
        """
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)
        
        # Filter access logs by date range
        filtered_access_logs = [
            log for log in self.access_log
            if start_dt <= datetime.fromisoformat(log["timestamp"]) <= end_dt
        ]
        
        # Generate summary statistics
        total_access_attempts = len(filtered_access_logs)
        successful_accesses = len([log for log in filtered_access_logs if log["success"]])
        failed_accesses = total_access_attempts - successful_accesses
        
        unique_users = len(set(log["user_id"] for log in filtered_access_logs))
        unique_patients = len(set(log["patient_id"] for log in filtered_access_logs))
        
        audit_report = {
            "report_id": str(uuid.uuid4()),
            "organization": self.organization_name,
            "covered_entity_id": self.covered_entity_id,
            "report_period": {
                "start_date": start_date,
                "end_date": end_date
            },
            "generated_timestamp": datetime.now().isoformat(),
            "summary": {
                "total_access_attempts": total_access_attempts,
                "successful_accesses": successful_accesses,
                "failed_accesses": failed_accesses,
                "unique_users": unique_users,
                "unique_patients_accessed": unique_patients
            },
            "access_logs": filtered_access_logs,
            "compliance_status": "compliant" if failed_accesses == 0 else "requires_review"
        }
        
        return audit_report
    
    def _hash_identifier(self, identifier: str) -> str:
        """Hash sensitive identifiers for logging purposes."""
        return hashlib.sha256(f"{identifier}_{self.covered_entity_id}".encode()).hexdigest()[:16]
    
    def _log_access_attempt(self, validation_result: Dict[str, Any]) -> None:
        """Log minimum necessary validation attempt."""
        self.audit_log.append({
            "type": "minimum_necessary_validation",
            "timestamp": validation_result["timestamp"],
            "details": validation_result
        })
    
    def _log_deidentification(self, original_data: Dict[str, Any], 
                            deidentified_data: Dict[str, Any], 
                            removed_identifiers: List[str]) -> None:
        """Log de-identification process."""
        self.audit_log.append({
            "type": "deidentification",
            "timestamp": datetime.now().isoformat(),
            "removed_identifiers": removed_identifiers,
            "organization": self.organization_name
        })