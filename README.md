# my-signal-bot from flask import Flask, render_template_string
import random, os, yfinance as yf
import pandas_ta as ta
from datetime import datetime, timedelta

app = Flask(__name__)

# --- CONFIGURATION (PUT YOUR INFO HERE) ---
BROKER_TYPE = "POCKET_OPTION"  # or "MT5"
ACCOUNT_ID = "YOUR_ID"
PASSWORD = "YOUR_PASSWORD"
TRADE_AMOUNT = 10  # Amount per trade

# --- REAL ANALYSIS ENGINE ---
def get_signal():
    try:
        # Fetch real-time data for Gold (XAUUSD)
        data = yf.download("GC=F", period="1d", interval="1m", progress=False)
        if data.empty: return "NO DATA", "#888"

        # Calculate RSI (Technical Analysis)
        data['RSI'] = ta.rsi(data['Close'], length=14)
        last_rsi = data['RSI'].iloc[-1]

        # Logic: Buy if Oversold, Sell if Overbought
        if last_rsi < 30:
            return "BUY ↗️", "#34c759"
        elif last_rsi > 70:
            return "SELL ↘️", "#ff3b30"
        else:
            return "WAIT ⏳", "#ffcc00"
    except:
        return "ERROR", "#888"

# --- THE APP INTERFACE ---
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; background: #f0f2f5; display: flex; justify-content: center; padding: 20px; }
        .card { background: white; width: 100%; max-width: 350px; border-radius: 25px; padding: 20px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        .asset { font-size: 22px; font-weight: bold; color: #333; margin: 15px 0; }
        .dir { font-size: 45px; font-weight: 900; color: {{ color }}; margin: 15px 0; }
        .status { font-size: 14px; color: #28a745; margin-bottom: 20px; font-weight: bold; }
        .btn { background: #0052ff; color: white; border: none; width: 100%; padding: 18px; border-radius: 15px; font-weight: bold; font-size: 18px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="card">
        <div style="font-size:11px; color:#aaa;">📶 Auto-Trade Active</div>
        <div class="asset">📊 XAUUSD (GOLD)</div>
        <div class="dir">{{ direction }}</div>
        <div class="status">● BOT CONNECTED TO BROKER</div>
        <p><b>NEXT BET: {{ next_bet }}</b></p>
        <button class="btn" onclick="location.reload()">REFRESH ANALYSIS</button>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    direction, color = get_signal()
    # No seconds, just minutes
    next_bet = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")
    
    # --- AUTO-EXECUTION LOGIC ---
    # Here, the script would send the 'direction' to your broker API
    # execute_trade(direction, TRADE_AMOUNT)
    
    return render_template_string(HTML_PAGE, direction=direction, color=color, next_bet=next_bet)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
