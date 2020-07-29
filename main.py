import requests
import random
import time
import sys
from bs4 import BeautifulSoup

class Bot():
    def __init__(self):
        print('[#] Programmiert von EIonTusk')
        print('[#] Github: https://github.com/EIonTusk')
        print('----------------------------------------------------------------------')
        print('[*] Gib dein Jugendwort des Jahres ein (s = Schabernack, m = Mittwoch)')
        self.name = input('>>> ')
        if self.name == '' or self.name == 's':
            self.name = 'Schabernack'
        elif self.name == 'm':
            self.name = 'Mittwoch'
        self.trys = 0
        self.success = 0
        self.url = "https://www.surveymonkey.com/r/7JZRVLJ?embedded=1"
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, 'html.parser')
        surveydata = soup.find(id='survey_data')['value']
        self.data = {'463803414': '3067519628',
                     '463803684': self.name,
                     '483089934[]': '3189794655',
                     'survey_data': surveydata,
                     'is_previous': 'false'
                     }
        print('[*] Das Programm startet jetzt')
        self.loop()
    def send(self):
        try:
            r = requests.post(self.url, data = self.data)
            if r.status_code == 200:
                self.success += 1
                sys.stdout.write('\r[+] Für %s abgestimmt                                                           \r\n' %self.name)
                sys.stdout.flush()
        except:
            sys.stdout.write('\r[!] Ein Fehler ist aufgetreten                                                      \r\n')
        self.trys += 1


    def loop(self):
        while True:
            self.send()
            sys.stdout.write('\rVersuche: %s, Erfolgreiche Versuche: %s, Fehlgeschlagene Versuche: %s' %(self.trys, self.success, self.trys - self.success))
            sys.stdout.flush()
            time.sleep(random.randint(10, 20))

if __name__ == '__main__':
    bot = Bot()