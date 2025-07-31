# PIPEDA Compliance Example: E-commerce Platform Implementation

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from pipeda import PIPEDAComplianceManager
from datetime import datetime
import json


def demonstrate_pipeda_compliance():
    """
    Demonstrate PIPEDA compliance implementation for an e-commerce platform.
    This example shows consent management, access requests, and data portability.
    """
    print("=== PIPEDA Compliance Example: E-commerce Platform ===\n")
    
    # Initialize PIPEDA compliance manager
    pipeda_manager = PIPEDAComplianceManager()
    
    # Simulate user data
    user_id = "user_12345"
    pipeda_manager.data_store[user_id] = {
        "name": "Sarah Chen",
        "email": "sarah.chen@email.com",
        "phone": "+1-416-555-0123",
        "address": "123 Maple Street, Toronto, ON M5V 3A1",
        "purchase_history": ["Order #1001", "Order #1045", "Order #1099"],
        "preferences": {"newsletter": True, "marketing_emails": False}
    }
    
    print("1. Recording Initial Consent")
    print("-" * 40)
    
    # Record consent for different purposes
    marketing_consent = pipeda_manager.record_consent(
        user_id=user_id,
        purpose="Email marketing and promotional offers",
        data_types=["name", "email", "purchase_history"],
        consent_given=True,
        method="explicit"
    )
    print(f"Marketing consent recorded: {marketing_consent}")
    
    analytics_consent = pipeda_manager.record_consent(
        user_id=user_id,
        purpose="Website analytics and performance improvement",
        data_types=["browsing_behavior", "device_info"],
        consent_given=True,
        method="implied"
    )
    print(f"Analytics consent recorded: {analytics_consent}")
    
    print("\n2. Checking Consent Validity")
    print("-" * 40)
    
    # Check if we have valid consent for marketing
    marketing_check = pipeda_manager.check_consent_validity(
        user_id=user_id,
        purpose="Email marketing"
    )
    print(f"Marketing consent valid: {marketing_check['has_valid_consent']}")
    print(f"Number of valid consents: {len(marketing_check['consent_records'])}")
    
    print("\n3. Processing Data Access Request")
    print("-" * 40)
    
    # User requests access to their personal data
    access_response = pipeda_manager.process_access_request(
        user_id=user_id,
        request_type="access"
    )
    
    print(f"Access request ID: {access_response['request_id']}")
    print(f"Personal data categories: {list(access_response['personal_data'].keys())}")
    print(f"Number of consent records: {len(access_response['consent_history'])}")
    
    print("\n4. Generating Privacy Report")
    print("-" * 40)
    
    # Generate comprehensive privacy report
    privacy_report = pipeda_manager.generate_privacy_report(user_id)
    print(f"Privacy report generated for: {privacy_report['user_id']}")
    print(f"Data collected: {privacy_report['data_collected']}")
    print(f"Retention policy: {privacy_report['retention_policy']}")
    print(f"Privacy officer contact: {privacy_report['contact_info']['privacy_officer']}")
    
    print("\n5. Data Export (Right to Portability)")
    print("-" * 40)
    
    # Export user data in JSON format
    json_export = pipeda_manager.export_user_data(user_id, "json")
    print("JSON export sample (first 200 characters):")
    print(json_export[:200] + "..." if len(json_export) > 200 else json_export)
    
    # Export in CSV format
    csv_export = pipeda_manager.export_user_data(user_id, "csv")
    print("\nCSV export sample:")
    print(csv_export[:150] + "..." if len(csv_export) > 150 else csv_export)
    
    print("\n6. Consent Withdrawal")
    print("-" * 40)
    
    # User decides to withdraw marketing consent
    withdrawal_success = pipeda_manager.withdraw_consent(user_id, marketing_consent)
    print(f"Marketing consent withdrawal: {'Successful' if withdrawal_success else 'Failed'}")
    
    # Check consent validity after withdrawal
    post_withdrawal_check = pipeda_manager.check_consent_validity(
        user_id=user_id,
        purpose="Email marketing"
    )
    print(f"Marketing consent valid after withdrawal: {post_withdrawal_check['has_valid_consent']}")
    
    print("\n7. Business Impact Analysis")
    print("-" * 40)
    
    # Analyze impact of consent changes on business operations
    remaining_consents = [
        record for record in pipeda_manager.consent_records.values()
        if record["user_id"] == user_id and not record["withdrawn"]
    ]
    
    print(f"Remaining active consents: {len(remaining_consents)}")
    for consent in remaining_consents:
        print(f"  - {consent['purpose']} (Method: {consent['method']})")
    
    print("\n=== PIPEDA Compliance Demonstration Complete ===")


def demonstrate_data_breach_response():
    """
    Demonstrate PIPEDA-compliant data breach response procedures.
    """
    print("\n=== PIPEDA Data Breach Response Example ===\n")
    
    pipeda_manager = PIPEDAComplianceManager()
    
    # Simulate affected users
    affected_users = ["user_001", "user_002", "user_003"]
    
    print("1. Data Breach Notification Process")
    print("-" * 40)
    
    breach_details = {
        "incident_id": "BREACH_2024_001",
        "discovery_date": datetime.now().isoformat(),
        "affected_users": len(affected_users),
        "data_types": ["email", "name", "phone"],
        "cause": "Unauthorized access to customer database",
        "containment_actions": ["Database access revoked", "Passwords reset", "Security audit initiated"],
        "risk_assessment": "Medium - No financial information compromised"
    }
    
    print(f"Breach ID: {breach_details['incident_id']}")
    print(f"Affected users: {breach_details['affected_users']}")
    print(f"Data types involved: {', '.join(breach_details['data_types'])}")
    print(f"Risk level: {breach_details['risk_assessment']}")
    
    print("\n2. Individual Notifications")
    print("-" * 40)
    
    # Generate individual breach notifications
    for user_id in affected_users:
        notification = {
            "user_id": user_id,
            "notification_date": datetime.now().isoformat(),
            "breach_summary": "Your personal information may have been accessed without authorization",
            "affected_data": breach_details["data_types"],
            "actions_taken": breach_details["containment_actions"],
            "user_actions": [
                "Monitor your accounts for suspicious activity",
                "Consider changing passwords on other accounts",
                "Contact us with any concerns"
            ],
            "contact_info": "privacy@company.com or 1-800-PRIVACY"
        }
        
        print(f"Notification sent to {user_id}")
        print(f"  Affected data: {', '.join(notification['affected_data'])}")
    
    print("\n=== Data Breach Response Complete ===")


if __name__ == "__main__":
    # Run the main PIPEDA compliance demonstration
    demonstrate_pipeda_compliance()
    
    # Run the data breach response demonstration
    demonstrate_data_breach_response()
    
    print("\n" + "="*60)
    print("PIPEDA Implementation Key Takeaways:")
    print("="*60)
    print("• Explicit consent required for sensitive personal information")
    print("• Users must be able to access and correct their information")
    print("• Data portability enables users to transfer their data")
    print("• Consent can be withdrawn at any time")
    print("• Organizations must have a privacy officer")
    print("• Data breach notifications required within 72 hours")
    print("• Personal information must be protected with appropriate safeguards")
    print("="*60)