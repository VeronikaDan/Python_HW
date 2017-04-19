import sqlite3
con = sqlite3.connect('vk_group.db')
cur = con.cursor()


def create_database():
    cur.execute('create table groups (id int primary key, name text)')
    con.commit()

    cur.execute('create table posts (id int primary key, post_text text)')
    con.commit()

    cur.execute('create table users (id int primary key, date_of_birth text, city text)')
    con.commit()

    cur.execute('create table comments (id int primary key, comment_text text, to_post int, to_comment int, ' +
                'from_who int, time text, foreign key (to_comment) references posts(id),' +
                'foreign key (from_who) references users(id))')
    con.commit()
