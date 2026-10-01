# Automatic Data Analysis (EDA) Boilerplate

A minimal, ready-to-use boilerplate for building an **Automatic Exploratory Data Analysis (EDA)** tool using Streamlit and `ydata-profiling` (formerly pandas-profiling).

This boilerplate allows you to upload any CSV or Excel dataset and instantly generate a full, interactive profiling report that details data distributions, correlations, missing values, and descriptive statistics.

---

## Features

- **File Upload**: Supports `.csv` and `.xlsx` files.
- **Data Preview**: Quickly view the head of your dataset.
- **Quick Summary**: Instantly view dataset shape, data types, missing values, descriptive statistics, correlation heatmap, and missing values bar chart.
- **Automated Profiling**: Uses `ydata-profiling` to generate a comprehensive, interactive HTML report directly embedded in the Streamlit app.
- **Column Selection**: Filter the dataset to profile only selected columns.
- **Minimal vs Explorative**: Toggle between minimal and explorative profiling reports for faster generation on large datasets.
- **Caching**: Uses Streamlit's `@st.cache_data` to ensure fast data reloading.

---

## Prerequisites

- Python 3.8+

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-name>/data_analysis
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

1. **Upload a dataset**: Drop your CSV or Excel file into the uploader.
2. **Preview Data**: Expand the preview section to view the first few rows.
3. **Quick Summary**: View the "Quick Summary" tab for an instant overview of your data.
4. **Generate Report**: Navigate to the "Full Profiling Report" tab, select columns to include, choose minimal or explorative generation, and click the "Generate Report" button to create your automated EDA profile. (Note: large datasets may take a few minutes to process).
