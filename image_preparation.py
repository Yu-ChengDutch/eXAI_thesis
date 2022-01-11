import requests
import pandas as pd

document = "fitzpatrick17k-amin-annotation.xlsx"
path = "C:/Users/zmezl/Desktop/University/AI/Thesis/eXAI_thesis/"

df = pd.read_excel(path + document)

url_list = df['url']
id_list = df['ID']

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.9"
           }

length = len(url_list)
length_string = str(length)

start = 8895

for i in range(start, length):
    
    print("Downloading " + id_list[i] + " of " + length_string)
    
    img_name = path + "Amin_dataset/" + id_list[i] + ".jpg"
    
    img_data = requests.get(url=url_list[i], headers=headers).content
    with open(img_name, 'wb') as handler:
        handler.write(img_data)