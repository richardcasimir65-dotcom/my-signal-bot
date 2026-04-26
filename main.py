from flask import Flask, render_template_string
import random, os
from datetime import datetime, timedelta

app = Flask(__name__)

# This is the "App" design in Somali
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; background: #f0f2f5; display: flex; justify-content: center; margin: 0; padding: 20px; }
        .card { background: white; width: 100%; max-width: 350px; border-radius: 25px; padding: 20px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        .asset { font-size: 22px; font-weight: bold; color: #333; margin: 15px 0; }
        .row { display: flex; justify-content: space-around; margin: 20px 0; text-align: left; }
        .label { color: #999; font-size: 12px; }
        .val { font-weight: bold; font-size: 16px; }
        .dir { font-size: 50px; font-weight: 900; color: {{ color }}; margin: 10px 0; }
        .next-bet { background: #f8f9fa; padding: 12px; border-radius: 12px; margin: 20px 0; font-weight: bold; border: 1px dashed #ccc; }
        .btn { background: #0052ff; color: white; border: none; width: 100%; padding: 18px; border-radius: 15px; font-weight: bold; font-size: 18px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="card">
        <div style="font-size:11px; color:#aaa; margin-bottom:10px;">📶 Signal Robot AI</div>
        <div class="asset">📊 AUD/CHF OTC</div>
        <div class="row">
            <div><span class="label">Waqtiga</span><br><span class="val">⌛ 15s</span></div>
            <div><span class="label">Kalsoonida</span><br><span class="val">93%</span></div>
        </div>
        <div class="dir">{{ direction }}</div>
        <div class="next-bet">NEXT BET: {{ next_bet }}</div>
        <button class="btn" onclick="location.reload()">DALBO SIGNAL</button>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    # Random signal logic
    direction = random.choice(["SELL ↘️", "BUY ↗️"])
    color = "#ff3b30" if "SELL" in direction else "#34c759"
    # Show time in minutes only (HH:MM)
    next_bet = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")
    return render_template_string(HTML_PAGE, direction=direction, color=color, next_bet=next_bet)

if __name__ == '__main__':
    # Render uses the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
