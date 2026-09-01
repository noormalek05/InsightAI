import streamlit as st
import sys
import os
import pandas as pd


# ==================================================
# FIND SRC FOLDER
# ==================================================

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "src"
    )
)


# ==================================================
# IMPORT PROJECT MODULES
# ==================================================

from data_analysis import run_analysis
from ml_model import train_sales_model, predict_sales
from insights import generate_business_insights
from llm_engine import ask_llm


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="InsightAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# CUSTOM DESIGN
# ==================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0b1120;
        color: #e5e7eb;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }

    .main-title {
        font-size: 46px;
        font-weight: 800;
        color: #f9fafb;
        margin-bottom: 0px;
    }

    .main-subtitle {
        font-size: 17px;
        color: #94a3b8;
        margin-top: 4px;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 700;
        color: #f9fafb;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .kpi-card {
        background: linear-gradient(
            135deg,
            #111827,
            #172554
        );

        border: 1px solid #1e3a8a;
        border-radius: 16px;
        padding: 20px;
        min-height: 125px;

        box-shadow:
            0 8px 20px rgba(0, 0, 0, 0.25);
    }

    .kpi-title {
        color: #94a3b8;
        font-size: 14px;
        font-weight: 600;
    }

    .kpi-value {
        color: #f9fafb;
        font-size: 28px;
        font-weight: 800;
        margin-top: 8px;
    }

    .ai-card {
        background:
            linear-gradient(
                135deg,
                #111827,
                #172554
            );

        border: 1px solid #2563eb;
        border-radius: 18px;
        padding: 25px;
        margin-top: 15px;

        box-shadow:
            0 10px 30px rgba(37, 99, 235, 0.15);
    }

    .ai-title {
        font-size: 24px;
        font-weight: 750;
        color: #f9fafb;
    }

    .ai-subtitle {
        color: #94a3b8;
        font-size: 14px;
        margin-top: 5px;
    }

    .prediction-card {
        background:
            linear-gradient(
                135deg,
                #111827,
                #1e1b4b
            );

        border: 1px solid #4f46e5;
        border-radius: 18px;
        padding: 28px;
        text-align: center;
        margin-top: 20px;
    }

    .prediction-label {
        color: #a5b4fc;
        font-size: 14px;
        font-weight: 600;
    }

    .prediction-value {
        color: #f9fafb;
        font-size: 42px;
        font-weight: 800;
        margin-top: 8px;
    }

    .stButton > button {
        border-radius: 10px;
        border: 1px solid #2563eb;
        background-color: #2563eb;
        color: white;
        font-weight: 650;
        padding: 10px 20px;
    }

    .stButton > button:hover {
        background-color: #1d4ed8;
        border-color: #1d4ed8;
    }

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #1f2937;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:28px;
            font-weight:800;
            color:#f9fafb;
            margin-bottom:4px;
        ">
        🧠 InsightAI
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "AI-Powered Business Intelligence"
    )

    st.divider()

    # --------------------------------------------------
    # CSV UPLOAD
    # --------------------------------------------------

    st.subheader("📂 Data Source")

    uploaded_file = st.file_uploader(
        "Upload your CSV",
        type=["csv"],
        key="business_csv"
    )

    if uploaded_file is not None:

        st.success(
            "Custom dataset loaded"
        )

        try:

            preview_data = pd.read_csv(
                uploaded_file
            )

            required_columns = [
                "Date",
                "Product",
                "Region",
                "Units_Sold",
                "Unit_Price",
                "Marketing_Spend",
                "Customer_Rating"
            ]

            missing_columns = [
                column
                for column in required_columns
                if column not in preview_data.columns
            ]

            if missing_columns:

                st.error(
                    "❌ Invalid CSV"
                )

                st.write(
                    "Missing columns:"
                )

                for column in missing_columns:

                    st.write(
                        f"- {column}"
                    )

            else:

                st.success(
                    "✅ Dataset validated successfully"
                )

        except Exception:

            st.error(
                "❌ Could not read this CSV file."
            )

    else:

        st.caption(
            "Using default sales dataset"
        )

    st.divider()

    # --------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------

    page = st.radio(
        "NAVIGATION",
        [
            "📊 Dashboard",
            "🔮 Sales Prediction",
            "🤖 Ask InsightAI"
        ]
    )

    st.divider()

    st.markdown(
        """
        **Technology**

        🐍 Python  
        🐼 Pandas  
        📈 Scikit-learn  
        🎨 Streamlit  
        🧠 Llama 3.2 3B
        """
    )

    st.divider()

    st.caption(
        "InsightAI • Local AI Business Analyst"
    )


