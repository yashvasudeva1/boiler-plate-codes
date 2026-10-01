# Machine Learning Boilerplate

A comprehensive boilerplate for running both **Supervised** and **Unsupervised** Machine Learning workflows using Streamlit and Scikit-Learn.

---

## Features

### Supervised Learning
- **Multi-Model Support**:
  - **Classification**: Choose between Random Forest, Logistic Regression, SVM (SVC), and Gradient Boosting.
  - **Regression**: Choose between Random Forest, Linear Regression, SVR, and Gradient Boosting.
- **Evaluation & Visualizations**:
  - Classification models output Accuracy, full Classification Report, and an annotated Confusion Matrix heatmap.
  - Regression models output Mean Squared Error (MSE) and R² Score.
  - Tree-based models display Feature Importance plots.
- **Configurable Validation**: Adjust the test size split via a sidebar slider.
- **Download Predictions**: After training, easily download actual vs predicted values as a CSV file.

### Unsupervised Learning
- **Clustering (K-Means)**: 
  - Automatically scales data.
  - Displays an "Elbow Method" chart to help choose optimal k.
  - Calculates the Silhouette Score.
  - Generates a PCA-projected 2D scatter plot if the dataset has more than 2 features.
- **Dimensionality Reduction (PCA)**: Reduces features to principal components. Outputs Explained Variance and a PC1 vs PC2 scatter plot.

### General
- **Missing Data Warning**: Automatically drops NA values and warns the user about the number/percentage of rows dropped.

---

## Prerequisites

- Python 3.8+

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-name>/machine_learning
   ```

2. **Create a Virtual Environment**

   **Windows**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

1. **Upload Dataset**: Upload any `.csv` or `.xlsx` file.
2. **Select Learning Type**: Choose Supervised or Unsupervised learning from the sidebar.
3. **Configure & Train**: Select your target variables and features, tweak model hyperparameters (like number of clusters or test size), and click the train/run button!
