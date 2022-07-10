import settings
import json_list
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient

site_html = requests.get(settings.url)
bs4_html = BeautifulSoup(site_html.text, 'html.parser')
base_html = bs4_html.find_all("article", {"class": "product-miniature"})
items = len(bs4_html.find_all("article", {"class": "product-miniature"}))

client = MongoClient(settings.MongoDB_URL_main)[settings.MongoDB_DB_name]
db_products = client[settings.MongoDB_coll_products]
db_status = client[settings.MongoDB_coll_status]
db_archives = client[settings.MongoDB_coll_archives]

for i in range(0, items):
    # KS_products:
    p_id = base_html[i]['data-id-product']
    p_name = base_html[i].find("h2", {"class": "h3 product-title"}).text
    p_url = base_html[i].find("a")['href']
    p_category = base_html[i].find("div", {"class": "product-category-name text-muted"}).text
    try:
        p_brand = base_html[i].find("div", {"class": "product-brand text-muted"}).text
    except AttributeError:
        p_brand = ""
    p_reference = base_html[i].find("div", {"class": "product-reference text-muted"}).text

    # KS_status:
    p_timestamp = datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f')
    p_price = base_html[i].find("span", {"class": "product-price"})['content']
    p_price_old = ""
    p_availability = base_html[i].find("div", {"class": "product-availability d-block"}).text

    db_products.insert_one(
        json_list.product_main_data_def(
            p_id,
            p_name,
            p_url,
            p_category,
            p_brand,
            p_reference,
            p_status="current"
        )
    )

    db_status.insert_one(
        json_list.product_check_def(
            p_id,
            p_price,
            p_price_old,
            p_availability,
            p_timestamp,
            p_status="stable",
            p_checked=False
        )
    )

    db_archives.insert_one(
        json_list.product_archive_def(
            p_id,
            p_price,
            p_availability,
            p_timestamp
        )
    )

print("Ilość produktów: " + str(db_products.count_documents({})))
print("Ilość statusów: " + str(db_status.count_documents({})))
print("Ilość produktów w archiwum: " + str(db_archives.count_documents({})))
