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


@app.route('/api/article/ids', methods=['GET'])
def get_article_ids():
    article_ids = []
    c.execute("SELECT id FROM articles;")
    article_ids.append(c.fetchall())
    return jsonify(article_ids[0]), 200


@app.route('/api/article/getText', methods=['GET'])
def show_title():
    title = request.args.get('title', '')
    k = int(request.args.get('k', '10'))
    res = ''
    symbols = ["'", ',', '!', '?', '-', ':', ';', '@', '(', '<', '.', '!', '?', '"']

    def whoIsIt(title, k, symbols):
        about = 0
        if len(title) == 0:
            about = 0  # title is empty, ExR: ...
        elif len(title) <= k:
            about = 1  # title length <= count, ExR: title
        elif title[k - 1] == ' ':
            about = 2  # 25 symbol is whitespace, ExR: delete whitespace and add ...
        elif symbols.__contains__(title[k]):
            about = 3  # 25+1 symbol is punctuation mark, ExR: delete symbol and add ...
        elif title[k] == ' ':
            about = 4  # 25+1 symbol is whitespace, ExR: delete ' ' and add ...
        else:
            about = 5  # other

        return about

    def delete_symb(res):
        j = len(res)
        while res[j - 1] in symbols:
            j -= 1
        return res[:j]

    about = whoIsIt(title, k)
    # print(about)

    if about == 0:
        return "..."
    elif about == 1:
        return title
    elif about == 2 or about == 3:
        return delete_symb(title[:k - 1]) + "..."
    elif about == 4:
        return delete_symb(title[:k]) + "..."
    else:
        i = k-1
        while title[i] != " " and i > 0:
            i -= 1
            if i != 0 and title[i] not in symbols:
                return title[:i] + '...'
            else:
                return title[:k] + '...'





if __name__ == '__main__':
    app.run(debug=True)
