from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import Session, sessionmaker

from .schema import User

class Database():
    
    def __init__(self):
        self.engine = create_engine(url='sqlite+pysqlite:///database/database.db', echo=True)

    def _test(self):

        with Session(self.engine) as sess:
            t = text("SELECT 'Hello World';")
            sess.execute(t)
            sess.commit()

    def _init_db(self):
        User.metadata.create_all(self.engine)        
        print('database created')

        
    def _create_user(self, **kwargs):
        
        username = kwargs.get('username', None)
        chat_id = kwargs.get('chat_id')
        created_at = kwargs.get('created_at')
        firstname = kwargs.get('firstname')

        with Session(self.engine) as s:
            stmt =  select(User).filter_by(chat_id = chat_id)
            row = s.execute(stmt).first()
            print(f'user_id {row}')

            if row is None:
                user = User(chat_id=chat_id, username=username, firstname=firstname, created_at=created_at)
                s.add(user)
                s.commit()
                print(f'user {username} added')
