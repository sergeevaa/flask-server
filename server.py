from flask import Flask, request, jsonify
from flask_cors import CORS
# import json
import pymysql
import sshtunnel

sshtunnel.SSH_TIMEOUT = 25.0
sshtunnel.TUNNEL_TIMEOUT = 25.0

app = Flask(__name__)  # g36eLvNOgV
cors = CORS(app, resources={r'/api/*': {'origins': '*'}})

db_blog = pymysql.connect(host='olebbj.mysql.pythonanywhere-services.com', user='olebbj', passwd='1111qwe!QWE',
                          db='olebbj$blog', connect_timeout=180, port=3306)
c = db_blog.cursor()
print(c.execute("SHOW TABLES;"))
tables = c.fetchall()
for table in tables:
    print(table)

c.execute("SELECT * FROM articles;")
rows = c.fetchall()
for row in rows:
    print(row)


@app.route('/')
def home():
    user_agent = request.headers.get('User-Agent')
    return (f'<h1>Hello! \r\n'
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


@app.route('/api/article/<int:id>', methods=['GET'])
def get_article_name(id):
    c.execute("SELECT * FROM articles WHERE id = %s;", (id,))
    articles = c.fetchone()

    if articles:
        id_articles, title, description = articles[0], articles[1], articles[2]
        response = {'id': id_articles, 'title': title, 'description': description}
        return jsonify(response), 200
    else:
        response = {'error': 'ID not found'}
        return jsonify(response), 404


@app.route('/api/article/count', methods=['GET'])
def get_articles_count():
    c.execute("SELECT COUNT(*) FROM articles;")
    count = c.fetchone()[0]

    if count > 0:
        response = {'count': count}
        return jsonify(response), 200
    else:
        response = {'message': 'No rows found'}
        return jsonify(response), 404


@app.route('/api/article/all/id', methods=['GET'])
def get_all_articles_id():
    c.execute("SELECT id FROM articles;")
    articles_id = c.fetchone()

    if len(articles_id) == 0:
        return jsonify({'error': 'No IDs found.'}), 404
    else:
        id_list = [item['id'] for item in articles_id]
        return jsonify({'ids': id_list})


if __name__ == '__main__':
    app.run(debug=True)
