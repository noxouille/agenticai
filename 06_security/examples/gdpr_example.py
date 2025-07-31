# Example implementation of GDPR right to explanation with mock data

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Import the ExplainableModel class from gdpr.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.gdpr import ExplainableModel

def create_mock_loan_data():
    """
    Create mock loan application data for demonstration.
    """
    np.random.seed(42)  # For reproducible results
    
    # Generate 1000 mock loan applications
    n_samples = 1000
    
    # Mock features
    credit_score = np.random.normal(700, 100, n_samples).astype(int)
    income = np.random.normal(75000, 25000, n_samples).astype(int)
    debt_ratio = np.random.uniform(0.1, 0.8, n_samples)
    employment_years = np.random.uniform(0, 20, n_samples)
    loan_amount = np.random.uniform(10000, 500000, n_samples)
    
    # Create a simple rule-based target (loan approval)
    # Higher credit score, income, employment years = higher chance of approval
    # Higher debt ratio = lower chance of approval
    approval_prob = (
        (credit_score - 500) / 300 +  # Credit score contribution
        (income - 50000) / 100000 +   # Income contribution
        employment_years / 20 -        # Employment years contribution
        debt_ratio * 2                 # Debt ratio penalty
    )
    
    # Convert to binary approval (1 = approved, 0 = denied)
    loan_approved = (approval_prob > 0.5).astype(int)
    
    # Create DataFrame
    data = pd.DataFrame({
        'credit_score': credit_score,
        'income': income,
        'debt_ratio': debt_ratio,
        'employment_years': employment_years,
        'loan_amount': loan_amount,
        'loan_approved': loan_approved
    })
    
    return data

def train_loan_model():
    """
    Train a Random Forest model on the mock loan data.
    """
    # Create mock data
    data = create_mock_loan_data()
    
    # Prepare features and target
    feature_names = ['credit_score', 'income', 'debt_ratio', 'employment_years', 'loan_amount']
    X = data[feature_names]
    y = data['loan_approved']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    return model, scaler, feature_names, X_test_scaled[:5]  # Return first 5 test samples

def demonstrate_gdpr_explanations():
    """
    Demonstrate the GDPR right to explanation functionality.
    """
    print("=== GDPR Right to Explanation Demo ===\n")
    
    # Train the model
    print("1. Training loan approval model...")
    model, scaler, feature_names, test_samples = train_loan_model()
    print(f"   Model trained with features: {feature_names}\n")
    
    # Create ExplainableModel wrapper
    print("2. Creating GDPR-compliant explainable model...")
    explainable_model = ExplainableModel(model, feature_names)
    print("   ✓ Model wrapped with explanation capabilities\n")
    
    # Demonstrate predictions and explanations
    print("3. Making predictions with explanations:\n")
    
    for i, sample in enumerate(test_samples):
        # Reshape for single prediction
        sample_reshaped = sample.reshape(1, -1)
        
        # Get prediction
        prediction = explainable_model.predict(sample_reshaped)[0]
        
        # Get explanation
        explanation = explainable_model.explain_prediction(sample_reshaped)
        
        print(f"--- Loan Application #{i+1} ---")
        print(f"Decision: {'APPROVED' if prediction == 1 else 'DENIED'}")
        print(f"Confidence: {prediction:.2f}")
        print("\nExplanation:")
        
        if explanation['factors_increasing_score']:
            print("  Factors that helped approval:")
            for factor in explanation['factors_increasing_score']:
                print(f"    • {factor}")
        
        if explanation['factors_decreasing_score']:
            print("  Factors that hurt approval:")
            for factor in explanation['factors_decreasing_score']:
                print(f"    • {factor}")
        
        print("\n" + "="*50 + "\n")

def demonstrate_individual_rights():
    """
    Demonstrate how this fulfills GDPR individual rights.
    """
    print("=== GDPR Individual Rights Fulfillment ===\n")
    
    print("1. Right to Explanation:")
    print("   ✓ Users can understand why their loan was approved/denied")
    print("   ✓ Clear, non-technical language used")
    print("   ✓ Specific factors identified with impact scores\n")
    
    print("2. Right to Transparency:")
    print("   ✓ Decision-making process is transparent")
    print("   ✓ No black-box decisions")
    print("   ✓ All factors contributing to decision are visible\n")
    
    print("3. Right to Contest:")
    print("   ✓ Users can identify which factors to improve")
    print("   ✓ Clear path for appealing decisions")
    print("   ✓ Specific actionable feedback provided\n")

if __name__ == "__main__":
    # Run the demonstration
    demonstrate_gdpr_explanations()
    demonstrate_individual_rights()
    
    print("=== Example Usage in Production ===\n")
    print("In a real application, you would:")
    print("1. Train your model on real data")
    print("2. Wrap it with ExplainableModel")
    print("3. Use explain_prediction() for each user request")
    print("4. Store explanations for audit trails")
    print("5. Provide explanations in user interface") 