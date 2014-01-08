from pyquery.pyquery import PyQuery
import requests

total_data = ''
host = 'gleitzman.com'

def extract_data(text):
    global total_data
    pq = PyQuery(text)
    data = pq.find('p.data').text()
    total_data = total_data + data
    nextState = pq.find('.nextState').attr('value')
    return nextState

def crank():
    r = requests.get('http://{0}:1337'.format(host))
    nextState = extract_data(r.text)
    while nextState:
        r = requests.post('http://{0}:1337/next'.format(host), {'nextState': nextState})
        nextState = extract_data(r.text)
        print 'Found {0} bytes'.format(len(total_data))

    print "done!!"
    with open('thing.mp3', 'w') as f:
        f.write(total_data.decode('hex'))

if __name__ == "__main__":
    crank()
