from fastapi import FastAPI
# from typing import Optional
import pandas as pd
from datetime import date
# import PyCurrency_Converter
from currency_converter import CurrencyConverter
from random import choice, randint
# import re
import requests
# from mangum import Mangum
# from flask_cors import CORS
import uvicorn

app = FastAPI()
# handler = Mangum(app)
# CORS(app)  # This enables CORS for all routes and origins

# origins = ["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

data = pd.read_csv('main_carbon_data.csv')
country_df = pd.read_csv('countries.csv')
iso_df = pd.read_csv('country-code-to-currency-code-mapping.csv')


country = {}
iso = {}
c = CurrencyConverter()


for i in range(len(country_df)):
    country[f'{country_df.iloc[i,1]}'] = country_df.iloc[i,0]
    
for i in range(len(iso_df)):
    iso[f'{iso_df.iloc[i,1]}'] = iso_df.iloc[i,3]



URL = 'https://raw.githubusercontent.com/AnotherKamila/currency-exchange-rates/master/rates.csv'
cc = CurrencyConverter(URL, ref_currency='USD')

def calculate_carbon(country_code, amount, df, country, iso, mcc):
    euro_amount = cc.convert(amount, iso[country[country_code]], 'EUR', date=date(2018, 1, 20))
    row = pd.DataFrame(df[df['MCC Code']==mcc])[country_code]
    print(euro_amount, row)
    return euro_amount * row.to_list()[0]


# Assuming your lists c_shortened and mcc are defined in this script or imported
c_shortened = [
"United States", "China", "India", "United Kingdom", "France", "Germany", "Japan", "Brazil", "Italy", "Canada", "Russia", "Australia", "Spain", "Mexico", "South Korea", "Indonesia", "Turkey", "Saudi Arabia", "Switzerland", "Netherlands", "Sweden", "United Arab Emirates", "Singapore", "Egypt", "South Africa", "Thailand", "Argentina", "Malaysia", "Nigeria", "Poland"
    # Add the rest of the countries here
]

mcc = [
"742", "763", "780", "1520", "1711", "1731", "1740", "1750", "1761", "1771", "1799", "2741", "2791", "2842", "4011", "4111", "4112", "4119", "4121", "4131", "4214", "4215", "4225", "4411", "4468", "4511", "4582", "4722", "4723", "4784", "4789", "4812", "4813", "4814", "4816", "4821", "4829", "4899", "4900", "5013", "5021", "5039", "5044", "5045", "5046", "5047"
    # "5051", "5065", "5072", "5074", "5085", "5094", "5099", "5111", "5122", "5131", "5137", "5139", "5169", "5172", "5192", "5193", "5198", "5199", "5200", "5211", "5231", "5251", "5261", "5262", "5271", "5300", "5309", "5310", "5311", "5331", "5399", "5411", "5422", "5441", "5451", "5462", "5499", "5511", "5521", "5531", "5532", "5533", "5541", "5542", "5551", "5552", "5561", "5571", "5592", "5598", "5599", "5611", "5621", "5631", "5641", "5651", "5655", "5661", "5681", "5691", "5697", "5698", "5699", "5712", "5713", "5714", "5718", "5719", "5722", "5732", "5733", "5734", "5735", "5811", "5812", "5813", "5814", "5815", "5816", "5817", "5818", "5912", "5921", "5931", "5932", "5933", "5935", "5937", "5940", "5941", "5942", "5943", "5944", "5945", "5946", "5947", "5948", "5949", "5950", "5960", "5962", "5963", "5964", "5965", "5966", "5967", "5968", "5969", "5970", "5971", "5972", "5973", "5975", "5976", "5977", "5978", "5983", "5992", "5993", "5994", "5995", "5996", "5997", "5998", "5999", "6010", "6011", "6012", "6050", "6051", "6211", "6300", "6513", "6532", "6533", "6536", "6537", "6538", "6540", "7011", "7012", "7032", "7033", "7210", "7211", "7216", "7217", "7221", "7230", "7251", "7261", "7273", "7276", "7277", "7278", "7296", "7297", "7298", "7299", "7311", "7321", "7322", "7333", "7338", "7339", "7342", "7349", "7361", "7372", "7375", "7379", "7392", "7393", "7394", "7395", "7399", "7512", "7513", "7523", "7531", "7534", "7535", "7538", "7542", "7549", "7622", "7623", "7629", "7631", "7641", "7692", "7699", "7800", "7801", "7802", "7829", "7832", "7841", "7911", "7922", "7929", "7932", "7933", "7941", "7991", "7992", "7993", "7994", "7995", "7996", "7997", "7998", "7999", "8011", "8021", "8031", "8041", "8042", "8043", "8049", "8050", "8062", "8071", "8099", "8111", "8211", "8220", "8241", "8244", "8249", "8299", "8351", "8398", "8641", "8651", "8661", "8675", "8699", "8734"
    # Add the rest of the MCC values here
]



@app.get("/random-data/{n}")
async def get_random_data(n:int):
    l = [] 
    for i in range(n):
        random_country = choice(c_shortened)
        random_mcc = choice(mcc)
        random_amount = randint(1, 100)
        l.append({"country": random_country, "MCC": random_mcc, "amount": random_amount})
    return l

@app.get("/")
async def root():
    return {"message": "Hello there"}


@app.get("/blogs/all")
async def get_all_blogs():
    return {"message": "all blogs "}


@app.get("/type/{country_code}")
async def get_blogs(country_code='Andorra', amount=10, mcc=780):
    return {calculate_carbon(country_code, amount, data, country, iso, mcc)}




@app.get("/image-search/{name}")
async def get_random_data(name:str):
    query = name

    r = requests.get("https://api.qwant.com/v3/search/images",
        params={
            'count': 5,
            'q': query,
            't': 'images',
            'safesearch': 1,
            'locale': 'en_US',
            'offset': 0,
            'device': 'desktop'
        },
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
    )

    response = r.json().get('data').get('result').get('items')
    urls = [r.get('media') for r in response][0]


#     return urls

# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port=8089)