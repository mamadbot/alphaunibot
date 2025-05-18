from flask import Flask, request, render_template
import requests
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/verify')
def verify():
    authority = request.args.get('Authority')
    status = request.args.get('Status')
    user_id = request.args.get('user_id')
    amount = 498000
    merchant_id = "MERCHANT-ID-YOU-GOT"

    if status == 'OK':
        res = requests.post(
            'https://api.zarinpal.com/pg/v4/payment/verify.json',
            json={
                "merchant_id": merchant_id,
                "amount": amount,
                "authority": authority
            }
        ).json()

        if res['data']['code'] == 100:
            try:
                with open("users.json", "r", encoding="utf-8") as f:
                    users = json.load(f)
            except:
                users = {}

            users[str(user_id)] = {"vip": True}

            with open("users.json", "w", encoding="utf-8") as f:
                json.dump(users, f, ensure_ascii=False, indent=2)

            return "پرداخت موفق بود. اشتراک VIP فعال شد."
        else:
            return "پرداخت ناموفق یا تکراری بود."
    return "پرداخت لغو شده."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)



