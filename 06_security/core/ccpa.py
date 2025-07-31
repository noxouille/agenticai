# Example code: Implementing CCPA compliance for consumer rights and data privacy

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum


class CCPARequestType(Enum):
    """Enumeration of CCPA consumer request types."""
    KNOW = "know"
    DELETE = "delete"
    OPT_OUT = "opt_out"
    NON_DISCRIMINATION = "non_discrimination"


class CCPAComplianceManager:
    """
    CCPAComplianceManager handles California Consumer Privacy Act compliance
    including consumer rights, data sales opt-out, and deletion requests.
    """

    def __init__(self):
        """
        Initialize the CCPA compliance manager with storage for requests and consumer data.
        """
        self.consumer_requests = {}      # Storage for consumer requests
        self.opt_out_records = {}        # Storage for do-not-sell requests
        self.personal_info = {}          # Storage for personal information
        self.sale_records = {}           # Records of data sales to third parties
        self.data_categories = [         # CCPA-defined categories of personal information
            "identifiers",
            "personal_info_records", 
            "protected_characteristics",
            "commercial_info",
            "biometric_info",
            "internet_activity",
            "geolocation_data",
            "sensory_data",
            "professional_info",
            "education_info",
            "inferences"
        ]

    def submit_consumer_request(self, consumer_id: str, request_type: CCPARequestType, 
                               verification_data: Dict[str, Any], 
                               specific_categories: Optional[List[str]] = None) -> str:
        """
        Submit a consumer request under CCPA rights.

        Parameters:
        * consumer_id: Unique identifier for the consumer
        * request_type: Type of CCPA request (know, delete, opt_out, non_discrimination)
        * verification_data: Data to verify consumer identity
        * specific_categories: Specific categories of data for the request

        Returns:
        * Request ID for tracking
        """
        request_id = f"ccpa_{request_type.value}_{consumer_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        request_record = {
            "request_id": request_id,
            "consumer_id": consumer_id,
            "request_type": request_type.value,
            "submission_date": datetime.now().isoformat(),
            "verification_data": verification_data,
            "specific_categories": specific_categories or [],
            "status": "pending_verification",
            "response_due_date": (datetime.now() + timedelta(days=45)).isoformat(),
            "completed": False,
            "completion_date": None
        }
        
        self.consumer_requests[request_id] = request_record
        return request_id

    def verify_consumer_identity(self, request_id: str, additional_verification: Dict[str, Any]) -> bool:
        """
        Verify consumer identity for CCPA request processing.

        Parameters:
        * request_id: ID of the request to verify
        * additional_verification: Additional verification data

        Returns:
        * True if verification successful, False otherwise
        """
        if request_id not in self.consumer_requests:
            return False
            
        request = self.consumer_requests[request_id]
        
        # Simulate verification process
        required_fields = ["name", "email", "phone"]
        verification_score = 0
        
        for field in required_fields:
            if field in additional_verification:
                verification_score += 1
        
        if verification_score >= 2:  # Require at least 2 matching fields
            request["status"] = "verified"
            request["verification_date"] = datetime.now().isoformat()
            return True
        else:
            request["status"] = "verification_failed"
            return False

    def process_right_to_know(self, consumer_id: str) -> Dict[str, Any]:
        """
        Process consumer's right to know what personal information is collected.

        Parameters:
        * consumer_id: Consumer requesting information

        Returns:
        * Comprehensive report of personal information and processing activities
        """
        consumer_data = self.personal_info.get(consumer_id, {})
        sale_history = [sale for sale in self.sale_records.values() 
                       if sale.get("consumer_id") == consumer_id]
        
        categories_collected = []
        for category in self.data_categories:
            if category in consumer_data:
                categories_collected.append({
                    "category": category,
                    "data_points": list(consumer_data[category].keys()) if isinstance(consumer_data[category], dict) else [str(consumer_data[category])],
                    "source": self._get_collection_source(category),
                    "business_purpose": self._get_business_purpose(category),
                    "third_parties": self._get_third_party_recipients(category)
                })
        
        return {
            "consumer_id": consumer_id,
            "report_date": datetime.now().isoformat(),
            "categories_collected": categories_collected,
            "sources_of_info": self._get_all_sources(),
            "business_purposes": self._get_all_business_purposes(),
            "third_party_recipients": self._get_all_third_parties(),
            "sale_history": sale_history,
            "data_retention_period": "Varies by category, typically 2-7 years",
            "consumer_rights": {
                "right_to_know": "You can request information about data collection",
                "right_to_delete": "You can request deletion of personal information",
                "right_to_opt_out": "You can opt out of sale of personal information",
                "right_to_non_discrimination": "We cannot discriminate for exercising rights"
            }
        }

    def process_deletion_request(self, consumer_id: str, categories_to_delete: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Process consumer's right to delete personal information.

        Parameters:
        * consumer_id: Consumer requesting deletion
        * categories_to_delete: Specific categories to delete (if None, delete all)

        Returns:
        * Deletion report with details of what was deleted
        """
        if consumer_id not in self.personal_info:
            return {
                "consumer_id": consumer_id,
                "status": "no_data_found",
                "deletion_date": datetime.now().isoformat(),
                "deleted_categories": []
            }
        
        consumer_data = self.personal_info[consumer_id]
        deleted_categories = []
        
        if categories_to_delete is None:
            # Delete all data
            categories_to_delete = list(consumer_data.keys())
        
        for category in categories_to_delete:
            if category in consumer_data:
                # Check if deletion is legally permissible
                if self._can_delete_category(category):
                    del consumer_data[category]
                    deleted_categories.append({
                        "category": category,
                        "deletion_status": "completed",
                        "reason": "Consumer request"
                    })
                else:
                    deleted_categories.append({
                        "category": category,
                        "deletion_status": "retained",
                        "reason": "Legal obligation or business necessity"
                    })
        
        # If all categories deleted, remove consumer entirely
        if not consumer_data:
            del self.personal_info[consumer_id]
        
        return {
            "consumer_id": consumer_id,
            "status": "completed",
            "deletion_date": datetime.now().isoformat(),
            "deleted_categories": deleted_categories,
            "retention_reasons": self._get_retention_reasons()
        }

    def process_opt_out_request(self, consumer_id: str) -> str:
        """
        Process consumer's request to opt out of sale of personal information.

        Parameters:
        * consumer_id: Consumer requesting opt-out

        Returns:
        * Opt-out record ID
        """
        opt_out_id = f"optout_{consumer_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        opt_out_record = {
            "opt_out_id": opt_out_id,
            "consumer_id": consumer_id,
            "request_date": datetime.now().isoformat(),
            "status": "active",
            "method": "web_form",
            "scope": "all_personal_information"
        }
        
        self.opt_out_records[opt_out_id] = opt_out_record
        
        # Stop any ongoing sales for this consumer
        self._halt_data_sales(consumer_id)
        
        return opt_out_id

    def check_sale_eligibility(self, consumer_id: str) -> Dict[str, Any]:
        """
        Check if consumer data can be sold based on opt-out status.

        Parameters:
        * consumer_id: Consumer to check

        Returns:
        * Sale eligibility status and details
        """
        active_opt_outs = [
            record for record in self.opt_out_records.values()
            if record["consumer_id"] == consumer_id and record["status"] == "active"
        ]
        
        can_sell = len(active_opt_outs) == 0
        
        return {
            "consumer_id": consumer_id,
            "can_sell_data": can_sell,
            "opt_out_status": "active" if not can_sell else "none",
            "active_opt_outs": active_opt_outs,
            "check_date": datetime.now().isoformat()
        }

    def generate_privacy_policy_disclosures(self) -> Dict[str, Any]:
        """
        Generate CCPA-required privacy policy disclosures.

        Returns:
        * Complete privacy policy disclosures as required by CCPA
        """
        return {
            "effective_date": "2024-01-01",
            "categories_collected": [
                {
                    "category": category,
                    "examples": self._get_category_examples(category),
                    "collected": True,
                    "sold": self._category_is_sold(category),
                    "disclosed": self._category_is_disclosed(category)
                }
                for category in self.data_categories
            ],
            "sources_of_information": [
                "Directly from consumers",
                "From consumer devices and browsers",
                "From third-party vendors and partners",
                "From public records and databases"
            ],
            "business_purposes": [
                "Providing and improving services",
                "Customer support and communication",
                "Marketing and advertising",
                "Legal compliance and fraud prevention",
                "Business operations and analytics"
            ],
            "third_party_categories": [
                "Service providers and vendors",
                "Advertising and marketing partners", 
                "Analytics providers",
                "Legal and professional advisors"
            ],
            "consumer_rights": {
                "right_to_know": "Request information about data collection and use",
                "right_to_delete": "Request deletion of personal information",
                "right_to_opt_out": "Opt out of sale of personal information",
                "right_to_non_discrimination": "Equal service regardless of rights exercise"
            },
            "contact_information": {
                "email": "privacy@company.com",
                "phone": "1-800-PRIVACY",
                "web_form": "https://company.com/ccpa-request"
            }
        }

    def _get_collection_source(self, category: str) -> str:
        """Get the source of data collection for a category."""
        sources = {
            "identifiers": "Direct from consumer",
            "commercial_info": "Transaction records",
            "internet_activity": "Website and app usage",
            "geolocation_data": "Device GPS and IP address"
        }
        return sources.get(category, "Various sources")

    def _get_business_purpose(self, category: str) -> str:
        """Get the business purpose for collecting a category."""
        purposes = {
            "identifiers": "Account management and communication",
            "commercial_info": "Order processing and customer service",
            "internet_activity": "Website optimization and personalization",
            "geolocation_data": "Location-based services"
        }
        return purposes.get(category, "Business operations")

    def _get_third_party_recipients(self, category: str) -> List[str]:
        """Get third-party recipients for a category."""
        return ["Service providers", "Analytics partners"]

    def _get_all_sources(self) -> List[str]:
        """Get all sources of personal information."""
        return ["Direct consumer input", "Website interaction", "Third-party partners"]

    def _get_all_business_purposes(self) -> List[str]:
        """Get all business purposes for data collection."""
        return ["Service provision", "Marketing", "Analytics", "Legal compliance"]

    def _get_all_third_parties(self) -> List[str]:
        """Get all third-party recipients."""
        return ["Cloud service providers", "Marketing platforms", "Analytics services"]

    def _can_delete_category(self, category: str) -> bool:
        """Check if a category can be legally deleted."""
        protected_categories = ["legal_compliance", "fraud_prevention"]
        return category not in protected_categories

    def _get_retention_reasons(self) -> Dict[str, str]:
        """Get reasons for data retention."""
        return {
            "legal_compliance": "Required by law for tax and regulatory purposes",
            "fraud_prevention": "Necessary for security and fraud detection",
            "contract_fulfillment": "Required to complete ongoing services"
        }

    def _halt_data_sales(self, consumer_id: str) -> None:
        """Stop ongoing data sales for a consumer."""
        # Implementation would notify all data buyers to stop using this consumer's data
        pass

    def _get_category_examples(self, category: str) -> List[str]:
        """Get examples of data types in each category."""
        examples = {
            "identifiers": ["Name", "Email", "Phone number", "Account ID"],
            "commercial_info": ["Purchase history", "Payment methods"],
            "internet_activity": ["Browser type", "Pages visited", "Search terms"],
            "geolocation_data": ["GPS coordinates", "IP address location"]
        }
        return examples.get(category, ["Various data points"])

    def _category_is_sold(self, category: str) -> bool:
        """Check if category data is sold to third parties."""
        sold_categories = ["commercial_info", "internet_activity"]
        return category in sold_categories

    def _category_is_disclosed(self, category: str) -> bool:
        """Check if category data is disclosed for business purposes."""
        return True  # Most categories are disclosed to service providers