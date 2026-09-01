# 🧠 InsightAI

AI-Powered Business Intelligence & Sales Analytics Platform

## 🚀 Live Application

👉 **https://insightai-noormalek.streamlit.app**

InsightAI is a business intelligence application that combines **Data Analysis, Machine Learning, and Local Generative AI** to help users understand business performance and make data-driven decisions.

It provides business KPIs, product and regional analysis, marketing ROI, sales predictions, scenario simulation, and an AI business assistant.

---

## 🚀 Features

### 📊 Business Dashboard

- Total Revenue
- Total Units Sold
- Average Customer Rating
- Total Marketing Spend
- Revenue by Product
- Units Sold by Product
- Revenue by Region
- Marketing ROI
- Top-performing Product
- Strongest Region
- Best Marketing ROI
- Business Insights

### 🔮 Sales Prediction

Users can enter a business scenario and predict expected sales using the Machine Learning model.

Input parameters include:

- Product
- Region
- Unit Price
- Marketing Spend
- Customer Rating

The system provides:

- Predicted Units Sold
- Expected Revenue
- Revenue After Marketing
- Scenario Outlook

### 🤖 AI Business Assistant

InsightAI includes a local AI business assistant powered by **Ollama and Llama 3.2 3B**.

Users can ask questions such as:

- Which product is performing best?
- Which region generated the highest revenue?
- Which product has the highest marketing ROI?
- Should I increase marketing for a particular product?

The AI answers using the available business data.

### 📂 Custom CSV Upload

Users can upload their own business dataset in CSV format.

The application validates the required columns before analyzing the dataset.

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Streamlit
- Ollama
- Llama 3.2 3B

---

## 📁 Project Structure

```text
InsightAI/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── data/
│   └── sales_data.csv
│
└── src/
    ├── data_analysis.py
    ├── ml_model.py
    ├── insights.py
    └── llm_engine.py
