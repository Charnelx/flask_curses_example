from flask_example import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    email = db.Column(db.Text)
    pw_hash = db.Column(db.Text)

    def __init__(self, username, email, pw_hash):
        self.username = username
        self.email = email
        self.pw_hash = pw_hash

    def __repr__(self):
        return '<User %r>' % self.username

class Topics(db.Model):

    _id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors._id'))
    author = db.relationship('Authors',
                                 backref=db.backref('all_topics', lazy='dynamic'))
    title = db.Column(db.Text)
    url = db.Column(db.Text)

    def __init__(self, author, title, url):
        self.author = author
        self.title = title
        self.url = url

    def __repr__(self):
        return '<%r by %r>' % (self.title, self.author)

class Authors(db.Model):

    _id = db.Column(db.Integer, primary_key=True)
    nickname =  db.Column(db.String(128))

    def __init__(self, nickname):
        self.nickname = nickname

    def __repr__(self):
        return '<User nick: %r>' % self.nickname

if __name__ == '__main__':
    db.create_all()

    user1 = Authors('Борман')
    user2 = Authors('Nashorn')
    user3 = Authors('ati76')

    topic1 = Topics(user1, 'HP 15-ah155n', 'http://forum.overclockers.ua/viewtopic.php?f=26&t=128672')
    topic2 = Topics(user2, 'Видеокарту MSI N680GTX Lightning 2GB', 'http://forum.overclockers.ua/viewtopic.php?f=26&t=172547')
    topic3 = Topics(user3, 'Кулер Scythe Mugen 3', 'http://forum.overclockers.ua/viewtopic.php?f=26&t=173926')

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(topic1)
    db.session.add(topic2)
    db.session.add(topic3)

    db.session.commit()
