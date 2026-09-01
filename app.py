import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="InsightAI",
    page_icon="🧠",
    layout="wide"
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0E1626;
        color: white;
    }

    h1, h2, h3 {
        color: #F5F5F5;
    }

    .main-title {
        font-size: 52px;
        font-weight: 800;
        color: white;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: #9FB3C8;
        margin-bottom: 40px;
    }

    .section-title {
        font-size: 30px;
        font-weight: 700;
        color: white;
        margin-top: 30px;
        margin-bottom: 20px;
    }

    .highlight-card {
        background-color: #223A59;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #315A8F;
        min-height: 150px;
    }

    .highlight-title {
        color: #75B6F5;
        font-size: 17px;
        font-weight: bold;
    }

    .highlight-value {
        color: white;
        font-size: 25px;
        font-weight: bold;
        margin-top: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def find_column(columns, possible_names):
    """
    Find a matching column from possible names.
    """

    for column in columns:
        column_lower = column.lower().replace(" ", "").replace("_", "")

        for name in possible_names:
            name_lower = name.lower().replace(" ", "").replace("_", "")

            if name_lower in column_lower:
                return column

    return None


def format_currency(value):
    """
    Format a number as Indian Rupees.
    """

    try:
        return f"₹{value:,.0f}"
    except:
        return str(value)


# ==========================================================
# LOAD DEFAULT DATA
# ==========================================================

def load_default_data():

    possible_paths = [
        "data/business_sales.csv",
        "data/sales.csv",
        "data/business_data.csv",
        "business_sales.csv",
        "sales.csv"
    ]

    for path in possible_paths:

        if os.path.exists(path):

            try:
                return pd.read_csv(path)

            except:
                pass

    return None


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("🧠 InsightAI")

    st.write("AI-Powered Business Intelligence")

    st.divider()

    st.subheader("📂 Data Source")

    uploaded_file = st.file_uploader(
        "Upload your CSV",
        type=["csv"],
        key="business_csv"
    )

    st.divider()

    st.info(
        """
        Upload a business or sales dataset in CSV format.

        InsightAI will automatically analyze the available columns.
        """
    )


# ==========================================================
# SELECT DATA
# ==========================================================

default_data = load_default_data()

if uploaded_file is not None:

    try:

        df = pd.read_csv(uploaded_file)

        st.success("✅ Custom dataset loaded successfully!")

        data_source = "Uploaded Dataset"

    except Exception as e:

        st.error("❌ Unable to read the uploaded CSV file.")

        st.stop()

else:

    if default_data is not None:

        df = default_data

        data_source = "Default Dataset"

    else:

        st.warning(
            "⚠️ No default dataset found. Please upload a CSV file from the sidebar."
        )

        st.stop()


# ==========================================================
# CLEAN COLUMN NAMES
# ==========================================================

df.columns = df.columns.astype(str).str.strip()


# ==========================================================
# DETECT IMPORTANT COLUMNS
# ==========================================================

columns = df.columns.tolist()


product_column = find_column(
    columns,
    [
        "product",
        "productname",
        "item",
        "itemname"
    ]
)


region_column = find_column(
    columns,
    [
        "region",
        "location",
        "area",
        "state",
        "city"
    ]
)


units_column = find_column(
    columns,
    [
        "unitssold",
        "quantity",
        "qty",
        "units",
        "salesquantity"
    ]
)


price_column = find_column(
    columns,
    [
        "unitprice",
        "price",
        "sellingprice",
        "cost"
    ]
)


revenue_column = find_column(
    columns,
    [
        "revenue",
        "salesamount",
        "totalrevenue",
        "amount",
        "sales"
    ]
)


marketing_column = find_column(
    columns,
    [
        "marketingspend",
        "marketing",
        "advertising",
        "adspend",
        "promotioncost"
    ]
)


rating_column = find_column(
    columns,
    [
        "customerrating",
        "rating",
        "reviewscore",
        "score"
    ]
)


# ==========================================================
# CONVERT NUMERIC COLUMNS
# ==========================================================

numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()


# Convert detected columns safely

for column in [
    units_column,
    price_column,
    revenue_column,
    marketing_column,
    rating_column
]:

    if column is not None:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ==========================================================
# CALCULATE REVENUE
# ==========================================================

if revenue_column is not None:

    df["Calculated_Revenue"] = df[revenue_column]

elif units_column is not None and price_column is not None:

    df["Calculated_Revenue"] = (
        df[units_column] *
        df[price_column]
    )

else:

    df["Calculated_Revenue"] = 0


# ==========================================================
# CALCULATE KPIs
# ==========================================================

total_revenue = df["Calculated_Revenue"].sum()


if units_column is not None:

    total_units = df[units_column].sum()

else:

    total_units = len(df)


if rating_column is not None:

    average_rating = df[rating_column].mean()

else:

    average_rating = 0


if marketing_column is not None:

    total_marketing = df[marketing_column].sum()

else:

    total_marketing = 0


# ==========================================================
# MAIN HEADER
# ==========================================================

st.markdown(
    """
    <div class="main-title">
        🧠 InsightAI
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="subtitle">
        AI-Powered Business Intelligence Dashboard
    </div>
    """,
    unsafe_allow_html=True
)


st.caption(f"📊 Currently analyzing: **{data_source}**")


# ==========================================================
# DATASET INFORMATION
# ==========================================================

with st.expander("📋 View Dataset Information"):

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", df.shape[0])

    col2.metric("Columns", df.shape[1])

    col3.metric("Data Source", data_source)

    st.write("### Available Columns")

    st.write(", ".join(df.columns.tolist()))

    st.write("### Data Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )


# ==========================================================
# BUSINESS OVERVIEW
# ==========================================================

st.markdown(
    '<div class="section-title">📊 Business Overview</div>',
    unsafe_allow_html=True
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "💰 Total Revenue",
        format_currency(total_revenue)
    )


with col2:

    st.metric(
        "📦 Total Units Sold",
        f"{total_units:,.0f}"
    )


with col3:

    if average_rating > 0:

        rating_display = f"{average_rating:.2f}/5"

    else:

        rating_display = "N/A"

    st.metric(
        "⭐ Customer Rating",
        rating_display
    )


with col4:

    st.metric(
        "📢 Marketing Spend",
        format_currency(total_marketing)
    )


# ==========================================================
# BUSINESS PERFORMANCE HIGHLIGHTS
# ==========================================================

st.markdown(
    '<div class="section-title">🏆 Business Performance Highlights</div>',
    unsafe_allow_html=True
)


highlight_col1, highlight_col2, highlight_col3 = st.columns(3)


# ----------------------------------------------------------
# TOP PRODUCT
# ----------------------------------------------------------

top_product = "N/A"
top_product_revenue = 0


if product_column is not None:

    product_analysis = (
        df.groupby(product_column)["Calculated_Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    if len(product_analysis) > 0:

        top_product = product_analysis.index[0]

        top_product_revenue = product_analysis.iloc[0]


with highlight_col1:

    st.markdown(
        f"""
        <div class="highlight-card">

        <div class="highlight-title">
        🏆 Top Product
        </div>

        <div class="highlight-value">
        {top_product}
        </div>

        <br>

        Revenue: {format_currency(top_product_revenue)}

        </div>
        """,
        unsafe_allow_html=True
    )


# ----------------------------------------------------------
# STRONGEST REGION
# ----------------------------------------------------------

strongest_region = "N/A"
strongest_region_revenue = 0


if region_column is not None:

    region_analysis = (
        df.groupby(region_column)["Calculated_Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    if len(region_analysis) > 0:

        strongest_region = region_analysis.index[0]

        strongest_region_revenue = region_analysis.iloc[0]


with highlight_col2:

    st.markdown(
        f"""
        <div class="highlight-card">

        <div class="highlight-title">
        🌍 Strongest Region
        </div>

        <div class="highlight-value">
        {strongest_region}
        </div>

        <br>

        Revenue: {format_currency(strongest_region_revenue)}

        </div>
        """,
        unsafe_allow_html=True
    )


# ----------------------------------------------------------
# MARKETING ROI
# ----------------------------------------------------------

best_roi_product = "N/A"
best_roi = 0


if (
    product_column is not None
    and marketing_column is not None
):

    roi_data = df.copy()

    roi_group = roi_data.groupby(product_column).agg(
        Revenue=("Calculated_Revenue", "sum"),
        Marketing=(marketing_column, "sum")
    )

    roi_group["ROI"] = (
        roi_group["Revenue"] /
        roi_group["Marketing"].replace(0, 1)
    )

    roi_group = roi_group.sort_values(
        "ROI",
        ascending=False
    )

    if len(roi_group) > 0:

        best_roi_product = roi_group.index[0]

        best_roi = roi_group.iloc[0]["ROI"]


with highlight_col3:

    st.markdown(
        f"""
        <div class="highlight-card">

        <div class="highlight-title">
        📢 Best Marketing ROI
        </div>

        <div class="highlight-value">
        {best_roi_product}
        </div>

        <br>

        ROI: {best_roi:.2f}

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# PRODUCT PERFORMANCE
# ==========================================================

st.markdown(
    '<div class="section-title">💼 Product Performance</div>',
    unsafe_allow_html=True
)


if product_column is not None:

    chart_col1, chart_col2 = st.columns(2)


    # ------------------------------------------------------
    # REVENUE BY PRODUCT
    # ------------------------------------------------------

    product_revenue = (
        df.groupby(product_column)["Calculated_Revenue"]
        .sum()
        .reset_index()
    )


    with chart_col1:

        st.subheader("💰 Revenue by Product")

        fig_revenue = px.bar(
            product_revenue,
            x=product_column,
            y="Calculated_Revenue",
            title="Revenue by Product"
        )

        fig_revenue.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0E1626",
            plot_bgcolor="#0E1626"
        )

        st.plotly_chart(
            fig_revenue,
            use_container_width=True
        )


    # ------------------------------------------------------
    # UNITS SOLD BY PRODUCT
    # ------------------------------------------------------

    if units_column is not None:

        product_units = (
            df.groupby(product_column)[units_column]
            .sum()
            .reset_index()
        )


        with chart_col2:

            st.subheader("📦 Units Sold by Product")

            fig_units = px.bar(
                product_units,
                x=product_column,
                y=units_column,
                title="Units Sold by Product"
            )

            fig_units.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0E1626",
                plot_bgcolor="#0E1626"
            )

            st.plotly_chart(
                fig_units,
                use_container_width=True
            )

else:

    st.info(
        "ℹ️ No product-related column was detected in this dataset."
    )


# ==========================================================
# REGION PERFORMANCE
# ==========================================================

if region_column is not None:

    st.markdown(
        '<div class="section-title">🌍 Regional Performance</div>',
        unsafe_allow_html=True
    )


    region_revenue = (
        df.groupby(region_column)["Calculated_Revenue"]
        .sum()
        .reset_index()
    )


    fig_region = px.pie(
        region_revenue,
        names=region_column,
        values="Calculated_Revenue",
        title="Revenue Distribution by Region"
    )


    fig_region.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0E1626"
    )


    st.plotly_chart(
        fig_region,
        use_container_width=True
    )


# ==========================================================
# MARKETING ANALYSIS
# ==========================================================

if marketing_column is not None:

    st.markdown(
        '<div class="section-title">📢 Marketing Analysis</div>',
        unsafe_allow_html=True
    )


    if product_column is not None:

        marketing_analysis = (
            df.groupby(product_column)[marketing_column]
            .sum()
            .reset_index()
        )


        fig_marketing = px.bar(
            marketing_analysis,
            x=product_column,
            y=marketing_column,
            title="Marketing Spend by Product"
        )


        fig_marketing.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0E1626",
            plot_bgcolor="#0E1626"
        )


        st.plotly_chart(
            fig_marketing,
            use_container_width=True
        )


# ==========================================================
# AI INSIGHTS
# ==========================================================

st.markdown(
    '<div class="section-title">🤖 InsightAI Smart Analysis</div>',
    unsafe_allow_html=True
)


insight_col1, insight_col2 = st.columns(2)


with insight_col1:

    st.subheader("📈 Key Business Insights")

    if top_product != "N/A":

        st.success(
            f"🏆 **{top_product}** is currently the highest-performing product."
        )


    if strongest_region != "N/A":

        st.info(
            f"🌍 **{strongest_region}** is the strongest revenue-generating region."
        )


    if average_rating > 0:

        if average_rating >= 4:

            st.success(
                "⭐ Customer satisfaction is strong based on the available ratings."
            )

        elif average_rating >= 3:

            st.warning(
                "⭐ Customer ratings are moderate and could be improved."
            )

        else:

            st.error(
                "⭐ Customer satisfaction requires attention."
            )


with insight_col2:

    st.subheader("💡 Business Recommendations")

    if marketing_column is not None and total_marketing > 0:

        st.write(
            "📢 Focus marketing investment on products that generate the highest revenue and ROI."
        )


    if strongest_region != "N/A":

        st.write(
            f"🌍 Consider expanding successful strategies from **{strongest_region}** into other regions."
        )


    if top_product != "N/A":

        st.write(
            f"🏆 Maintain inventory and promotional focus for **{top_product}**."
        )


# ==========================================================
# DATA EXPLORER
# ==========================================================

st.markdown(
    '<div class="section-title">🔍 Data Explorer</div>',
    unsafe_allow_html=True
)


st.write(
    "Explore the complete dataset currently being analyzed."
)


st.dataframe(
    df,
    use_container_width=True
)


# ==========================================================
# DOWNLOAD ANALYZED DATA
# ==========================================================

csv = df.to_csv(index=False).encode("utf-8")


st.download_button(
    label="📥 Download Analyzed Dataset",
    data=csv,
    file_name="insightai_analyzed_data.csv",
    mime="text/csv"
)


# ==========================================================
# FOOTER
# ==========================================================

st.divider()


st.markdown(
    """
    <center>

    🧠 <b>InsightAI</b><br>

    AI-Powered Business Intelligence & Sales Analytics Platform

    </center>
    """,
    unsafe_allow_html=True
)
