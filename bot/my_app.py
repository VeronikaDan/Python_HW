import flask
import telebot
import conf

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)

bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

from gensim.models import Word2Vec
import pymorphy2
m = pymorphy2.MorphAnalyzer()
model = Word2Vec.load('model_2007')

def wordvec(word, pos):
    try:
        vec = model[word]
        syns = model.most_similar(positive=[vec], topn=30)
        res = []
        for s in syns:
            morph = m.parse(s[0])[0]
            pos_s = morph.tag.POS
            lemma = morph.normal_form
            if (pos_s == pos) and (lemma != word):
                res.append(s[0])
        if len(res) !=0:
            return res
        else:
            return 0
    except:
        return 0
    
    
    
def answer(mess):
    words = mess.split()
    ans = ''
    for w in words:
        w = w.strip('[](),.;:-_+=/*"«»!?<>')
        morph = m.parse(w)[0]
        lemma = morph.normal_form
        pos = morph.tag.POS
        syns = wordvec(lemma, pos)
        if syns == 0:
            continue
        else:
            ans += syns[0]
            ans += ' '
	if ans == '':
		ans = 'моя твоя не понимать!'
    return ans

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "привет, насяника! я повторять твой слова на мой лад!")


@bot.message_handler(func=lambda m: True)
def dude(message):
    try:
        ans = answer(message.text)
    except:
        ans = "отдых, насяника!"
    bot.send_message(message.chat.id, ans)

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

# функция, которая запускается, когда к нам постучался телеграм 
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
	