# ==================================================
# LOAD BUSINESS DATA
# ==================================================

@st.cache_data
def load_business_data(file_bytes=None):

    if file_bytes is None:

        return run_analysis()

    else:

        uploaded_data = pd.read_csv(
            pd.io.common.BytesIO(file_bytes)
        )

        return run_analysis(
            uploaded_data
        )


# ==================================================
# SELECT DATA SOURCE
# ==================================================

if uploaded_file is not None:

    try:

        analysis_results = load_business_data(
            uploaded_file.getvalue()
        )

    except Exception:

        st.warning(
            "⚠️ Unable to analyze the uploaded file. "
            "Using the default sales dataset instead."
        )

        analysis_results = load_business_data()

else:

    analysis_results = load_business_data()


# ==================================================
# MACHINE LEARNING MODEL
# ==================================================

@st.cache_resource
def load_ml_model(data):

    return train_sales_model(data)


ml_results = load_ml_model(
    analysis_results["data"]
)


# ==================================================
# BUSINESS INSIGHTS
# ==================================================

business_insights = generate_business_insights(
    analysis_results
)


# ==================================================
# DASHBOARD
# ==================================================

if page == "📊 Dashboard":

    st.markdown(
        '<div class="main-title">🧠 InsightAI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'AI-Powered Business Intelligence Dashboard'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # BUSINESS OVERVIEW
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '📊 Business Overview'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    st.subheader("📊 Business Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Total Revenue",
        value=f"₹{analysis_results['kpis']['total_revenue']:,.0f}"
    )

with col2:
    st.metric(
        label="📦 Total Units Sold",
        value=f"{analysis_results['kpis']['total_units']:,}"
    )

with col3:
    st.metric(
        label="⭐ Customer Rating",
        value=f"{analysis_results['kpis']['average_rating']:.2f}/5"
    )

with col4:
    st.metric(
        label="📢 Marketing Spend",
        value=f"₹{analysis_results['kpis']['total_marketing_spend']:,.0f}"
    )
    st.write("")

    # --------------------------------------------------
    # TOP BUSINESS PERFORMERS
    # --------------------------------------------------

    product_revenue = (
        analysis_results["products"]["revenue"]
    )

    region_revenue = (
        analysis_results["regions"]["revenue"]
    )

    marketing_roi = (
        analysis_results["marketing"]["roi"]
    )

    top_product = (
        product_revenue.idxmax()
    )

    top_product_revenue = (
        product_revenue.max()
    )

    top_region = (
        region_revenue.idxmax()
    )

    top_region_revenue = (
        region_revenue.max()
    )

    top_roi_product = (
        marketing_roi.idxmax()
    )

    top_roi_value = (
        marketing_roi.max()
    )

    st.markdown(
        '<div class="section-title">'
        '🏆 Business Performance Highlights'
        '</div>',
        unsafe_allow_html=True
    )

    highlight1, highlight2, highlight3 = st.columns(3)

    with highlight1:

        st.info(
            f"""
            🏆 **Top Product**

            **{top_product}**

            Revenue: **₹{top_product_revenue:,.0f}**
            """
        )

    with highlight2:

        st.info(
            f"""
            🌍 **Strongest Region**

            **{top_region}**

            Revenue: **₹{top_region_revenue:,.0f}**
            """
        )

    with highlight3:

        st.info(
            f"""
            📢 **Best Marketing ROI**

            **{top_roi_product}**

            ROI: **{top_roi_value:.2f}**
            """
        )

    # --------------------------------------------------
    # PRODUCT PERFORMANCE
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🛍️ Product Performance'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "💰 Revenue by Product"
        )

        st.bar_chart(
            product_revenue
        )

    with col2:

        st.subheader(
            "📦 Units Sold by Product"
        )

        st.bar_chart(
            analysis_results["products"]["units"]
        )

    # --------------------------------------------------
    # REGIONAL PERFORMANCE
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🌍 Regional Performance'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Revenue by Region"
        )

        st.bar_chart(
            region_revenue
        )

    with col2:

        st.subheader(
            "Marketing ROI by Product"
        )

        st.bar_chart(
            marketing_roi
        )

    # --------------------------------------------------
    # MACHINE LEARNING PERFORMANCE
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🤖 Machine Learning Performance'
        '</div>',
        unsafe_allow_html=True
    )

    ml_col1, ml_col2 = st.columns(2)

    with ml_col1:

        st.metric(
            "Mean Absolute Error",
            f"{ml_results['mae']:.2f}"
        )

    with ml_col2:

        st.metric(
            "R² Score",
            f"{ml_results['r2']:.2f}"
        )

    # --------------------------------------------------
    # BUSINESS INSIGHTS
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '💡 AI Business Insights'
        '</div>',
        unsafe_allow_html=True
    )

    for insight in business_insights:

        st.info(
            insight
        )


