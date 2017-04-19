from hw_5.create_bd import *
import urllib.request, json, datetime


def get_wall(no, name):
    cur.execute('select id from groups where id=' + str(no) + '')
    match = cur.fetchall()
    if not match:
        cur.execute('insert into groups (id, name) values (%s, "%s")' % (no, name))
        con.commit()
    url = 'https://api.vk.com/method/wall.get?count=100&owner_id=' + str(no)
    for i in [0, 100, 200, 300, 400]:
        if i != 0:
            url = url + '&offset=' + str(i)
        res = urllib.request.urlopen(url).read().decode('utf-8')
        wall = json.loads(res)
        wall = wall['response'][1:]
        for post in wall:
            if post['marked_as_ads'] == 0:
                post_id = post['id']
                print('post_id - ' + str(post_id))
                comm_count = post['comments']['count']
                post_text = post['text']
                post_text = post_text.replace('\"', '*')
                cur.execute('select id from posts where id=' + str(post_id) + '')
                match = cur.fetchall()
                if not match:
                    cur.execute('insert into posts (id, post_text) values (%s, "%s")' % (post_id, post_text))
                    con.commit()
                    get_comments(no, post_id, comm_count)


def get_comments(no, post_id, count):
    url_comm = 'https://api.vk.com/method/wall.getComments?owner_id=' + str(no) \
               + '&post_id=' + str(post_id)
    tens = int(count / 10) + 1
    for i in range(tens):
        res_comm = urllib.request.urlopen(url_comm).read().decode('utf-8')
        comms = json.loads(res_comm)
        comms = comms['response'][1:]
        for com in comms:
            com_id = com['cid']
            print('com_id - ' + str(com_id))
            com_text = com['text']
            com_text = com_text.replace('\"', '*')
            from_who = com['from_id']
            get_user_info(from_who)
            if 'reply_to_cid' in com:
                to_comment = com['reply_to_cid']
            else:
                to_comment = 0
            time = dt(com['date'])
            cur.execute('select id from comments where id=' + str(com_id) + '')
            match = cur.fetchall()
            if not match:
                cur.execute('insert into comments (id, comment_text, to_post, to_comment, from_who, time) ' +
                            'values (%s, "%s", %s, %s, %s, "%s")' %
                            (com_id, com_text, post_id, to_comment, from_who, time))
                con.commit()


def dt(u): return datetime.datetime.fromtimestamp(u)


def get_user_info(user_id):
    if user_id > 0:
        url = 'https://api.vk.com/method/users.get?fields=bdate,city&' \
              + 'user_ids=' + str(user_id)
        res = urllib.request.urlopen(url).read().decode('utf-8')
        user = json.loads(res)
        user = user['response'][0]
        if 'bdate' in user:
            bdate = user['bdate']
        else:
            bdate = '-'
        if 'city' in user:
            if user['city'] != 0:
                city = get_city_name(user['city'])
            else:
                city = '-'
        else:
            city = '-'
    else:
        bdate = '-'
        city = '-'
    cur.execute('select id from users where id=' + str(user_id) + '')
    match = cur.fetchall()
    if not match:
        cur.execute('insert into users (id, date_of_birth, city) values (%s, "%s", "%s")' % (user_id, bdate, city))
        con.commit()


def get_city_name(city_id):
    url_city = 'https://api.vk.com/method/database.getCitiesById?city_ids=' \
               + str(city_id)
    res_city = urllib.request.urlopen(url_city).read().decode('utf-8')
    city = json.loads(res_city)
    city = city['response'][0]['name']
    return city


if __name__ == '__main__':
    #create_database()
    get_wall('-53845179', 'che')
