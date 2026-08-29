import matplotlib.pyplot as plt


def plot_revenue_by_product(product_revenue):
    """Create a bar chart showing revenue by product."""

    product_revenue.plot(kind="bar")

    plt.title("Revenue by Product")
    plt.xlabel("Product")
    plt.ylabel("Revenue (₹)")

    plt.tight_layout()
    plt.show()

def plot_revenue_by_region(region_revenue):
    """Create a bar chart showing revenue by region."""

    region_revenue.plot(kind="bar")

    plt.title("Revenue by Region")
    plt.xlabel("Region")
    plt.ylabel("Revenue (₹)")

    plt.tight_layout()
    plt.show()

def plot_revenue_by_region_product(region_product_revenue):
    """Create a chart showing revenue by region and product."""

    chart_data = region_product_revenue.unstack()

    chart_data.plot(kind="bar")

    plt.title("Revenue by Region and Product")
    plt.xlabel("Region")
    plt.ylabel("Revenue (₹)")

    plt.tight_layout()
    plt.show()

def plot_marketing_roi(roi_by_product):
    """Create a bar chart showing marketing ROI by product."""

    roi_by_product.plot(kind="bar")

    plt.title("Marketing ROI by Product")
    plt.xlabel("Product")
    plt.ylabel("Marketing ROI")

    plt.tight_layout()
    plt.show()
    