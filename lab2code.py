import requests
import pandas as pd
import matplotlib.pyplot as plt
import boto3
import json

urlusd = 'https://bank.gov.ua/NBU_Exchange/exchange'
urleur = 'https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode=€'

usd = requests.get(urlusd)
eu = requests.get(urleur)
dataus = usd.json()
dataeu = eu.json()

usd = []
eur = []

for i in dataus:
    usd.append({'exchangedate': i[ 'exchangedate'], 'rate_usd':i['rate']})
for i in dataeu:
    eur.append({'exchangedate': i[ 'exchangedate'], 'rate_eur':i['rate']})

usd_df = pd.DataFrame(usd).set_index('exchangedate')
eur_df = pd.DataFrame(eur).set_index('exchangedate')
data = pd.concat([usd_df, eur_df], axis=1)
data.to_csv('rates_uah_2021.csv')

s3 = boto3.client('s3')
s3.upload_file('rates_uah_2021.csv', 'nastyushkabucket', 'rates_uah_2021.csv')

s3.download_file('nastyushkabucket', 'rates_uah_2021.csv', 'rates_uah_2021.csv')
df = pd.read_csv('rates_uah_2021.csv')
df.plot(x='exchangedate', y=['rate_usd', 'rate_eur'], rot=45, title='rates 2021')
plt.savefig('gr.png')
s3.upload_file('gr.png', 'nastyushkabucket', 'gr.png')