from bs4 import BeautifulSoup
import requests
import time
#for get respons
bb = 1
def get_respond(p_url):
    global bb
    count = 0
    xc=0
    while True:
        m = requests.get(p_url)
        if m.status_code == 200:
            print(f"{bb} page Loaded")
            bb+=1
            return m
        if count==20:
            count=0
            xc+=1
            print(f"page {bb} not responding")
            print("wait...")
            time.sleep(1)
        if xc== 2:
            bb+=1
            return None
        count+=1

#for getting description
def get_Description(html):
    x=[]
    div_html = html.find('div',{'class':'a-section a-spacing-medium a-spacing-top-small'})
    for i in div_html.find_all('li',{'class':'a-spacing-mini'}):
        x.append(i.text.strip())
    return x


# def find_menufacturer(html):
#     x = html.find_all('div',{'id':'detailBulletsReverseInterleaveContainer_feature_v2'})
#     for i in x:
#         pp=i.find('div',{'id':'detailBulletsWrapper_feature_div'})
#         gg = pp.find('div',{'id':'detailBullets_feature_div'}) if pp else None
#         y = gg.find('ul',{'class':'a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list'}) if pp else None
#         print(y)

#for main calling
def get_pd(p_url):
    r = get_respond(p_url)
    if r:
        p_html_text = r.text  
    else:
        return "Not responding"
    p_soup = BeautifulSoup(p_html_text, 'html.parser')
    discription = get_Description(p_soup)
    return discription
    
# output_csv = "final_data.csv"
import pandas as pd
# df = pd.read_csv('product_data.csv')
# df['Description'] = df['URL'].apply(get_pd)

# df.to_csv(output_csv, index=False)
# print("Data saved to", output_csv)

output_csv = 'final_data.csv'

df = pd.read_csv('product_data.csv')

# Create an empty DataFrame to store the processed data
df['Description'] = ''

for index, row in df.iterrows():
    description = get_pd(row['URL'])
    df.at[index, 'Description'] = description
    
    # Save DataFrame to CSV after each loop iteration
    df.to_csv(output_csv, index=False)
    print("Data saved after iteration", index)

