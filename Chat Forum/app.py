from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'

db = SQLAlchemy(app)
app.app_context().push()


class Forum(db.Model):
    __tablename__ = 'ForumTable'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    description = db.Column(db.Text)


# db.create_all()


@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        forums = Forum.query.all()
        return render_template('index.html', forums=forums)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        forum = Forum(author='Danush', title=title, description=description)
        db.session.add(forum)
        db.session.commit()
        return redirect('/')


@app.route('/delete-post/<id>')
def delete_post(id):
    forum = Forum.query.filter_by(id=id).first()
    db.session.delete(forum)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
