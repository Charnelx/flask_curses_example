from scraper_app.models import User, Topics, Authors, db
from flask_example import app

if __name__ == '__main__':
    with app.app_context() as context:
        db.init_app(context.app)

        db.create_all()

        user1 = Authors('Борман')
        user2 = Authors('Nashorn')
        user3 = Authors('ati76')

        topic1 = Topics(user1, 'HP 15-ah155n', 'http://forum.overclockers.ua/viewtopic.php?f=26&t=128672')
        topic2 = Topics(user2, 'Видеокарту MSI N680GTX Lightning 2GB', 'http://forum.overclockers.ua/viewtopic.php?f=26&t=172547')
        topic3 = Topics(user3, 'Кулер Scythe Mugen 3', 'http://forum.overclockers.ua/viewtopic.php?f=26&t=173926')
        topic4 = Topics(user2, 'Ati radeon 9600 XT', 'http://forum.overclockers.ua/viewtopic.php?f=26&t=173977')

        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.add(topic1)
        db.session.add(topic2)
        db.session.add(topic3)
        db.session.add(topic4)

        db.session.commit()



        '''Queries on related fields example'''
        # topics = Topics.query.all()
        # for topic in topics:
        #     print('Author nickname by foreign key: {}'.format(topic.author.nickname))
        #
        #     a_id = topic.author_id
        #     author = Authors.query.filter_by(_id = a_id).first()
        #     print('Author nickname by Authors model filter with _id field: {}'.format(author.nickname))
