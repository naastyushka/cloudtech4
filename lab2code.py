import requests
import pandas as pd
import boto3
import matplotlib.pyplot as plt

url_usd = "https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode=usd&sort=exchangedate&order=desc&json"
url_eur = "https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode=eur&sort=exchangedate&order=desc&json"

response_usd = requests.get(url_usd)
response_eur = requests.get(url_eur)

data_usd = response_usd.json()
data_eur = response_eur.json()

usd = []
eur = []

for i in data_usd:
    usd.append({"exchangedate": i["exchangedate"], "rate_usd": i["rate"]})

for i in data_eur:
    eur.append({"exchangedate": i["exchangedate"], "rate_eur": i["rate"]})

df1 = pd.DataFrame(usd).set_index("exchangedate")
df2 = pd.DataFrame(eur).set_index("exchangedate")

general_data = pd.concat([df1, df2], axis=1)
general_data.to_csv("exchange_rates_uah_2021.csv")

s3 = boto3.client("s3")

s3.upload_file(
    "exchange_rates_uah_2021.csv", "nastyushkabucket", "exchange_rates_uah_2021.csv"
)

s3.download_file(
    "nastyushkabucket", "exchange_rates_uah_2021.csv", "exchange_rates_uah_2021.csv"
)

df = pd.read_csv("exchange_rates_uah_2021.csv")

df.plot(
    x="exchangedate", y=["rate_usd", "rate_eur"], rot=45, title="UAH exchange graph"
)
plt.savefig("UAH_graph.png")

s3.upload_file("UAH_graph.png", "nastyushkabucket", "UAH_graph.png")