from llm_engine import ask_llm
import pandas as pd
from visualization import (
    plot_revenue_by_product,
    plot_revenue_by_region,
    plot_revenue_by_region_product,
    plot_marketing_roi
)

from ml_model import train_sales_model, predict_sales
from insights import generate_business_insights

def load_data():
    """Load the sales dataset."""
    data = pd.read_csv("data/sales_data.csv")

    # Calculate revenue for each transaction
    data["Revenue"] = data["Units_Sold"] * data["Unit_Price"]

    return data


def calculate_kpis(data):
    """Calculate important business KPIs."""

    total_revenue = data["Revenue"].sum()
    total_units = data["Units_Sold"].sum()
    average_rating = data["Customer_Rating"].mean()
    total_marketing = data["Marketing_Spend"].sum()

    return {
        "total_revenue": total_revenue,
        "total_units": total_units,
        "average_rating": average_rating,
        "total_marketing": total_marketing
    }


def analyze_products(data):
    """Analyze revenue and units sold by product."""

    revenue_by_product = data.groupby("Product")["Revenue"].sum()

    units_by_product = data.groupby("Product")["Units_Sold"].sum()

    return {
        "revenue": revenue_by_product,
        "units": units_by_product
    }

def analyze_regions(data):
    """Analyze revenue by region."""

    revenue_by_region = data.groupby("Region")["Revenue"].sum()

    return {
        "revenue": revenue_by_region
    }

def analyze_region_products(data):
    """Analyze revenue by region and product."""

    revenue_by_region_product = (
        data.groupby(["Region", "Product"])["Revenue"].sum()
    )

    return revenue_by_region_product

def analyze_marketing(data):
    """Analyze marketing performance."""

    # Calculate revenue remaining after marketing spend
    data["Revenue_After_Marketing"] = (
        data["Revenue"] - data["Marketing_Spend"]
    )

    # Calculate revenue generated per rupee of marketing spend
    data["Marketing_ROI"] = (
        data["Revenue"] / data["Marketing_Spend"]
    )

    # Calculate average marketing ROI by product
    roi_by_product = data.groupby("Product")["Marketing_ROI"].mean()

    # Calculate revenue after marketing by product
    revenue_after_marketing = (
        data.groupby("Product")["Revenue_After_Marketing"].sum()
    )

    return {
        "roi": roi_by_product,
        "revenue_after_marketing": revenue_after_marketing
    }

def run_analysis():
    """Run all business analysis functions."""

    data = load_data()

    kpis = calculate_kpis(data)

    product_analysis = analyze_products(data)

    region_analysis = analyze_regions(data)

    region_product_analysis = analyze_region_products(data)
    
    marketing_analysis = analyze_marketing(data)

    return {
    "data": data,
    "kpis": kpis,
    "products": product_analysis,
    "regions": region_analysis,
    "region_products": region_product_analysis,
    "marketing": marketing_analysis
}


analysis_results = run_analysis()

ml_results = train_sales_model(
    analysis_results["data"]
)

print("\n--- MACHINE LEARNING RESULTS ---")
print(f"Mean Absolute Error: {ml_results['mae']:.2f}")
print(f"R² Score: {ml_results['r2']:.2f}")

business_insights = generate_business_insights(
    analysis_results
)

print("\n--- BUSINESS INSIGHTS ---")

for insight in business_insights:
    print(f"- {insight}")
    
def generate_sales_prediction(
    ml_results,
    product,
    region,
    unit_price,
    marketing_spend,
    customer_rating
):
    """Generate a sales prediction for a business scenario."""

    prediction = predict_sales(
        ml_results,
        product=product,
        region=region,
        unit_price=unit_price,
        marketing_spend=marketing_spend,
        customer_rating=customer_rating
    )

    return prediction

predicted_units = generate_sales_prediction(
    ml_results,
    product="Phone",
    region="South",
    unit_price=35000,
    marketing_spend=10000,
    customer_rating=4.5
)

print("\n--- SALES PREDICTION ---")
print(f"Predicted Units Sold: {predicted_units:.2f}")

plot_revenue_by_product(
    analysis_results["products"]["revenue"]
)

plot_revenue_by_region(
    analysis_results["regions"]["revenue"]
)
plot_revenue_by_region_product(
    analysis_results["region_products"]
)

plot_marketing_roi(
    analysis_results["marketing"]["roi"]
)
print("\n--- BUSINESS KPIs ---")

kpis = analysis_results["kpis"]

print(f"Total Revenue: ₹{kpis['total_revenue']:,.0f}")
print(f"Total Units Sold: {kpis['total_units']}")
print(f"Average Customer Rating: {kpis['average_rating']:.2f}/5")
print(f"Total Marketing Spend: ₹{kpis['total_marketing']:,.0f}")


print("\n--- REVENUE BY PRODUCT ---")
print(analysis_results["products"]["revenue"])


print("\n--- UNITS SOLD BY PRODUCT ---")
print(analysis_results["products"]["units"])


print("\n--- REVENUE BY REGION ---")
print(analysis_results["regions"]["revenue"])


print("\n--- REVENUE AFTER MARKETING BY PRODUCT ---")
print(analysis_results["marketing"]["revenue_after_marketing"])


print("\n--- AVERAGE MARKETING ROI BY PRODUCT ---")
print(analysis_results["marketing"]["roi"])

business_context = f"""
Total Revenue: ₹16,510,000
Total Units Sold: 503
Average Customer Rating: 4.26/5
Total Marketing Spend: ₹348,500

Revenue by Product:
{analysis_results["products"]["revenue"]}

Revenue by Region:
{analysis_results["regions"]["revenue"]}

Marketing ROI by Product:
{analysis_results["marketing"]["roi"]}

Business Insights:
{business_insights}

ML Model MAE:
{ml_results["mae"]:.2f}

ML Model R²:
{ml_results["r2"]:.2f}
"""

print("\n--- INSIGHTAI BUSINESS CHAT ---")

while True:
    question = input("\nAsk InsightAI (type 'exit' to quit): ")

    if question.lower() == "exit":
        print("Exiting InsightAI...")
        break

    answer = ask_llm(
        question,
        business_context
    )

    print("\n--- AI BUSINESS ANSWER ---")
    print(answer)