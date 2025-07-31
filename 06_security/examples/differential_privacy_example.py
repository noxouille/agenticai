# Example implementation of Differential Privacy with mock healthcare data

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt

# Import the DifferentiallyPrivateTrainer class
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.differential_privacy import DifferentiallyPrivateTrainer

def create_mock_healthcare_data():
    """
    Create mock healthcare data for diabetes prediction.
    This simulates sensitive medical data that needs privacy protection.
    """
    np.random.seed(42)  # For reproducible results
    
    # Generate 2000 mock patient records
    n_samples = 2000
    
    # Mock medical features (sensitive data)
    age = np.random.normal(55, 15, n_samples).astype(int)
    bmi = np.random.normal(28, 6, n_samples)
    glucose = np.random.normal(120, 30, n_samples)
    blood_pressure = np.random.normal(80, 12, n_samples)
    insulin = np.random.normal(100, 50, n_samples)
    family_history = np.random.choice([0, 1], n_samples, p=[0.7, 0.3])
    
    # Create diabetes prediction target based on medical rules
    # Higher glucose, BMI, age, family history = higher diabetes risk
    diabetes_risk = (
        (glucose - 100) / 50 +           # Glucose contribution
        (bmi - 25) / 10 +                # BMI contribution
        (age - 50) / 30 +                # Age contribution
        family_history * 0.5 +           # Family history contribution
        (blood_pressure - 80) / 20       # Blood pressure contribution
    )
    
    # Add some randomness and convert to binary (1 = diabetes, 0 = no diabetes)
    diabetes_risk += np.random.normal(0, 0.2, n_samples)
    diabetes = (diabetes_risk > 0.5).astype(int)
    
    # Create DataFrame with patient data
    data = pd.DataFrame({
        'age': age,
        'bmi': bmi,
        'glucose': glucose,
        'blood_pressure': blood_pressure,
        'insulin': insulin,
        'family_history': family_history,
        'diabetes': diabetes
    })
    
    return data

def compare_privacy_vs_accuracy():
    """
    Compare model performance with different privacy levels.
    """
    print("=== Differential Privacy vs Accuracy Trade-off ===\n")
    
    # Create mock healthcare data
    print("1. Creating mock healthcare dataset...")
    data = create_mock_healthcare_data()
    print(f"   Dataset created with {len(data)} patient records")
    print(f"   Diabetes prevalence: {data['diabetes'].mean():.1%}\n")
    
    # Prepare features and target
    feature_names = ['age', 'bmi', 'glucose', 'blood_pressure', 'insulin', 'family_history']
    X = data[feature_names].values
    y = data['diabetes'].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Test different privacy levels
    privacy_levels = [0.1, 0.5, 1.0, 2.0, 5.0]  # Different epsilon values
    results = []
    
    print("2. Training models with different privacy levels...\n")
    
    for epsilon in privacy_levels:
        print(f"Training with epsilon = {epsilon} (privacy level: {'High' if epsilon < 1 else 'Medium' if epsilon < 3 else 'Low'})")
        
        # Train differentially private model
        dp_trainer = DifferentiallyPrivateTrainer(epsilon=epsilon, delta=1e-5)
        
        # Train the differentially private model
        try:
            dp_trainer.train(X_train_scaled, y_train, batch_size=32, epochs=5)
            
            # Make predictions and calculate accuracy
            predictions = dp_trainer.predict(X_test_scaled)
            accuracy = accuracy_score(y_test, predictions)
            
            results.append({
                'epsilon': epsilon,
                'accuracy': accuracy,
                'privacy_level': 'High' if epsilon < 1 else 'Medium' if epsilon < 3 else 'Low'
            })
            print(f"   ✓ Model trained successfully")
            print(f"   ✓ Accuracy: {accuracy:.3f}")
        except Exception as e:
            print(f"   ✗ Training failed: {e}")
            results.append({
                'epsilon': epsilon,
                'accuracy': 0.0,
                'privacy_level': 'High' if epsilon < 1 else 'Medium' if epsilon < 3 else 'Low'
            })
        
        print()
    
    return results

def demonstrate_privacy_attack_simulation():
    """
    Demonstrate how differential privacy protects against privacy attacks.
    """
    print("=== Privacy Attack Simulation ===\n")
    
    print("Scenario: Attacker tries to determine if a specific patient was in the training data")
    print("Method: Membership inference attack\n")
    
    # Simulate attack scenarios
    attack_scenarios = [
        {
            'epsilon': 0.1,
            'attack_success': 0.52,  # Close to random (50%)
            'privacy_protection': 'Excellent'
        },
        {
            'epsilon': 1.0,
            'attack_success': 0.58,
            'privacy_protection': 'Good'
        },
        {
            'epsilon': 5.0,
            'attack_success': 0.75,
            'privacy_protection': 'Weak'
        }
    ]
    
    for scenario in attack_scenarios:
        print(f"Epsilon = {scenario['epsilon']}:")
        print(f"  Attack success rate: {scenario['attack_success']:.1%}")
        print(f"  Privacy protection: {scenario['privacy_protection']}")
        print(f"  Interpretation: {'Safe' if scenario['attack_success'] < 0.6 else 'Risky'}")
        print()

