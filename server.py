from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    user_agent = request.headers.get('User-Agent')
    return (f'<h1>Hello, bro!</h1> \r\n'
            f'<h2>Lol your  11 bro is %s</h2>' % user_agent)


@app.route('/user/<name>')
def user(name):
    return 'Hello, %s' % name


# function to check if a number is a PEST number
def is_pest(number):
    if 0 < number <= 400:
        return 0
    elif 400 < number <= 1000:
        return 1
    elif 1000 < number <= 5000:
        return 2
    elif 5000 < number <= 15000:
        return 3
    else:
        return 4

# endpoint to handle GET requests
@app.route('/api/pest/<int:number>', methods=['GET'])
def check_pest(number):
    if number < 0 or number > 16000:
        return jsonify({'error': 'Number out of range'}), 400
    else:
        result = is_pest(number)
        return jsonify({'is_pest': result}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
