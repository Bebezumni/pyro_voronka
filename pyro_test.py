from pyrogram import Client, filters
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import asyncio

bot_token = ''
api_id = ''
api_hash = ''
app = Client(
    'my_userbot',
    bot_token=bot_token,
    api_id=api_id,
    api_hash=api_hash,
)
engine = create_engine('sqlite:///userbot.db')
Base = declarative_base()
msg1='Текст 1 сообщения'
msg2='Текст 2 сообщения'
msg3='Текст 3 сообщения'
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default='alive')
    status_updated_at = Column(DateTime, default=datetime.utcnow)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session()

@app.on_message(filters.text)
async def handle_first_message(client, message):
    print('message found')
    user_id = message.from_user.id
    existing_user = db_session.query(User).filter_by(id=user_id).first()
    if not existing_user:
        new_user = User(id=user_id)
        db_session.add(new_user)
        db_session.commit()
        asyncio.create_task(first_timer(user_id))
        print('первый таймер запущен')

def message_checker(text):
    if 'прекрасно' in text:
        return 'Stop'
    elif 'ожидать' in text:
        return 'Stop'
    else:
        return 'Go on'

def trigger_check(text):
    if 'Триггер 1' in text:
        return 'Stop'

async def first_timer(user_id):
    print('1 timer on')
    await asyncio.sleep(6 * 60)
    user = db_session.query(User).filter_by(id=user_id).first()
    if user and user.status == 'alive':
        print('user alive')
        if message_checker(msg1) == 'Stop':
            print('stop detected')
            user.status = 'finished'
            user.status_updated_at = datetime.utcnow()
            db_session.commit()
        else:
            print('trying to send reply')
            try:
                await app.send_message(user_id, msg1)
            except Exception as e:
                existing_user = db_session.query(User).filter_by(id=user_id).first()
                if existing_user:
                    existing_user.status = 'dead'
                    existing_user.status_updated_at = datetime.utcnow()
                    db_session.commit()
                    print(f'Error sending message to user {user_id}: {str(e)}')
            if message_checker(msg2)== 'Stop':
                asyncio.create_task(third_timer(user_id))
                print('Второй таймер остановен триггером, запускаем третий')
            else:
                asyncio.create_task(second_timer(user_id))
                print('Второй таймер запущен')

async def second_timer(user_id):
    print('2 timer on')
    await asyncio.sleep(39 * 60)
    user = db_session.query(User).filter_by(id=user_id).first()
    if user and user.status == 'alive':
        if message_checker(msg2) == 'Stop':
            user.status = 'finished'
            user.status_updated_at = datetime.utcnow()
            db_session.commit()
        else:
            try:
                await app.send_message(user_id, msg2)
            except Exception as e:
                existing_user = db_session.query(User).filter_by(id=user_id).first()
                if existing_user:
                    existing_user.status = 'dead'
                    existing_user.status_updated_at = datetime.utcnow()
                    db_session.commit()
                    print(f'Error sending message to user {user_id}: {str(e)}')
            asyncio.create_task(third_timer(user_id))
            print('Третий таймер запущен')
async def third_timer(user_id):
    print('3 timer on')
    await asyncio.sleep(26 * 60 * 60)
    user = db_session.query(User).filter_by(id=user_id).first()
    if user and user.status == 'alive':
        if message_checker(msg2) == 'Stop':
            user.status = 'finished'
            user.status_updated_at = datetime.utcnow()
            db_session.commit()
        else:
            try:
                await app.send_message(user_id, msg3)
            except Exception as e:
                existing_user = db_session.query(User).filter_by(id=user_id).first()
                if existing_user:
                    existing_user.status = 'dead'
                    existing_user.status_updated_at = datetime.utcnow()
                    db_session.commit()
                    print(f'Error sending message to user {user_id}: {str(e)}')
app.run()
