import requests
import random
import time
import sys
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from proxy_requests import ProxyRequests
from pyfiglet import Figlet

# I'm really sorry for this code. It is a mess.
# But it works and I am very lazy, so I think it will stay like this for a long time.
# I will work on this, some day.

class Bot():
    def __init__(self):
        f = Figlet(font='slant')
        print(f.renderText('JwdJ 2020 Bot'))
        self.vote_list = ['Wild/Wyld', 'Lost', 'Cringe']
        print('[#] Programmiert von EIonTusk')
        print('[#] Github: https://github.com/EIonTusk')
        print('----------------------------------------------------------------------')
        self.proxy = False
        self.proxy_list = False
        while True:
            print('[*] Willst du einen Proxyserver benutzen?[Y/n](Anonymer aber langsamer)')
            i = input('>>> ')
            if i in ['YES', 'Y', 'y', 'yes', 'ja', 'j', 'JA', 'J']:
                self.proxy = True
                break
            elif i in ['No', 'N', 'n', 'no', 'NEIN', 'Nein', 'nein']:
                self.proxy = False
                break
            else:
                print('[!] Ungültige Eingabe!')

        while True:
            print('[*] Gib dein Jugendwort des Jahres aus den Top10 ein.')
            print('[*] Top10: %s'%(self.vote_list))
            self.name = input('>>> ')
            self.vote = None
            for i in range(len(self.vote_list)):
                if self.vote_list[i] == self.name:
                    print('[+] Gültige Eingabe!')
                    self.vote = i
                    break

            if self.vote != None:
                break
            else:
                print('[!] Ungültige Eingabe!')

        self.trys = 0
        self.success = 0
        self.url = 'https://woerterbuch.langenscheidt.de/js20/top10/vote'
        self.url_site = 'https://woerterbuch.langenscheidt.de/js20/top10'
        self.headers = {'Host': 'woerterbuch.langenscheidt.de',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Content-Length': '525',
                        'Origin': 'null',
                        'Connection': 'keep-alive',
                        'Cookie': 'js20=eyJ0b3AzQWdlSWR4IjoyLCJ0b3AzV29yZElkeCI6MCwidG9wM0NvbnNlbnQiOjEsInZvdGVkVG9wMyI6MCwidG9wM1dvcmQiOiJXaWxkL1d5bGQifQ==; js20.sig=vnlpaOYf1Ym-DazwDNPWKC1i4Qo',
                        'Upgrade-Insecure-Requests': '1'}

        self.check = 'Wir haben deine Abstimmung gespeichert.'
        age_list = ['1', '2', '3', '4']

        while True:
            try:
                session = HTMLSession()
                r = session.get(self.url_site)
                r.html.render()
                session.close()
                soup = BeautifulSoup(r.html.html, 'html.parser')
                iframe = soup.find_all('iframe')[0]['src']
                r = requests.get(iframe)
                soup = BeautifulSoup(r.text, 'html.parser')
                token = soup.find(id='recaptcha-token')['value']
                print('[+] Recaptcha-Token bekommen')
                break
            except:
                print('[!] Nicht möglich Recaptcha-Token zu bekommen')
                print('[*] Versuche es nochmal')

        self.data = {'age': random.choice(age_list),
                     'w': str(self.vote),
                     'consent': '1',
                     'g-recaptcha-response': token}
        print('[*] Das Programm startet jetzt')

        self.loop()

    def send(self):
        try:
            if not self.proxy:
                r = requests.post(self.url, data=self.data, headers=self.headers)
            elif self.proxy:
                r = ProxyRequests(self.url)
                r.set_headers(self.headers)
                r.post_with_headers(self.data)
            else:
                sys.stdout.write('\r[!] Ein Fehler ist aufgetreten                                                      \r\n')
            if self.check in str(r) or self.check in r.text:
                self.success += 1
                sys.stdout.write('\r[+] Für %s abgestimmt                                                           \r\n' %self.name)
            else:
                sys.stdout.write('\r[!] Ein Fehler ist aufgetreten                                                      \r\n')
        except:
            sys.stdout.write('\r[!] Ein Fehler ist aufgetreten                                                      \r\n')
        self.trys += 1

    def loop(self):
        while True:
            self.send()
            sys.stdout.write('\rVersuche: %s, Erfolgreiche Versuche: %s, Fehlgeschlagene Versuche: %s' %(self.trys, self.success, self.trys - self.success))
            sys.stdout.flush()
            time.sleep(random.randint(1, 3))

if __name__ == '__main__':
    bot = Bot()
