from flask import Flask, request, render_template
import pandas as pd
import matplotlib.pyplot as plt
import json
import requests

app = Flask(__name__)

# Sample keyword mapping for categorization
category_mapping = {
    "groceries": "Groceries",
    "supermarket": "Groceries",
    "restaurant": "Dining",
    "cafe": "Dining",
    "utilities": "Utilities",
    "rent": "Housing"
}

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def handle_file_upload():
    file = request.files['file']
    if file and file.filename.endswith('.csv'):
        df = pd.read_csv(file)
        df = categorize_expenses(df)
        visualize_expenses(df)
        insights = get_ai_insights(df)
        return render_template('results.html', tables=[df.to_html(classes='data')], insights=insights)
    return "Invalid file format. Please upload a CSV file."

def categorize_expense(description):
    for keyword, category in category_mapping.items():
        if keyword in description.lower():
            return category
    return "Other"  # Default category

def categorize_expenses(df):
    df['Category'] = df['Description'].apply(categorize_expense)
    return df

def visualize_expenses(df):
    category_summary = df.groupby('Category')['Amount'].sum()
    category_summary.plot(kind='bar')
    plt.title('Expenses by Category')
    plt.xlabel('Category')
    plt.ylabel('Total Amount')
    plt.savefig('static/expense_chart.png')  # Save the chart as an image

def get_ai_insights(df):
    # Example API call to an AI service (mocked for this example)
    expense_summary = df.groupby('Category')['Amount'].sum().to_dict()
    # Mock response for demonstration
    return "Your dining expenses have increased significantly this month."

if __name__ == '__main__':
    app.run(debug=True)