# ==================================================
# SALES PREDICTION
# ==================================================

elif page == "🔮 Sales Prediction":

    st.markdown(
        '<div class="main-title">'
        '🔮 Sales Scenario Simulator'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Enter a business scenario and let the ML model estimate expected sales.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">'
        'Scenario Inputs'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # DYNAMIC PRODUCT AND REGION
    # --------------------------------------------------

    product_options = sorted(
        analysis_results["data"]["Product"]
        .dropna()
        .unique()
        .tolist()
    )

    region_options = sorted(
        analysis_results["data"]["Region"]
        .dropna()
        .unique()
        .tolist()
    )

    # --------------------------------------------------
    # INPUTS
    # --------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        product = st.selectbox(
            "Product",
            product_options
        )

        region = st.selectbox(
            "Region",
            region_options
        )

        average_price = int(
            analysis_results["data"]["Unit_Price"].mean()
        )

        unit_price = st.number_input(
            "Unit Price (₹)",
            min_value=1,
            value=max(average_price, 1),
            step=1000
        )

    with col2:

        average_marketing = int(
            analysis_results["data"]["Marketing_Spend"].mean()
        )

        marketing_spend = st.number_input(
            "Marketing Spend (₹)",
            min_value=0,
            value=max(average_marketing, 0),
            step=1000
        )

        customer_rating = st.slider(
            "Expected Customer Rating",
            min_value=1.0,
            max_value=5.0,
            value=4.5,
            step=0.1
        )

    st.write("")

    # --------------------------------------------------
    # PREDICT SALES
    # --------------------------------------------------

    if st.button(
        "🔮 Predict Expected Sales",
        use_container_width=True
    ):

        prediction = predict_sales(
            ml_results,
            product,
            region,
            unit_price,
            marketing_spend,
            customer_rating
        )

        # --------------------------------------------------
        # SCENARIO CALCULATIONS
        # --------------------------------------------------

        predicted_revenue = (
            prediction * unit_price
        )

        estimated_net_revenue = (
            predicted_revenue
            - marketing_spend
        )

        # --------------------------------------------------
        # MAIN PREDICTION
        # --------------------------------------------------

        st.markdown(
            f"""
            <div class="prediction-card">

                <div class="prediction-label">
                    EXPECTED UNITS SOLD
                </div>

                <div class="prediction-value">
                    {prediction:.2f}
                </div>

                <div style="
                    color:#94a3b8;
                    margin-top:8px;
                ">
                    Based on your selected business scenario
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        # --------------------------------------------------
        # SCENARIO RESULTS
        # --------------------------------------------------

        st.subheader(
            "📊 Scenario Results"
        )

        result1, result2, result3 = st.columns(3)

        with result1:

            st.metric(
                "Expected Revenue",
                f"₹{predicted_revenue:,.0f}"
            )

        with result2:

            st.metric(
                "Marketing Spend",
                f"₹{marketing_spend:,.0f}"
            )

        with result3:

            st.metric(
                "Revenue After Marketing",
                f"₹{estimated_net_revenue:,.0f}"
            )

        st.write("")

        # --------------------------------------------------
        # BUSINESS INTERPRETATION
        # --------------------------------------------------

        st.subheader(
            "💡 Scenario Outlook"
        )

        if estimated_net_revenue > 0:

            st.success(
                f"""
                This scenario is expected to sell approximately
                **{prediction:.2f} units**, generating around
                **₹{predicted_revenue:,.0f} in revenue**.

                After the planned marketing spend of
                **₹{marketing_spend:,.0f}**, the estimated revenue
                remaining is **₹{estimated_net_revenue:,.0f}**.
                """
            )

        else:

            st.warning(
                f"""
                The predicted revenue of **₹{predicted_revenue:,.0f}**
                does not cover the planned marketing spend of
                **₹{marketing_spend:,.0f}**.

                Consider reviewing the pricing, marketing budget,
                or selected product/region combination.
                """
            )

        # --------------------------------------------------
        # SCENARIO SUMMARY
        # --------------------------------------------------

        st.write("")

        st.subheader(
            "📋 Scenario Summary"
        )

        scenario = pd.DataFrame(
            {
                "Parameter": [
                    "Product",
                    "Region",
                    "Unit Price",
                    "Marketing Spend",
                    "Customer Rating"
                ],

                "Selected Value": [
                    product,
                    region,
                    f"₹{unit_price:,.0f}",
                    f"₹{marketing_spend:,.0f}",
                    f"{customer_rating:.1f}/5"
                ]
            }
        )

        st.dataframe(
            scenario,
            use_container_width=True,
            hide_index=True
        )


# ==================================================
# ASK INSIGHTAI
# ==================================================

elif page == "🤖 Ask InsightAI":

    st.markdown(
        '<div class="main-title">'
        '🤖 Ask InsightAI'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Ask questions about your business data and receive AI-generated analysis.'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # AI HEADER
    # --------------------------------------------------

    st.markdown(
        """
        <div class="ai-card">

            <div class="ai-title">
                🧠 AI Business Copilot
            </div>

            <div class="ai-subtitle">
                Powered by your business data and local Llama 3.2 3B
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # --------------------------------------------------
    # EXAMPLE QUESTIONS
    # --------------------------------------------------

    st.caption(
        "Try asking:"
    )

    example_questions = [
        "Which product is performing best and why?",
        "Which region generated the highest revenue?",
        "Which product has the highest marketing ROI?",
        "Should I increase marketing for Phone?"
    ]

    selected_question = st.selectbox(
        "Example questions",
        [
            "Choose a question..."
        ] + example_questions
    )

    # --------------------------------------------------
    # USER QUESTION
    # --------------------------------------------------

    question = st.text_area(
        "Your business question",
        value=(
            ""
            if selected_question == "Choose a question..."
            else selected_question
        ),
        height=100,
        placeholder="Example: Which product should I focus on?"
    )

    # --------------------------------------------------
    # ASK AI
    # --------------------------------------------------

    if st.button(
        "✨ Analyze with InsightAI",
        use_container_width=True
    ):

        if question.strip() == "":

            st.warning(
                "Please enter a business question."
            )

        else:

            # --------------------------------------------------
            # BUSINESS CONTEXT
            # --------------------------------------------------

            business_context = f"""

            BUSINESS KPIs

            Total Revenue:
            ₹{analysis_results['kpis']['total_revenue']:,.0f}

            Total Units Sold:
            {analysis_results['kpis']['total_units']}

            Average Customer Rating:
            {analysis_results['kpis']['average_rating']:.2f}/5

            Total Marketing Spend:
            ₹{analysis_results['kpis']['total_marketing_spend']:,.0f}


            REVENUE BY PRODUCT

            {analysis_results['products']['revenue']}


            UNITS SOLD BY PRODUCT

            {analysis_results['products']['units']}


            REVENUE BY REGION

            {analysis_results['regions']['revenue']}


            MARKETING ROI

            {analysis_results['marketing']['roi']}


            BUSINESS INSIGHTS

            {business_insights}


            MACHINE LEARNING

            MAE:
            {ml_results['mae']:.2f}

            R²:
            {ml_results['r2']:.2f}

            """

            # --------------------------------------------------
            # AI PROCESSING
            # --------------------------------------------------

            with st.spinner(
                "🧠 InsightAI is analyzing your business data..."
            ):

                answer = ask_llm(
                    question,
                    business_context
                )

            # --------------------------------------------------
            # AI ANSWER
            # --------------------------------------------------

            st.markdown(
                """
                <div class="ai-card">

                    <div class="ai-title">
                        💡 InsightAI Analysis
                    </div>

                    <div class="ai-subtitle">
                        AI-generated analysis based on your business data
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")

            st.markdown(
                answer
            )


# ==================================================
# FOOTER
# ==================================================

st.markdown(
    """
    <div class="footer">

        InsightAI • AI-Powered Business Intelligence

        <br>

        Python • Pandas • Scikit-learn • Streamlit • Llama 3.2 3B

    </div>
    """,
    unsafe_allow_html=True
)
