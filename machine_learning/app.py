import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, mean_squared_error, silhouette_score, classification_report, confusion_matrix, r2_score

st.set_page_config(page_title="Machine Learning Boilerplate", page_icon="🤖", layout="wide")

st.title("🤖 Machine Learning Boilerplate")
st.write("Upload a dataset to train Supervised or Unsupervised Machine Learning models.")

with st.sidebar:
    st.header("Settings")
    learning_type = st.selectbox(
        "Select Learning Type", 
        ["Supervised Learning", "Unsupervised Learning"]
    )
    
uploaded_file = st.file_uploader("Upload your dataset (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file is not None:
    @st.cache_data
    def load_data(file):
        """Loads data from a CSV or Excel file."""
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        else:
            return pd.read_excel(file)
            
    df = load_data(uploaded_file)
    st.write("### Data Preview")
    st.dataframe(df.head())
    
    missing_rows = df.isna().any(axis=1).sum()
    total_rows = len(df)
    if missing_rows > 0:
        missing_pct = (missing_rows / total_rows) * 100
        st.warning(f"Dropped {missing_rows} rows with missing values ({missing_pct:.2f}% of dataset).")
    
    df = df.dropna()
    
    if learning_type == "Supervised Learning":
        st.subheader("Supervised Learning")
        task_type = st.sidebar.selectbox("Task Type", ["Classification", "Regression"])
        test_size = st.sidebar.slider("Test Size", min_value=0.1, max_value=0.5, value=0.2, step=0.05)
        
        if task_type == "Classification":
            model_name = st.sidebar.selectbox("Select Model", ["Random Forest", "Logistic Regression", "SVM (SVC)", "Gradient Boosting"])
        else:
            model_name = st.sidebar.selectbox("Select Model", ["Random Forest", "Linear Regression", "SVR", "Gradient Boosting"])

        col1, col2 = st.columns(2)
        with col1:
            target_col = st.selectbox("Select Target Column", df.columns)
        with col2:
            feature_cols = st.multiselect(
                "Select Feature Columns", 
                [col for col in df.columns if col != target_col], 
                default=[col for col in df.columns if col != target_col][:5]
            )
        
        if st.button("Train Model"):
            if not feature_cols:
                st.error("Please select at least one feature column.")
            else:
                with st.spinner(f"Training {model_name} {task_type} model..."):
                    X = df[feature_cols]
                    y = df[target_col]
                    
                    if task_type == "Classification" and y.dtype == 'object':
                        le = LabelEncoder()
                        y = le.fit_transform(y)
                        
                    X = pd.get_dummies(X, drop_first=True)
                    
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
                    
                    if task_type == "Classification":
                        if model_name == "Random Forest":
                            model = RandomForestClassifier(random_state=42)
                        elif model_name == "Logistic Regression":
                            model = LogisticRegression(random_state=42, max_iter=1000)
                        elif model_name == "SVM (SVC)":
                            model = SVC(random_state=42)
                        elif model_name == "Gradient Boosting":
                            model = GradientBoostingClassifier(random_state=42)
                            
                        model.fit(X_train, y_train)
                        preds = model.predict(X_test)
                        acc = accuracy_score(y_test, preds)
                        st.success(f"Model Trained! Accuracy: {acc:.4f}")
                        
                        st.write("### Classification Report")
                        st.code(classification_report(y_test, preds))
                        
                        st.write("### Confusion Matrix")
                        cm = confusion_matrix(y_test, preds)
                        fig, ax = plt.subplots(figsize=(6, 4))
                        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
                        st.pyplot(fig)
                    else:
                        if model_name == "Random Forest":
                            model = RandomForestRegressor(random_state=42)
                        elif model_name == "Linear Regression":
                            model = LinearRegression()
                        elif model_name == "SVR":
                            model = SVR()
                        elif model_name == "Gradient Boosting":
                            model = GradientBoostingRegressor(random_state=42)

                        model.fit(X_train, y_train)
                        preds = model.predict(X_test)
                        mse = mean_squared_error(y_test, preds)
                        r2 = r2_score(y_test, preds)
                        st.success(f"Model Trained! Mean Squared Error: {mse:.4f} | R² Score: {r2:.4f}")
                        
                    if model_name in ["Random Forest", "Gradient Boosting"]:
                        st.write("### Feature Importance")
                        importance = pd.DataFrame(
                            {"Feature": X.columns, "Importance": model.feature_importances_}
                        ).sort_values(by="Importance", ascending=False).head(10)
                        
                        fig, ax = plt.subplots(figsize=(10, 5))
                        sns.barplot(x="Importance", y="Feature", data=importance, ax=ax)
                        st.pyplot(fig)
                        
                    results_df = pd.DataFrame({"Actual": y_test, "Predicted": preds})
                    csv = results_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download Predictions",
                        data=csv,
                        file_name='predictions.csv',
                        mime='text/csv',
                    )

    else:
        st.subheader("Unsupervised Learning")
        task_type = st.sidebar.selectbox("Task Type", ["Clustering (K-Means)", "Dimensionality Reduction (PCA)"])
        
        feature_cols = st.multiselect("Select Feature Columns", df.columns, default=list(df.columns)[:5])
        
        if st.button("Run Unsupervised Algorithm"):
            if not feature_cols:
                st.error("Please select at least one feature column.")
            else:
                with st.spinner(f"Running {task_type}..."):
                    X = df[feature_cols]
                    X = pd.get_dummies(X, drop_first=True)
                    
                    scaler = StandardScaler()
                    X_scaled = scaler.fit_transform(X)
                    
                    if task_type == "Clustering (K-Means)":
                        st.write("### Elbow Method")
                        inertias = []
                        max_k = min(10, len(X))
                        if max_k > 2:
                            k_range = range(2, max_k + 1)
                            for i in k_range:
                                km = KMeans(n_clusters=i, random_state=42)
                                km.fit(X_scaled)
                                inertias.append(km.inertia_)
                                
                            fig, ax = plt.subplots(figsize=(8, 4))
                            ax.plot(k_range, inertias, marker='o')
                            ax.set_xlabel("Number of Clusters (k)")
                            ax.set_ylabel("Inertia")
                            ax.set_title("Elbow Method for Optimal k")
                            st.pyplot(fig)
                        
                        k = st.sidebar.slider("Number of Clusters (k)", 2, 10, 3)
                        
                        kmeans = KMeans(n_clusters=k, random_state=42)
                        clusters = kmeans.fit_predict(X_scaled)
                        
                        if X_scaled.shape[1] >= 2:
                            score = silhouette_score(X_scaled, clusters)
                            st.success(f"Clustering Complete! Silhouette Score: {score:.4f}")
                        else:
                            st.success("Clustering Complete!")
                            
                        if len(X.columns) >= 2:
                            st.write("### Cluster Plot")
                            fig, ax = plt.subplots(figsize=(8, 6))
                            if len(X.columns) > 2:
                                pca = PCA(n_components=2)
                                X_plot = pca.fit_transform(X_scaled)
                                ax.set_xlabel("Principal Component 1")
                                ax.set_ylabel("Principal Component 2")
                            else:
                                X_plot = X_scaled
                                ax.set_xlabel(X.columns[0])
                                ax.set_ylabel(X.columns[1])
                                
                            sns.scatterplot(x=X_plot[:, 0], y=X_plot[:, 1], hue=clusters, palette="viridis", ax=ax)
                            st.pyplot(fig)
                            
                    elif task_type == "Dimensionality Reduction (PCA)":
                        max_comp = min(10, len(X.columns))
                        if max_comp < 2:
                            st.error("Need at least 2 features for PCA.")
                        else:
                            n_components = st.sidebar.slider("Number of Components", 2, max_comp, 2)
                            
                            pca = PCA(n_components=n_components)
                            components = pca.fit_transform(X_scaled)
                            
                            st.success(f"PCA Complete! Total Explained Variance: {sum(pca.explained_variance_ratio_):.4f}")
                            
                            st.write("### PCA Scatter Plot (PC1 vs PC2)")
                            fig, ax = plt.subplots(figsize=(8, 6))
                            sns.scatterplot(x=components[:, 0], y=components[:, 1], ax=ax)
                            ax.set_xlabel("Principal Component 1")
                            ax.set_ylabel("Principal Component 2")
                            st.pyplot(fig)

else:
    st.info("Awaiting file upload.")
