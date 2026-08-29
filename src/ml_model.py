import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder


def prepare_ml_data(data):
    """Prepare data for machine learning."""

    features = data[
        [
            "Product",
            "Region",
            "Unit_Price",
            "Marketing_Spend",
            "Customer_Rating"
        ]
    ]

    target = data["Units_Sold"]

    return features, target


def train_sales_model(data):
    """Train a Linear Regression model to predict units sold."""

    features, target = prepare_ml_data(data)

    categorical_features = [
        "Product",
        "Region"
    ]

    numerical_features = [
        "Unit_Price",
        "Marketing_Spend",
        "Customer_Rating"
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features
            )
        ],
        remainder="passthrough"
    )

    X_train, X_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=42
    )

    X_train = preprocessor.fit_transform(X_train)
    X_test = preprocessor.transform(X_test)

    model = LinearRegression()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    return {
        "model": model,
        "preprocessor": preprocessor,
        "mae": mae,
        "r2": r2,
        "predictions": predictions,
        "actual": y_test
    }

def predict_sales(
    model_results,
    product,
    region,
    unit_price,
    marketing_spend,
    customer_rating
):
    """Predict units sold for a new business scenario."""

    new_data = pd.DataFrame({
        "Product": [product],
        "Region": [region],
        "Unit_Price": [unit_price],
        "Marketing_Spend": [marketing_spend],
        "Customer_Rating": [customer_rating]
    })

    processed_data = model_results["preprocessor"].transform(new_data)

    prediction = model_results["model"].predict(processed_data)

    return prediction[0]