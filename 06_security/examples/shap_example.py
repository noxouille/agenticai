# Section: SHAP for Model Explanation
import shap
import xgboost
import numpy as np

# Generate sample data and train an XGBoost model.
X, y = np.random.rand(100, 5), np.random.randint(2, size=100)
model = xgboost.XGBClassifier().fit(X, y)

# Initialize SHAP explainer for the trained model.
explainer = shap.Explainer(model)
# Compute SHAP values for the first instance.
shap_values = explainer(X[:1])
# Display SHAP summary plot.
shap.summary_plot(shap_values)