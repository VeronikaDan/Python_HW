import urllib.request, json, re
from access import ACCESS_TOKEN
users = {}

def get_messages(no):
    url = 'https://api.vk.com/method/messages.getHistory?count=200&user_id=c' + no\
          + '&chat_id=' + no + '&access_token=' + ACCESS_TOKEN
    messages = {}    
    for i in [c * 200 for c in range(20)]:
        if i!=0:
            url = url + '&offset=' + str(i)
        res = urllib.request.urlopen(url).read().decode('utf-8')
        mess = json.loads(res)
        mess = mess['response'][1:]
        for m in mess:
            m_id = m['mid']
            print('m_id - '+str(m_id))
            m_info = {}
            m_info['words'] = count_words(m['body'])
            if not (m['from_id']% 100000) in users:
                bro_id = add_user(m['from_id'])
                print('bro_id = '+ str(bro_id))
            m_info['from_who'] = bro_id
            messages[m_id] = m_info
    return messages
               
            
def get_user_info(user_id):
    print('user_id - '+str(user_id))
    url = 'https://api.vk.com/method/users.get?fields=first_name,last_name&' \
            + 'user_ids=' + str(user_id)
    res = urllib.request.urlopen(url).read().decode('utf-8')
    user = json.loads(res)
    user = user['response'][0]
    user_info = {}
    user_info['name'] = user['first_name'] + ' ' + user['last_name']
    user_info['real_id'] = user_id
    print(user_info['name'])
    return user_info

    
def add_user(user_id):
    nick = user_id % 100000
    user = get_user_info(user_id)
    users[nick] = user
    return nick
    
    
def count_words(text):
    words = text.split()
    return len(words)

              
def dump(text, name):
    f = open(name+'.json', 'w', encoding='utf-8')
    json.dump(text, f, indent = 2, ensure_ascii = False)
    f.close()


def messages_to_tsv(posts):
    i = 0
    for key, info in posts.items():
        if i == 0:
            f = open('messages.tsv', 'w', encoding='utf-8')
            i += 1
        else:
            f = open('messages.tsv', 'a', encoding='utf-8')
        text = str(key)+'\t'+str(info['words'])+'\t'+str(info['from_who'])+'\n'
        f.write(text)


if __name__ == '__main__':
    info = get_messages('7')
    dump(info, 'messages_bros')
    messages_to_tsv(info)
    dump(users, 'bros')