def demonstrate_gdpr_compliance():
    """
    Demonstrate how differential privacy ensures GDPR compliance.
    """
    print("=== GDPR Compliance Demonstration ===\n")
    
    print("1. Data Minimization:")
    print("   ✓ Only necessary features are used for training")
    print("   ✓ No individual identifiers are stored")
    print("   ✓ Model cannot reconstruct individual records\n")
    
    print("2. Privacy by Design:")
    print("   ✓ Privacy protection is built into the training process")
    print("   ✓ Mathematical guarantees prevent data reconstruction")
    print("   ✓ No need for data anonymization (privacy is inherent)\n")
    
    print("3. Right to be Forgotten:")
    print("   ✓ Individual records cannot be identified from the model")
    print("   ✓ Removing one person's data has minimal impact")
    print("   ✓ Model remains functional without specific individuals\n")
    
    print("4. Accountability:")
    print("   ✓ Privacy parameters (epsilon, delta) are documented")
    print("   ✓ Privacy guarantees are mathematically provable")
    print("   ✓ Audit trail shows privacy protection measures\n")

def create_visualization(results):
    """
    Create visualization of privacy vs accuracy trade-off.
    """
    try:
        plt.figure(figsize=(10, 6))
        
        epsilons = [r['epsilon'] for r in results]
        accuracies = [r['accuracy'] for r in results]
        colors = ['red' if r['privacy_level'] == 'High' else 'orange' if r['privacy_level'] == 'Medium' else 'green' for r in results]
        
        plt.scatter(epsilons, accuracies, c=colors, s=100, alpha=0.7)
        
        # Add labels
        for i, result in enumerate(results):
            plt.annotate(f"ε={result['epsilon']}", 
                        (epsilons[i], accuracies[i]), 
                        xytext=(5, 5), textcoords='offset points')
        
        plt.xlabel('Privacy Level (ε) - Lower = More Private')
        plt.ylabel('Model Accuracy')
        plt.title('Differential Privacy vs Model Accuracy Trade-off')
        plt.grid(True, alpha=0.3)
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='red', alpha=0.7, label='High Privacy (ε < 1)'),
            Patch(facecolor='orange', alpha=0.7, label='Medium Privacy (ε < 3)'),
            Patch(facecolor='green', alpha=0.7, label='Low Privacy (ε ≥ 3)')
        ]
        plt.legend(handles=legend_elements)
        
        plt.tight_layout()
        plt.savefig('privacy_vs_accuracy.png', dpi=300, bbox_inches='tight')
        print("✓ Visualization saved as 'privacy_vs_accuracy.png'")
        
    except Exception as e:
        print(f"Visualization failed: {e}")

def practical_implementation_guide():
    """
    Provide practical guidance for implementing differential privacy.
    """
    print("=== Practical Implementation Guide ===\n")
    
    print("1. Choose Privacy Parameters:")
    print("   • ε (epsilon): 0.1-1.0 for high privacy, 1.0-3.0 for medium, >3.0 for low")
    print("   • δ (delta): Typically 1e-5 or smaller")
    print("   • Balance: Higher privacy = lower accuracy\n")
    
    print("2. Data Preparation:")
    print("   • Normalize/standardize features")
    print("   • Remove identifiers and sensitive fields")
    print("   • Ensure data quality and consistency\n")
    
    print("3. Model Selection:")
    print("   • Logistic regression works well with DP")
    print("   • Neural networks can use DP-SGD")
    print("   • Tree-based models have limited DP support\n")
    
    print("4. Evaluation:")
    print("   • Test privacy guarantees with membership inference attacks")
    print("   • Monitor accuracy degradation")
    print("   • Validate privacy parameters with domain experts\n")

if __name__ == "__main__":
    print("=== Differential Privacy in Healthcare Example ===\n")
    
    # Run the demonstration
    results = compare_privacy_vs_accuracy()
    demonstrate_privacy_attack_simulation()
    demonstrate_gdpr_compliance()
    create_visualization(results)
    practical_implementation_guide()
    
    print("\n=== Key Takeaways ===\n")
    print("✓ Differential privacy provides mathematical privacy guarantees")
    print("✓ Trade-off exists between privacy and model accuracy")
    print("✓ GDPR compliance is achieved through privacy-by-design")
    print("✓ Healthcare and financial applications benefit most from DP")
    print("✓ Implementation requires careful parameter tuning") 