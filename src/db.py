import sqlite3

import settings

connection = sqlite3.connect(settings.DATABASE_FILE)


def init_db():
    execute('''
        create table if not exists message (
            id integer primary key autoincrement,
            chat_id integer not null,
            message_id integer not null,
            user_id integer not null,
            foreign key(user_id) references telegram_user(id)
        )
    ''')

    execute('''
        create table if not exists telegram_user (
            id integer primary key autoincrement,
            username text not null,
            fullname text not null 
        )
    ''')

    execute('''  
        create table if not exists reaction (
            id integer primary key autoincrement,
            user_id integer not null,
            chat_id integer not null,
            emoji_id text not null,
            delta integer not null,
            created_at integer default current_timestamp,
            foreign key(user_id) references telegram_user(id)
        )
    ''')


def execute(sql: str, arguments: tuple = None):
    cursor = connection.cursor()
    data = cursor.execute(sql, arguments or tuple()).fetchall()
    connection.commit()
    cursor.close()
    return data
