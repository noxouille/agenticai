# CCPA Compliance Example: Social Media Platform Implementation

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from ccpa import CCPAComplianceManager, CCPARequestType
from datetime import datetime
import json


def demonstrate_ccpa_compliance():
    """
    Demonstrate CCPA compliance implementation for a social media platform.
    This example shows consumer rights, data sales opt-out, and deletion requests.
    """
    print("=== CCPA Compliance Example: Social Media Platform ===\n")
    
    # Initialize CCPA compliance manager
    ccpa_manager = CCPAComplianceManager()
    
    # Simulate consumer data
    consumer_id = "consumer_98765"
    ccpa_manager.personal_info[consumer_id] = {
        "identifiers": {
            "name": "Alex Rodriguez",
            "email": "alex.rodriguez@email.com",
            "phone": "+1-213-555-0199",
            "username": "alex_rod_2024"
        },
        "commercial_info": {
            "subscription_type": "Premium",
            "payment_method": "Credit Card ending in 4567",
            "purchase_history": ["Premium upgrade", "Extra storage", "Ad removal"]
        },
        "internet_activity": {
            "posts_created": 1247,
            "likes_given": 8934,
            "pages_followed": ["TechNews", "Photography", "Travel"],
            "search_history": ["vacation destinations", "camera reviews", "programming tutorials"]
        },
        "geolocation_data": {
            "current_location": "Los Angeles, CA",
            "location_history": ["San Francisco, CA", "Seattle, WA", "Portland, OR"]
        }
    }
    
    # Simulate some data sales
    ccpa_manager.sale_records["sale_001"] = {
        "consumer_id": consumer_id,
        "buyer": "MarketingCorp Inc.",
        "date": "2024-01-15",
        "categories_sold": ["commercial_info", "internet_activity"],
        "purpose": "Targeted advertising"
    }
    
    print("1. Consumer Right to Know Request")
    print("-" * 40)
    
    # Submit a right to know request
    know_request_id = ccpa_manager.submit_consumer_request(
        consumer_id=consumer_id,
        request_type=CCPARequestType.KNOW,
        verification_data={"name": "Alex Rodriguez", "email": "alex.rodriguez@email.com"}
    )
    print(f"Right to know request submitted: {know_request_id}")
    
    # Verify consumer identity
    verification_success = ccpa_manager.verify_consumer_identity(
        request_id=know_request_id,
        additional_verification={"phone": "+1-213-555-0199", "username": "alex_rod_2024"}
    )
    print(f"Identity verification: {'Successful' if verification_success else 'Failed'}")
    
    # Process the right to know request
    if verification_success:
        know_response = ccpa_manager.process_right_to_know(consumer_id)
        print(f"Categories of data collected: {len(know_response['categories_collected'])}")
        
        print("\nData Categories and Details:")
        for category in know_response['categories_collected'][:3]:  # Show first 3
            print(f"  • {category['category']}: {len(category['data_points'])} data points")
            print(f"    Source: {category['source']}")
            print(f"    Purpose: {category['business_purpose']}")
        
        print(f"\nData sales to third parties: {len(know_response['sale_history'])}")
        if know_response['sale_history']:
            for sale in know_response['sale_history']:
                print(f"  • Sold to {sale['buyer']} on {sale['date']}")
    
    print("\n2. Opt-Out of Sale Request")
    print("-" * 40)
    
    # Consumer opts out of data sales
    opt_out_id = ccpa_manager.process_opt_out_request(consumer_id)
    print(f"Opt-out request processed: {opt_out_id}")
    
    # Check sale eligibility after opt-out
    sale_eligibility = ccpa_manager.check_sale_eligibility(consumer_id)
    print(f"Can sell consumer data: {sale_eligibility['can_sell_data']}")
    print(f"Opt-out status: {sale_eligibility['opt_out_status']}")
    
    print("\n3. Right to Delete Request")
    print("-" * 40)
    
    # Submit deletion request for specific categories
    delete_request_id = ccpa_manager.submit_consumer_request(
        consumer_id=consumer_id,
        request_type=CCPARequestType.DELETE,
        verification_data={"name": "Alex Rodriguez", "email": "alex.rodriguez@email.com"},
        specific_categories=["internet_activity", "geolocation_data"]
    )
    print(f"Deletion request submitted: {delete_request_id}")
    
    # Verify and process deletion
    delete_verification = ccpa_manager.verify_consumer_identity(
        request_id=delete_request_id,
        additional_verification={"phone": "+1-213-555-0199"}
    )
    
    if delete_verification:
        deletion_response = ccpa_manager.process_deletion_request(
            consumer_id=consumer_id,
            categories_to_delete=["internet_activity", "geolocation_data"]
        )
        
        print(f"Deletion status: {deletion_response['status']}")
        print("Deleted categories:")
        for category in deletion_response['deleted_categories']:
            print(f"  • {category['category']}: {category['deletion_status']}")
            if category['deletion_status'] == 'retained':
                print(f"    Reason: {category['reason']}")
    
    print("\n4. Non-Discrimination Verification")
    print("-" * 40)
    
    # Demonstrate that services continue normally after rights exercise
    remaining_data = ccpa_manager.personal_info.get(consumer_id, {})
    print(f"Remaining data categories: {list(remaining_data.keys())}")
    print("Service level maintained: Premium features still available")
    print("Account status: Active and in good standing")
    print("No penalties applied for exercising CCPA rights")
    
    print("\n=== CCPA Consumer Rights Demonstration Complete ===")


