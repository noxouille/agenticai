# Example code: Implementing PIPEDA compliance for data access and consent management

import json
from datetime import datetime
from typing import Dict, List, Optional, Any


class PIPEDAComplianceManager:
    """
    PIPEDAComplianceManager handles Personal Information Protection and Electronic Documents Act
    compliance including consent management, access requests, and data portability.
    """

    def __init__(self):
        """
        Initialize the PIPEDA compliance manager with storage for consents and data requests.
        """
        self.consent_records = {}  # Storage for consent records
        self.data_requests = {}    # Storage for data access requests
        self.data_store = {}       # Simulated personal data storage

    def record_consent(self, user_id: str, purpose: str, data_types: List[str], 
                      consent_given: bool, method: str = "explicit") -> str:
        """
        Record user consent for data collection under PIPEDA requirements.

        Parameters:
        * user_id: Unique identifier for the user
        * purpose: Clear description of why data is being collected
        * data_types: List of data types being collected
        * consent_given: Whether consent was granted
        * method: Method of consent collection (explicit, implied, opt-in)

        Returns:
        * Consent record ID
        """
        consent_id = f"consent_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        consent_record = {
            "consent_id": consent_id,
            "user_id": user_id,
            "purpose": purpose,
            "data_types": data_types,
            "consent_given": consent_given,
            "method": method,
            "timestamp": datetime.now().isoformat(),
            "withdrawn": False,
            "withdrawal_date": None
        }
        
        self.consent_records[consent_id] = consent_record
        return consent_id

    def withdraw_consent(self, user_id: str, consent_id: str) -> bool:
        """
        Allow user to withdraw consent as required by PIPEDA.

        Parameters:
        * user_id: User requesting withdrawal
        * consent_id: ID of consent to withdraw

        Returns:
        * True if withdrawal successful, False otherwise
        """
        if consent_id in self.consent_records:
            record = self.consent_records[consent_id]
            if record["user_id"] == user_id:
                record["withdrawn"] = True
                record["withdrawal_date"] = datetime.now().isoformat()
                return True
        return False

    def process_access_request(self, user_id: str, request_type: str = "access") -> Dict[str, Any]:
        """
        Process user's right to access their personal information under PIPEDA.

        Parameters:
        * user_id: User making the request
        * request_type: Type of request (access, correction, deletion)

        Returns:
        * Dictionary containing user's data and processing information
        """
        request_id = f"req_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Simulate data retrieval
        user_data = self.data_store.get(user_id, {})
        
        # Get consent history for this user
        user_consents = [
            record for record in self.consent_records.values() 
            if record["user_id"] == user_id
        ]
        
        response = {
            "request_id": request_id,
            "user_id": user_id,
            "request_type": request_type,
            "request_date": datetime.now().isoformat(),
            "personal_data": user_data,
            "consent_history": user_consents,
            "data_retention_info": self._get_retention_info(user_id),
            "third_party_disclosures": self._get_disclosure_info(user_id)
        }
        
        self.data_requests[request_id] = response
        return response

    def check_consent_validity(self, user_id: str, purpose: str) -> Dict[str, Any]:
        """
        Check if valid consent exists for a specific purpose.

        Parameters:
        * user_id: User to check consent for
        * purpose: Purpose to verify consent for

        Returns:
        * Dictionary with consent status and details
        """
        valid_consents = []
        
        for record in self.consent_records.values():
            if (record["user_id"] == user_id and 
                purpose in record["purpose"] and 
                record["consent_given"] and 
                not record["withdrawn"]):
                valid_consents.append(record)
        
        return {
            "user_id": user_id,
            "purpose": purpose,
            "has_valid_consent": len(valid_consents) > 0,
            "consent_records": valid_consents,
            "check_timestamp": datetime.now().isoformat()
        }

    def generate_privacy_report(self, user_id: str) -> Dict[str, Any]:
        """
        Generate comprehensive privacy report for user as required by PIPEDA.

        Parameters:
        * user_id: User to generate report for

        Returns:
        * Complete privacy report including all data processing activities
        """
        user_consents = [
            record for record in self.consent_records.values() 
            if record["user_id"] == user_id
        ]
        
        user_requests = [
            request for request in self.data_requests.values() 
            if request["user_id"] == user_id
        ]
        
        return {
            "user_id": user_id,
            "report_date": datetime.now().isoformat(),
            "data_collected": list(self.data_store.get(user_id, {}).keys()),
            "consent_status": user_consents,
            "access_requests": user_requests,
            "retention_policy": "Data retained for maximum 7 years as per PIPEDA guidelines",
            "contact_info": {
                "privacy_officer": "privacy@company.com",
                "phone": "1-800-PRIVACY",
                "address": "123 Privacy St, Toronto, ON"
            }
        }

    def _get_retention_info(self, user_id: str) -> Dict[str, str]:
        """
        Get data retention information for user.
        """
        return {
            "policy": "Personal data retained for business purposes only",
            "max_retention": "7 years",
            "deletion_schedule": "Automatic deletion after retention period"
        }

    def _get_disclosure_info(self, user_id: str) -> List[Dict[str, str]]:
        """
        Get information about third-party disclosures.
        """
        return [
            {
                "recipient": "Analytics Service Provider",
                "purpose": "Website performance analysis",
                "date": "2024-01-15",
                "consent_basis": "Explicit consent for analytics"
            }
        ]

    def export_user_data(self, user_id: str, format_type: str = "json") -> str:
        """
        Export user data in portable format as required by PIPEDA.

        Parameters:
        * user_id: User whose data to export
        * format_type: Export format (json, csv, xml)

        Returns:
        * Exported data as string
        """
        user_data = self.process_access_request(user_id, "export")
        
        if format_type.lower() == "json":
            return json.dumps(user_data, indent=2)
        elif format_type.lower() == "csv":
            # Simplified CSV export
            csv_data = "field,value\n"
            for key, value in user_data.get("personal_data", {}).items():
                csv_data += f"{key},{value}\n"
            return csv_data
        else:
            return str(user_data)