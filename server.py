from flask import Flask, render_template, request, redirect, json, url_for
import datetime

app = Flask(__name__)

file = open('cat.txt', 'r', encoding='utf-8')
cats = json.loads(file.read())
file.close()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', cats=cats)


@app.route('/add', methods=['GET'])
def add_form():
    return render_template('add.html')


@app.route('/add', methods=['POST'])
def add():
    fields = ['name', 'photo', 'description']
    for field in fields:
        if request.form.get(field, '') == '':
            return redirect('/add')
    cat = {
        "name": request.form['name'],
        "description": request.form['description'],
        "photo": request.form['photo'],
        "comments": [],
        "date": str(datetime.datetime.today()).split()[0],
        "likes": 0
    }
    cats.append(cat)
    qwerty = json.dumps(cats)
    file = open('cat.txt', 'w', encoding='utf-8')
    file.write(qwerty)
    file.close()
    return redirect('/cats/{0}'.format(len(cats)))

@app.route('/cats/<id>', methods=['GET'])
def details(id):
    cat = cats[int(id) - 1]
    return render_template('details.html', cat=cat, id=id)

@app.route('/like/<id>', methods=['GET'])
def like(id):
    cat = cats[int(id) - 1]
    cat['likes'] += 1
    cats[int(id) - 1] = cat
    qwerty = json.dumps(cats)
    file = open('cat.txt', 'w', encoding='utf-8')
    file.write(qwerty)
    file.close()
    return redirect('/cats/{}'.format(id))
@app.route('/dislike/<id>', methods=['GET'])
def dislike(id):
    cat = cats[int(id) - 1]
    cat['likes'] -= 1
    cats[int(id) - 1] = cat
    qwerty = json.dumps(cats)
    file = open('cat.txt', 'w', encoding='utf-8')
    file.write(qwerty)
    file.close()
    return redirect('/cats/{}'.format(id))
@app.route('/coment/<id>', methods=['GET'])
def comment_form(id):
    return render_template('coment.html')
@app.route('/coment/<id>', methods=['POST'])
def  comment(id):
    cat = cats[int(id) - 1]
    coment = {}
    coment['author'] = request.form.get("author","Неизвестно")
    if coment['author'] == '':
        coment['author'] = "Неизвестно"
    coment['text'] = request.form.get("text", "Неизвестно")
    if coment['text'] == '':
        coment['text'] = "Неизвестно"
    coment['date'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
    cat["comments"].append(coment)
    cats[int(id) - 1] = cat
    qwerty = json.dumps(cats)
    file = open('cat.txt', 'w', encoding='utf-8')
    file.write(qwerty)
    file.close()
    return redirect ('/cats/{}'.format(id))
@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))
app.run(debug=True, port=8100)