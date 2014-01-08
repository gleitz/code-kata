from crypto import EncodeAES, DecodeAES
from Crypto.Cipher import AES
from flask import Flask, render_template, jsonify, request, url_for
import hashlib
import sys
from flaskutil import ReverseProxied

cipher = AES.new('\xc4^\xbaa_\x8f\x9aaC\xa7xlu\xa0\x0b0\xba\x89Y\xa7_\x1d \x944\xab<\xa5\x98\xae\xb70')

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def encode(text):
    return EncodeAES(cipher, text)

def decode(text):
    return DecodeAES(cipher, text)

def sha1(text):
    return hashlib.sha1(text).hexdigest()

with open('data/rick.mp3', 'rb') as RICK:
    RICK_DATA = RICK.read()
    RICK_PIECES = list(chunks(RICK_DATA, (len(RICK_DATA) / 10) + 8))

rhyme = ['the', 'itsy', 'bitsy', 'spider', 'climbed', 'up', 'da', 'water', 'spout', '!']

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)

def _nedry():
    return render_template('template.html',
                           top = 244,
                           left = 449,
                           title = 'Ah ah ah, you didn\'t say the magic verb',
                           edison_url = url_for('static',filename='nedry.jpg'))

def _success():
    return render_template('template.html',
                           title = 'Almost there!!',
                           top = 114,
                           left = 200,
                           edison_url = url_for('static',filename='hex.png'))

def _final():
    return 'http://{0}{1}'.format(request.host, url_for('static',filename='congrats.jpg'))

def _get_piece(num):
    data = RICK_PIECES[num].encode('hex')
    return render_template('template.html',
                           data = data,
                           top = 283,
                           left = 500,
                           title = 'Puzzle',
                           relay_state = sha1(rhyme[num]),
                           edison_url = url_for('static', filename='edison.jpg'))
@app.route("/")
def home():
    return _get_piece(0)

@app.route("/next", methods = ['GET', 'POST'])
def login():
    if request.method == 'GET' or not request.form.get('nextState'):
        return _nedry()
    next_state = request.form['nextState']
    if next_state.lower() == 'rickrolle':
        return _final()
    current_page = -1
    for i, word in enumerate(rhyme):
        if sha1(word) == next_state:
            current_page = i
    if current_page == -1:
        return _nedry()
    print "current page is", current_page
    next_page = current_page + 1
    if next_page >= len(RICK_PIECES):
        return _success()
    return _get_piece(next_page)

if __name__ == "__main__":
    debug = False
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        debug = True
    app.run(host='0.0.0.0', debug=debug, port=1337)
