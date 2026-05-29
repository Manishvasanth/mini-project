import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Advanced EDA Dashboard",
    layout="wide"
)

# ---------------- TITLE ----------------
st.markdown(
    """
    <h1 style='text-align:center; color:#00FFFF;'>
    Advanced Interactive EDA Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("Dashboard Settings")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

# ---------------- THEME ----------------
theme = st.sidebar.selectbox(
    "Select Theme",
    [
        "plotly_dark",
        "plotly",
        "ggplot2",
        "seaborn"
    ]
)

# ---------------- LOAD DATA ----------------
if uploaded_file is not None:

    # Read dataset
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("Dataset Uploaded Successfully")

    # ---------------- DATA PREVIEW ----------------
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # ---------------- KPI CARDS ----------------
    st.subheader("Dataset Information")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric(
        "Missing Values",
        int(df.isnull().sum().sum())
    )
    col4.metric(
        "Duplicates",
        int(df.duplicated().sum())
    )

    # ---------------- COLUMN TYPES ----------------
    numeric_cols = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    cat_cols = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    # ---------------- SIDEBAR FILTERS ----------------
    st.sidebar.subheader("Visualization Filters")

    chart_type = st.sidebar.selectbox(
        "Select Chart",
        [
            "Histogram",
            "Scatter Plot",
            "Line Chart",
            "Box Plot",
            "Pie Chart",
            "Correlation Heatmap",
            "Treemap",
            "Seaborn Histogram",
            "Seaborn Boxplot",
            "Seaborn Countplot",
            "Seaborn Heatmap"
        ]
    )

    # ---------------- HISTOGRAM ----------------
    if chart_type == "Histogram":

        st.subheader("Histogram")

        if len(numeric_cols) > 0:

            col = st.selectbox(
                "Select Numeric Column",
                numeric_cols
            )

            fig = px.histogram(
                df,
                x=col,
                nbins=30,
                template=theme,
                color_discrete_sequence=["cyan"]
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.warning("No numeric columns found")

    # ---------------- SCATTER PLOT ----------------
    elif chart_type == "Scatter Plot":

        st.subheader("Scatter Plot")

        if len(numeric_cols) >= 2:

            x_col = st.selectbox(
                "Select X-axis",
                numeric_cols
            )

            y_col = st.selectbox(
                "Select Y-axis",
                numeric_cols,
                index=1
            )

            fig = px.scatter(
                df,
                x=x_col,
                y=y_col,
                color=y_col,
                size=y_col,
                template=theme
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.warning("Need at least 2 numeric columns")

    # ---------------- LINE CHART ----------------
    elif chart_type == "Line Chart":

        st.subheader("Line Chart")

        if len(numeric_cols) > 0:

            x_col = st.selectbox(
                "Select X-axis",
                df.columns
            )

            y_col = st.selectbox(
                "Select Y-axis",
                numeric_cols
            )

            fig = px.line(
                df,
                x=x_col,
                y=y_col,
                template=theme
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.warning("No numeric columns found")

    # ---------------- BOX PLOT ----------------
    elif chart_type == "Box Plot":

        st.subheader("Box Plot")

        if len(numeric_cols) > 0:

            col = st.selectbox(
                "Select Column",
                numeric_cols
            )

            fig = px.box(
                df,
                y=col,
                template=theme
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.warning("No numeric columns found")

    # ---------------- PIE CHART ----------------
    elif chart_type == "Pie Chart":

        st.subheader("Pie Chart")

        if len(cat_cols) > 0:

            col = st.selectbox(
                "Select Categorical Column",
                cat_cols
            )

            pie_data = df[col].value_counts().reset_index()

            pie_data.columns = [col, "Count"]

            fig = px.pie(
                pie_data,
                names=col,
                values="Count",
                template=theme
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.warning("No categorical columns found for Pie Chart")

    # ---------------- HEATMAP ----------------
    elif chart_type == "Correlation Heatmap":

        st.subheader("Correlation Heatmap")

        if len(numeric_cols) > 1:

            corr = df[numeric_cols].corr()

            fig = px.imshow(
                corr,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="RdBu",
                template=theme
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.warning("Need at least 2 numeric columns")

    # ---------------- TREEMAP ----------------
    elif chart_type == "Treemap":

        st.subheader("Treemap")

        if len(cat_cols) > 0 and len(numeric_cols) > 0:

            fig = px.treemap(
                df,
                path=[cat_cols[0]],
                values=numeric_cols[0],
                template=theme
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.warning(
                "Treemap requires categorical and numeric columns"
            )

    # ---------------- SEABORN HISTOGRAM ----------------
    elif chart_type == "Seaborn Histogram":

        st.subheader("Seaborn Histogram")

        if len(numeric_cols) > 0:

            col = st.selectbox(
                "Select Numeric Column",
                numeric_cols
            )

            fig, ax = plt.subplots(figsize=(8, 5))

            sns.histplot(
                df[col],
                kde=True,
                color="cyan",
                ax=ax
            )

            st.pyplot(fig)

        else:
            st.warning("No numeric columns found")

    # ---------------- SEABORN BOXPLOT ----------------
    elif chart_type == "Seaborn Boxplot":

        st.subheader("Seaborn Boxplot")

        if len(numeric_cols) > 0:

            col = st.selectbox(
                "Select Numeric Column",
                numeric_cols
            )

            fig, ax = plt.subplots(figsize=(8, 5))

            sns.boxplot(
                y=df[col],
                color="orange",
                ax=ax
            )

            st.pyplot(fig)

        else:
            st.warning("No numeric columns found")

    # ---------------- SEABORN COUNTPLOT ----------------
    elif chart_type == "Seaborn Countplot":

        st.subheader("Seaborn Countplot")

        if len(cat_cols) > 0:

            col = st.selectbox(
                "Select Categorical Column",
                cat_cols
            )

            fig, ax = plt.subplots(figsize=(10, 5))

            sns.countplot(
                x=df[col],
                palette="viridis",
                ax=ax
            )

            plt.xticks(rotation=45)

            st.pyplot(fig)

        else:
            st.warning("No categorical columns found")

    # ---------------- SEABORN HEATMAP ----------------
    elif chart_type == "Seaborn Heatmap":

        st.subheader("Seaborn Heatmap")

        if len(numeric_cols) > 1:

            corr = df[numeric_cols].corr()

            fig, ax = plt.subplots(figsize=(10, 6))

            sns.heatmap(
                corr,
                annot=True,
                cmap="coolwarm",
                ax=ax
            )

            st.pyplot(fig)

        else:
            st.warning("Need at least 2 numeric columns")

    # ---------------- DATA TYPES ----------------
    st.subheader("Data Types")
    st.write(df.dtypes)

    # ---------------- MISSING VALUES ----------------
    st.subheader("Missing Values")
    st.write(df.isnull().sum())

    # ---------------- STATISTICAL SUMMARY ----------------
    if len(numeric_cols) > 0:

        st.subheader("Statistical Summary")
        st.write(df[numeric_cols].describe())

    # ---------------- DOWNLOAD ----------------
    st.subheader("Download Cleaned Dataset")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="cleaned_dataset.csv",
        mime="text/csv"
    )

else:

    st.info("Please upload a dataset from the sidebar.")
