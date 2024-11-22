
from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db.init_app(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    intro = db.Column(db.String(256), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>'  %  self.id


@app.route('/')
@app.route('/home')
def index():
    articles = Article.query.order_by(Article.date).all()
    return render_template('index.html', articles=articles)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return 'Ошибка добавления'
    else:
        return render_template('create.html')


@app.route('/<int:id>')
def index_el(id):
    details = Article.query.get(id)
    return render_template('details.html', details=details)


@app.route('/<int:id>/edit', methods=['POST', 'GET'])
def index_edit(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибка изменения"
    else:
        return render_template('update.html', article=article)



@app.route('/<int:id>/delete')
def index_delete(id):
    details = Article.query.get_or_404(id)
    try:
        db.session.delete(details)
        db.session.commit()
        return redirect('/')
    except:
        return "Ошибка удаления"


@app.route('/about')
def about():
    return render_template('about.html')





if __name__ == '__main__':
    app.run(debug=True)