def demonstrate_ccpa_privacy_policy():
    """
    Demonstrate CCPA privacy policy disclosure requirements.
    """
    print("\n=== CCPA Privacy Policy Disclosures ===\n")
    
    ccpa_manager = CCPAComplianceManager()
    
    # Generate privacy policy disclosures
    privacy_disclosures = ccpa_manager.generate_privacy_policy_disclosures()
    
    print("1. Categories of Personal Information")
    print("-" * 40)
    
    collected_categories = [cat for cat in privacy_disclosures['categories_collected'] if cat['collected']]
    print(f"We collect {len(collected_categories)} categories of personal information:")
    
    for category in collected_categories[:5]:  # Show first 5
        print(f"\n• {category['category'].replace('_', ' ').title()}:")
        print(f"  Examples: {', '.join(category['examples'][:3])}")
        print(f"  Sold to third parties: {'Yes' if category['sold'] else 'No'}")
        print(f"  Disclosed for business purposes: {'Yes' if category['disclosed'] else 'No'}")
    
    print(f"\n2. Business Purposes ({len(privacy_disclosures['business_purposes'])} total)")
    print("-" * 40)
    for purpose in privacy_disclosures['business_purposes']:
        print(f"• {purpose}")
    
    print(f"\n3. Third-Party Categories ({len(privacy_disclosures['third_party_categories'])} total)")
    print("-" * 40)
    for category in privacy_disclosures['third_party_categories']:
        print(f"• {category}")
    
    print("\n4. Consumer Rights Summary")
    print("-" * 40)
    for right, description in privacy_disclosures['consumer_rights'].items():
        right_name = right.replace('_', ' ').title()
        print(f"• {right_name}: {description}")
    
    print("\n5. Contact Information")
    print("-" * 40)
    contact = privacy_disclosures['contact_information']
    print(f"Email: {contact['email']}")
    print(f"Phone: {contact['phone']}")
    print(f"Web Form: {contact['web_form']}")


def demonstrate_ccpa_data_mapping():
    """
    Demonstrate data mapping and inventory for CCPA compliance.
    """
    print("\n=== CCPA Data Mapping Example ===\n")
    
    ccpa_manager = CCPAComplianceManager()
    
    # Create sample data inventory
    data_inventory = {
        "user_profiles": {
            "categories": ["identifiers", "personal_info_records"],
            "retention": "Account lifetime + 2 years",
            "third_party_sharing": ["Cloud storage provider"],
            "sale_status": "Not sold"
        },
        "behavioral_analytics": {
            "categories": ["internet_activity", "inferences"],
            "retention": "2 years",
            "third_party_sharing": ["Analytics platform", "Advertising network"],
            "sale_status": "Sold for advertising"
        },
        "transaction_records": {
            "categories": ["commercial_info", "identifiers"],
            "retention": "7 years (tax requirements)",
            "third_party_sharing": ["Payment processor", "Accounting firm"],
            "sale_status": "Not sold"
        },
        "location_services": {
            "categories": ["geolocation_data"],
            "retention": "30 days",
            "third_party_sharing": ["Map service provider"],
            "sale_status": "Shared but not sold"
        }
    }
    
    print("Data System Inventory:")
    print("-" * 40)
    
    for system, details in data_inventory.items():
        print(f"\n{system.replace('_', ' ').title()}:")
        print(f"  CCPA Categories: {', '.join(details['categories'])}")
        print(f"  Retention Period: {details['retention']}")
        print(f"  Third-Party Sharing: {', '.join(details['third_party_sharing'])}")
        print(f"  Sale Status: {details['sale_status']}")
    
    print("\n" + "="*50)
    print("CCPA Compliance Checklist:")
    print("="*50)
    print("✓ Privacy policy updated with CCPA disclosures")
    print("✓ Consumer request portal implemented")
    print("✓ Identity verification process established")
    print("✓ Data deletion procedures documented")
    print("✓ Opt-out mechanism for data sales")
    print("✓ Non-discrimination policy in place")
    print("✓ Employee training on CCPA requirements")
    print("✓ Data inventory and mapping completed")
    print("="*50)


if __name__ == "__main__":
    # Run the main CCPA compliance demonstration
    demonstrate_ccpa_compliance()
    
    # Demonstrate privacy policy disclosures
    demonstrate_ccpa_privacy_policy()
    
    # Demonstrate data mapping
    demonstrate_ccpa_data_mapping()
    
    print("\n" + "="*60)
    print("CCPA Implementation Key Takeaways:")
    print("="*60)
    print("• Consumers have the right to know what data is collected")
    print("• Consumers can request deletion of personal information")
    print("• Consumers can opt out of sale of personal information")
    print("• No discrimination for exercising CCPA rights")
    print("• Identity verification required for sensitive requests")
    print("• 45-day response time for consumer requests")
    print("• Privacy policy must include detailed disclosures")
    print("• 'Do Not Sell My Personal Information' link required")
    print("="*60)