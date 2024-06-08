from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    model = request.form['model']
    start_day = request.form['start_day']
    rental_days = int(request.form['rental_days'])
    review_discount = request.form['review_discount']

    model_prices = {
        "s24울트라": 60000,
        "s23울트라": 50000,
        "s22울트라": 40000,
        "Iphone 15 Pro Max": 65000,
        "Iphone 15 Pro": 50000,
        "Iphone 14 Pro": 40000
    }

    review_discount_values = {
        "리뷰할인 미신청": 0,
        "리뷰할인 1개 신청": 5000,
        "리뷰할인 2개 신청": 10000
    }

    weekday_discount = 5000
    additional_day_discount = 10000

    model_price = model_prices[model]
    review_discount_value = review_discount_values[review_discount]

    total_weekdays = calculate_weekdays(start_day, rental_days)

    rental_price = ((model_price - review_discount_value) * rental_days
                    - (total_weekdays * weekday_discount)
                    - ((rental_days - 1) * additional_day_discount))
                    
    return render_template('result.html', price=rental_price)

def calculate_weekdays(start_day, rental_days):
    weekdays = ["월", "화", "수", "목", "금"]
    all_days = ["월", "화", "수", "목", "금", "토", "일"]
    start_index = all_days.index(start_day)
    total_weekdays = 0
    
    for i in range(rental_days):
        current_day = all_days[(start_index + i) % 7]
        if current_day in weekdays:
            total_weekdays += 1
            
    return total_weekdays

if __name__ == '__main__':
    app.run(debug=True)
