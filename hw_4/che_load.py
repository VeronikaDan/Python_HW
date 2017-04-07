import urllib.request, json, re, os

def get_wall(no):
    url = 'https://api.vk.com/method/wall.get?count=100&owner_id=' + no
    posts = {}
    comments = {}
    for i in [0,100,200,300,400]:
        if i!=0:
            url = url + '&offset=' + str(i)
        res = urllib.request.urlopen(url).read().decode('utf-8')
        wall = json.loads(res)
        wall = wall['response'][1:]
        for post in wall:
            if post['marked_as_ads'] == 0:
                post_id = post['id']
                print('post_id - '+str(post_id))
                comm_count = post['comments']['count']
                post_info = {}
                post_info['words'] = count_words(post['text'])
                post_info['likes'] = post['likes']['count']
                posts[post_id] = post_info
                com = get_comments(no, post_id, comm_count)
                for k, v in com.items():
                    comments[k] = v
    return posts, comments
    

def get_comments(no, post_id, count):
    comments = {}
    url_comm = 'https://api.vk.com/method/wall.getComments?owner_id='+no \
               +'&need_likes=1&post_id='+str(post_id)
    tens = int(count/10) + 1
    print('how many tens of comms - ' + str(tens))
    for i in range(tens):           
        res_comm = urllib.request.urlopen(url_comm).read().decode('utf-8')
        comms = json.loads(res_comm)
        comms = comms['response'][1:]
        for com in comms:
            com_info = {}
            print('comm_id - '+str(com['cid']))
            com_info['words'] = count_words(com['text'])
            com_info['likes'] = com['likes']['count']
            com_info['from_who'] = get_user_info(com['from_id'])
            comments[com['cid']] = com_info
    return comments
            
            
def get_user_info(user_id):
    print('user_id - '+str(user_id))
    user_info = {}
    if user_id > 0:
        url = 'https://api.vk.com/method/users.get?fields=bdate,city&' \
              + 'user_ids=' + str(user_id)
        res = urllib.request.urlopen(url).read().decode('utf-8')
        user = json.loads(res)
        user = user['response'][0]        
        if 'bdate' in user:
            user_info['bdate'] = good_bd(user['bdate'])
        else:
            user_info['bdate'] = '-'
        if 'city' in user:
            if user['city'] != 0:        
                user_info['city'] = get_city_name(user['city'])
            else:
                user_info['city'] = '-'
        else:
            user_info['city'] = '-'
    else:
        user_info['bdate'] = '-'
        user_info['city'] = '-'
    return user_info

    
def count_words(text):
    words = text.split()
    return len(words)


def get_city_name(city_id):
    print('city_id - '+str(city_id))
    url_city = 'https://api.vk.com/method/database.getCitiesById?city_ids='\
                + str(city_id)
    res_city = urllib.request.urlopen(url_city).read().decode('utf-8')
    city = json.loads(res_city)
    city = city['response'][0]['name']
    print(city)
    return city


def good_bd(bdate):
    dots = re.findall(r'\.', bdate)
    if len(dots) == 2:
        years = str(2017 - int(bdate[-4:]))
        print(years)
        return years
    else:
        print('no year of bd')
        return '-'

              
def dump(text, name):
    f = open(name+'.json', 'w', encoding='utf-8')
    json.dump(text, f, indent = 2, ensure_ascii = False)
    f.close()


def posts_to_tsv(posts):
    i = 0
    for key, info in posts.items():
        if i == 0:
            f = open('posts.tsv', 'w', encoding='utf-8')
            i += 1
        else:
            f = open('posts.tsv', 'a', encoding='utf-8')
        text = str(key)+'\t'+str(info['words'])+'\t'+str(info['likes'])+'\n'
        f.write(text)


def comments_to_tsv(comms):
    i = 0
    for key, info in comms.items():
        if i == 0:
            f = open('comments.tsv', 'w', encoding='utf-8')
            i += 1
        else:
            f = open('comments.tsv', 'a', encoding='utf-8')
        text = str(key)+'\t'+str(info['words'])+'\t'+str(info['likes'])\
               +'\t'+info['from_who']['bdate']+'\t'+info['from_who']['city']+'\n'
        f.write(text)


if __name__ == '__main__':
    info = get_wall('-53845179')
    dump(info[0], 'posts_che')
    dump(info[1], 'comments_che')
    posts_to_tsv(info[0])
    comments_to_tsv(info[1])
