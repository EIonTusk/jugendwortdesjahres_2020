import requests
import random
import time
import sys
from bs4 import BeautifulSoup
from requests_html import HTMLSession

class Bot():
    def __init__(self):
        self.vote_list = ['Schabernack', 'Mittwoch', 'Sauftrag', 'Wild/Wyld', 'Lost', 'no front', 'Köftespieß',
                          'Digga/Diggah', 'Cringe', 'Mashallah']
        print('[#] Programmiert von EIonTusk')
        print('[#] Github: https://github.com/EIonTusk')
        while True:
            print('----------------------------------------------------------------------')
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
        self.url = "https://woerterbuch.langenscheidt.de/js20/top10/vote"
        self.url_site = 'https://woerterbuch.langenscheidt.de/js20/top10'
        self.headers = {'Host': 'woerterbuch.langenscheidt.de',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Content-Length': '461',
                        'Origin': 'null',
                        'Connection': 'keep-alive',
                        'Cookie': 'js20=eyJ0b3AxMEFnZUlkeCI6MiwidG9wMTBXb3JkSWR4IjowLCJ0b3AxMENvbnNlbnQiOjEsInZvdGVkVG9wMTAiOjAsInZvdGVkVG9wMTBXb3JkIjoiU2NoYWJlcm5hY2sifQ==; js20.sig=W0UAPnkamc9lOvQRdLP4hJNhdRs',
                        'Upgrade-Insecure-Requests': '1',
                        'TE': 'Trailers'}
        self.check = 'Wir haben deine Abstimmung gespeichert.'
        age_list = ['1', '2', '3', '4']
        session = HTMLSession()
        r = session.get(self.url_site)
        r.html.render()
        soup = BeautifulSoup(r.html.html, 'html.parser')
        iframe = soup.find_all('iframe')[0]['src']
        r = requests.get(iframe)
        soup = BeautifulSoup(r.text, 'html.parser')
        token = soup.find(id='recaptcha-token')['value']
        self.data = {'age': random.choice(age_list),
                     'w': str(self.vote),
                     'consent': '1',
                     'g-recaptcha-response': token}
        print('[*] Das Programm startet jetzt')
        self.loop()

    def send(self):
        try:
            r = requests.post(self.url, data=self.data, headers=self.headers)
            if r.status_code == 200 and self.check in r.text:
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
            time.sleep(random.randint(5, 10))

if __name__ == '__main__':
    bot = Bot()