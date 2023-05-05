from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# API endpoint to get all companies' stock data for a particular day
@app.route('/stock-data', methods=['GET'])
def get_stock_data_by_date():
    date = request.args.get('date')
    conn = sqlite3.connect('financial_data.db')
    cursor = conn.cursor()
    query = f"SELECT company, date, price FROM stocks WHERE date = '{date}'"
    cursor.execute(query)
    results = cursor.fetchall()
    stock_data = [{'company': row[0], 'date': row[1], 'price': row[2]} for row in results]
    conn.close()
    return jsonify(stock_data)


# API endpoint to get all stock data for a particular company for a particular day
@app.route('/stock-data/<company>/<date>', methods=['GET'])
def get_stock_data_by_company_and_date(company, date):
    conn = sqlite3.connect('financial_data.db')
    cursor = conn.cursor()
    query = f"SELECT company, date, price FROM stocks WHERE company = '{company}' AND date = '{date}'"
    cursor.execute(query)
    results = cursor.fetchall()
    stock_data = [{'company': row[0], 'date': row[1], 'price': row[2]} for row in results]
    conn.close()
    return jsonify(stock_data)


# API endpoint to get all stock data for a particular company
@app.route('/stock-data/<company>', methods=['GET'])
def get_stock_data_by_company(company):
    conn = sqlite3.connect('financial_data.db')
    cursor = conn.cursor()
    query = f"SELECT company, date, price FROM stocks WHERE company = '{company}'"
    cursor.execute(query)
    results = cursor.fetchall()
    stock_data = [{'company': row[0], 'date': row[1], 'price': row[2]} for row in results]
    conn.close()
    return jsonify(stock_data)


# API endpoint to update stock data for a company by date
@app.route('/stock-data/<company>/<date>', methods=['POST', 'PATCH'])
def update_stock_data(company, date):
    new_price = request.json['price']
    conn = sqlite3.connect('financial_data.db')
    cursor = conn.cursor()
    query = f"UPDATE stocks SET price = {new_price} WHERE company = '{company}' AND date = '{date}'"
