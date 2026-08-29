def generate_business_insights(analysis_results):
    """Generate important business insights from analysis results."""

    insights = []

    product_revenue = analysis_results["products"]["revenue"]
    region_revenue = analysis_results["regions"]["revenue"]
    marketing_roi = analysis_results["marketing"]["roi"]

    # Best product by revenue
    best_product = product_revenue.idxmax()
    best_product_revenue = product_revenue.max()

    insights.append(
        f"{best_product} is the top-performing product by revenue, "
        f"generating ₹{best_product_revenue:,.0f}."
    )

    # Best region by revenue
    best_region = region_revenue.idxmax()
    best_region_revenue = region_revenue.max()

    insights.append(
        f"{best_region} is the strongest region by revenue, "
        f"generating ₹{best_region_revenue:,.0f}."
    )

    # Best marketing ROI
    best_roi_product = marketing_roi.idxmax()
    best_roi = marketing_roi.max()

    insights.append(
        f"{best_roi_product} has the highest marketing ROI "
        f"at {best_roi:.2f}."
    )

    # Recommendation
    insights.append(
        f"Recommendation: Consider increasing marketing focus on "
        f"{best_roi_product}, as it currently provides the strongest "
        f"marketing return."
    )

    return insights