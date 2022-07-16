from flask import Flask, render_template, request, redirect, json, url_for
import datetime

app = Flask(__name__)

file = open('cat.txt', 'r', encoding='utf-8')
cats = json.loads(file.read())
file.close()

ooo = {}

@app.route('/parol', methods=['GET'])
def parol_get():
    flag = ''
    return render_template('parol.html', cats=cats, flag=flag)

@app.route('/parol', methods=['POST'])
def parol_post():
    global ooo
    file = open('cat.txt', 'r', encoding='utf-8')
    cat = json.loads(file.read())
    file.close()
    i = ooo
    if request.form['pasword'] == '630303' and request.form['name'] == 'imeliorut@gmail.com':
        cat.pop(cat.index(i))
        qwerty = json.dumps(cat)
        file = open('cat.txt', 'w', encoding='utf-8')
        file.write(qwerty)
        file.close()
        return redirect('/')
    flag = ' d-none'
    return redirect('/parol')

@app.route('/del', methods=['GET'])
def delete_get():
    return render_template('delete.html', cats=cats)

@app.route('/del', methods=['POST'])
def delete_post():
    global ooo
    file = open('cat.txt', 'r', encoding='utf-8')
    cat = json.loads(file.read())
    file.close()
    for i in cat:
        if request.form['name'] ==  i['name']:
            ooo = i
            return redirect('/parol')
    return redirect('/del')

@app.route('/', methods=['GET'])
def index():
    file = open('cat.txt', 'r', encoding='utf-8')
    cats = json.loads(file.read())
    file.close()
    return render_template('index.html', cats=cats)

@app.route('/spravka', methods=['GET'])
def abc():
    return render_template('info.html')

@app.route('/konf', methods=['GET'])
def vision():
    return render_template('konfi.html')

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
    file = open('cat.txt', 'r', encoding='utf-8')
    cats = json.loads(file.read())
    file.close()
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