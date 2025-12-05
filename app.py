#Hudson

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from src.data_pipeline import get_data
from src.anomaly_detection import find_big_moves
from src.news_data import get_news_for_moves
from src.llm_reasoning import explain_moves
from datetime import date, datetime
import os

app = Flask(__name__, static_folder='static') #go into static folder for files
CORS(app) #create flask application backend

def date_converter(o):
    #convert to strings
    if isinstance(o, (date, datetime)):
        return o.isoformat()
    raise TypeError(f"Object of type {type(o)} is not JSON serializable")



@app.route('/') #keep as /
def index():
    #Main page index.html path
    return send_from_directory('static', 'index.html')

@app.route('/style.css')
def serve_css():
    #same for css
    return send_from_directory('static','style.css')

@app.route('/page.js')
def serve_js():
    #and same for js
    return send_from_directory('static','page.js')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json() #get post json data
        ticker = data.get('ticker', 'AAPL').upper()
        threshold = float(data.get('threshold', 5.0)) #match threshold
        
        print(f"Analyzing {ticker} with threshold {threshold}%") #Just for clairty when running (in terminal)
        
        #stock data here
        df = get_data(ticker, period="2y", interval="1d")
        
        if df is None or df.empty:
            return jsonify({
                "error": f"Could not get data for {ticker}",
                "ticker": ticker
            }), 404 #In case of error thanks chat
        
        #big
        moves = find_big_moves(df, threshold=threshold)
        
        if not moves:
            return jsonify({

                #format ticker, moves, explain, timestamp in this order
                "ticker": ticker,
                "moves": [],

                "explanation": f"No moves greater than {threshold}% found for {ticker} in the past 2 years.",
                "timestamp": datetime.now().isoformat()
            })
        
        print(f"Found {len(moves)} big moves") #confirmation print
        #print("check")
        
        #query news
        news_by_date = get_news_for_moves(ticker, moves, window_days=1, limit=50)
        
        #query llm
        explanation = explain_moves(ticker, moves, news_by_date)
        
        #format response here, following reg format i use usually
        result = {
            "ticker": ticker,
            "moves": [
                {
                    "time": str(m["time"]), 
                    "date": str(m["date"]),
                    "move": m["move"]
                }
                for m in moves
            ],
            "explanation": explanation,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"Analysis complete for {ticker}")
        return jsonify(result) #make sure ots jsonify result, otherwise so many errors and this took me foreve rto find
        
    except Exception as e: #chat exception
        print(f"Error during analysis: {str(e)}")
        #idek anymore whats going on here
        return jsonify({
            "error": str(e),
            "ticker": ticker if 'ticker' in locals() else "unknown"
        }), 500

@app.route('/api/tickers', methods=['GET']) #get method for tickers, stringify below
def get_tickers():
    popular_tickers = [ #Keep as popular options for now, wont expand prob (longer names for clarity and thats the only way i got it to work)
        {"symbol": "AAPL", "name": "Apple Inc."},
        {"symbol": "MSFT", "name": "Microsoft Corp."},
        {"symbol": "GOOGL","name": "Alphabet Inc."},
        {"symbol": "AMZN","name": "Amazon.com Inc."},
        {"symbol": "TSLA", "name": "Tesla Inc."},
        {"symbol": "META", "name": "Meta Platforms Inc."},
        {"symbol": "NVDA", "name": "NVIDIA Corp."},
        {"symbol": "JPM", "name":"JPMorgan Chase"},
        {"symbol": "V", "name": "Visa Inc."},
        {"symbol": "WMT", "name": "Walmart Inc."}
    ]
    return jsonify(popular_tickers) #return ticker

if __name__ == '__main__':
    print("Starting Flask server...") 
    #print(" Server started? ")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)


    #check done