import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

st.set_page_config(page_title="Automatic EDA", page_icon="📊", layout="wide")

st.title("📊 Automatic Exploratory Data Analysis")
st.write("Upload a CSV or Excel dataset to automatically generate a comprehensive exploratory data analysis (EDA) report.")

with st.sidebar:
    st.header("Settings")
    st.info("The generated report includes correlations, missing values, descriptive statistics, and data distributions.")
    minimal_report = st.toggle("Minimal Report", value=False)
    
uploaded_file = st.file_uploader("Upload your dataset", type=["csv", "xlsx"])

if uploaded_file is not None:
    @st.cache_data
    def load_data(file):
        """Load data from uploaded file."""
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        else:
            return pd.read_excel(file)

    try:
        df = load_data(uploaded_file)
        st.success(f"Successfully loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.")
        
        with st.expander("Preview Data"):
            st.dataframe(df.head(10))
            
        tab1, tab2 = st.tabs(["Quick Summary", "Full Profiling Report"])
        
        with tab1:
            st.subheader("Dataset Shape")
            st.write(f"**Rows:** {df.shape[0]}, **Columns:** {df.shape[1]}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Data Types")
                dtypes_df = pd.DataFrame(df.dtypes, columns=["Type"]).astype(str)
                st.dataframe(dtypes_df, use_container_width=True)
                
            with col2:
                st.subheader("Missing Values")
                missing = df.isnull().sum()
                missing_pct = (df.isnull().sum() / len(df)) * 100
                missing_df = pd.DataFrame({'Count': missing, 'Percentage': missing_pct})
                st.dataframe(missing_df, use_container_width=True)
                
            st.subheader("Descriptive Statistics")
            st.dataframe(df.describe(), use_container_width=True)
            
            col3, col4 = st.columns(2)
            
            with col3:
                st.subheader("Correlation Heatmap")
                numeric_df = df.select_dtypes(include=['number'])
                if not numeric_df.empty:
                    fig, ax = plt.subplots(figsize=(8, 6))
                    sns.heatmap(numeric_df.corr(), annot=False, cmap='coolwarm', ax=ax)
                    st.pyplot(fig)
                else:
                    st.info("No numeric columns available for correlation heatmap.")
                    
            with col4:
                st.subheader("Missing Values Chart")
                if missing.sum() > 0:
                    fig, ax = plt.subplots(figsize=(8, 6))
                    missing[missing > 0].plot(kind='bar', ax=ax)
                    plt.ylabel("Missing Count")
                    plt.xticks(rotation=45, ha='right')
                    st.pyplot(fig)
                else:
                    st.info("No missing values found in the dataset.")
                    
        with tab2:
            st.subheader("Automated Profiling Report")
            selected_columns = st.multiselect(
                "Select columns to include in the profiling report:",
                options=df.columns.tolist(),
                default=df.columns.tolist()
            )
            
            if st.button("Generate Report"):
                if not selected_columns:
                    st.warning("Please select at least one column.")
                else:
                    with st.spinner("Generating profiling report... This may take a while for large datasets."):
                        filtered_df = df[selected_columns]
                        profile = ProfileReport(filtered_df, minimal=minimal_report, explorative=not minimal_report, config_file=None)
                        st_profile_report(profile)
                
    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Awaiting for a CSV or Excel file to be uploaded.")
