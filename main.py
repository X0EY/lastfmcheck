import json
import random
import requests
import multiprocessing.dummy as mp

# config
SeshFM = 'SESSION ID HERE'
CSRFToken = 'CSRF TOKEN HERE'
pcount = 15

cookies = {'csrftoken': CSRFToken,
           'sessionid': SeshFM}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'referer': 'https://www.last.fm/join'}

with open("list.txt") as f:
    namelist = [line.rstrip('\n') for line in f]

with open("proxies.txt") as f:
    proxylist = [line.rstrip('\n') for line in f]


def check(name):
    try:
        url = 'https://www.last.fm/join/partial/validate'
        data = {'csrfmiddlewaretoken': CSRFToken,
                'userName': name}
        x = requests.post(url, cookies=cookies, headers=headers, data=data, timeout=(6, 10),
                          proxies=dict(http='socks5://' + random.choice(proxylist) + ':1080',
                                       https='socks5://' + random.choice(proxylist) + ':1080'))
        if "Not quite so fast" in x.text:
            jsdata = json.loads(x.text)

            if str(jsdata['userName']['valid']) == "True":
                print(name + ' - Available')
                available = open("available.txt", "a")
                available.write(name + "\n")
                available.close()
            elif str(jsdata['userName']['valid']) == "False":
                print(name + ' - Taken')
                taken = open("taken.txt", "a")
                taken.write(name + "\n")
                taken.close()
            else:
                print(name + ' - Error')
                error = open("error.txt", "a")
                error.write(name + "\n")
                error.close()
        else:
            if "429 Too Many Requests" in x.text:
                print('Error 429 - Too Many Requests')

            elif "406 Not Acceptable" in x.text:
                print('Error 406 - Not Acceptable')
    except requests.exceptions.Timeout as e:
        # Maybe set up for a retry
        print(e)
    except requests.exceptions.RequestException as e:
        print(e)


if __name__ == '__main__':
    p = mp.Pool(pcount)
    p.map(check, namelist)
    p.close()
    p.join()
