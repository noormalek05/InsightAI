import pandas as pd


def run_analysis(input_data=None):
    """
     Load sales data and perform business analysis.
    """

    # --------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------

    if input_data is None:
         data = pd.read_csv("data/sales_data.csv")
    else:
         data = input_data.copy()


    # Calculate revenue
    data["Revenue"] = data["Units_Sold"] * data["Unit_Price"]

    # --------------------------------------------------
    # PRODUCT ANALYSIS
    # --------------------------------------------------

    product_revenue = (
        data.groupby("Product")["Revenue"]
        .sum()
    )

    product_units = (
        data.groupby("Product")["Units_Sold"]
        .sum()
    )

    # --------------------------------------------------
    # REGION ANALYSIS
    # --------------------------------------------------

    region_revenue = (
        data.groupby("Region")["Revenue"]
        .sum()
    )

    region_product_revenue = (
        data.groupby(["Region", "Product"])["Revenue"]
        .sum()
    )

    # --------------------------------------------------
    # MARKETING ANALYSIS
    # --------------------------------------------------

    data["Revenue_After_Marketing"] = (
        data["Revenue"] - data["Marketing_Spend"]
    )

    product_net_revenue = (
        data.groupby("Product")["Revenue_After_Marketing"]
        .sum()
    )

    data["Marketing_ROI"] = (
        data["Revenue"] / data["Marketing_Spend"]
    )

    product_marketing_roi = (
        data.groupby("Product")["Marketing_ROI"]
        .mean()
    )

    # --------------------------------------------------
    # BUSINESS KPIs
    # --------------------------------------------------

    total_revenue = data["Revenue"].sum()

    total_units = data["Units_Sold"].sum()

    average_rating = data["Customer_Rating"].mean()

    total_marketing = data["Marketing_Spend"].sum()

    kpis = {
        "total_revenue": total_revenue,
        "total_units": total_units,
        "average_rating": average_rating,
        "total_marketing_spend": total_marketing
    }

    # --------------------------------------------------
    # RETURN ALL RESULTS
    # --------------------------------------------------

    return {
        "data": data,

        "kpis": kpis,

        "products": {
            "revenue": product_revenue,
            "units": product_units,
            "net_revenue": product_net_revenue
        },

        "regions": {
            "revenue": region_revenue
        },

        "region_products": {
            "revenue": region_product_revenue
        },

        "marketing": {
            "roi": product_marketing_roi
        }
    }