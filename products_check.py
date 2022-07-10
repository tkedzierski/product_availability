import json_list
import settings
import report
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
db_report = client[settings.MongoDB_coll_report]

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
    p_availability = base_html[i].find("div", {"class": "product-availability d-block"}).text

    search_id_in_products = db_products.find_one({"product_id": int(p_id)}, {})
    search_id_in_status = db_status.find_one({"product_id": int(p_id)}, {})

    if search_id_in_products is not None:
        if search_id_in_status["product_price"] != str(p_price) or\
                search_id_in_status["product_availability"] != str(p_availability.strip()):
            if search_id_in_status["product_price"] != str(p_price):
                db_status.update_one({"product_id": int(p_id)}, {
                    "$set": {"product_price_old": str(search_id_in_status["product_price"]),
                             "product_price": str(p_price),
                             "product_status": "updated",
                             "product_checked": True}})

                db_archives.insert_one(
                    json_list.product_archive_def(
                        p_id, p_price, p_availability, p_timestamp
                    )
                )

                db_report.insert_one(
                    json_list.product_report_def(
                        p_id, p_status="price_change"
                    )
                )
            if search_id_in_status["product_availability"] != str(p_availability.strip()):
                db_status.update_one(
                    {"product_id": int(p_id)},
                    {"$set": {"product_availability": str(p_availability.strip()),
                              "product_status": "updated",
                              "product_checked": True}})

                db_archives.insert_one(
                    json_list.product_archive_def(
                        p_id, p_price, p_availability, p_timestamp
                    )
                )

                db_report.insert_one(
                    json_list.product_report_def(
                        p_id, p_status="avaiability_change"
                    )
                )
        else:
            db_status.update_one({"product_id": int(p_id)}, {"$set": {'product_checked': True}})
    else:
        db_products.insert_one(
            json_list.product_main_data_def(
                p_id, p_name, p_url, p_category, p_brand, p_reference, p_status="current"
            )
        )

        db_status.insert_one(
            json_list.product_check_def(
                p_id, p_price, p_availability, p_timestamp, p_status="new", p_checked=True
            )
        )

        db_archives.insert_one(
            json_list.product_archive_def(
                p_id, p_price, p_availability, p_timestamp
            )
        )

        db_report.insert_one(
            json_list.product_report_def(
                p_id, p_status="new"
            )
        )

for result in db_status.find({"product_checked": False}):
    if result["product_status"] != "deleted":
        result_p_id = result["product_id"]
        db_products.update_one({"product_id": int(result["product_id"])}, {"$set": {'product_status': "archived"}})
        db_status.update_one({"product_id": int(result["product_id"])},
                             {"$set": {'product_status': "deleted",
                                       'product_price': "0",
                                       'product_availability': "Produkt usunięty"}})
        db_archives.update_one({"product_id": int(result["product_id"])},
                               {"$set": {'product_price': "0",
                                         'product_availability': "Produkt usunięty"}})
        db_report.insert_one(
            json_list.product_report_def(
                result_p_id, p_status="deleted"
            )
        )

db_status.update_many({}, {"$set": {"product_checked": False}})

if db_report.count_documents({}) > 0:
    new_product_dict = {}
    deleted_product_dict = {}
    price_change_product_dict = {}
    availability_change_product_dict = {}

    for report_new_product in db_report.find({"product_status": "new"}):
        detailed = {
            "product_id": int(report_new_product["product_id"]),
            "product_name": db_products.find_one(
                {"product_id": int(report_new_product["product_id"])})["product_name"],
            "product_url": db_products.find_one(
                {"product_id": int(report_new_product["product_id"])})["product_url"],
            "product_price": db_status.find_one(
                {"product_id": int(report_new_product["product_id"])})["product_price"],
            "product_availability": db_status.find_one(
                {"product_id": int(report_new_product["product_id"])})["product_availability"]
        }
        new_product_dict[report_new_product["product_id"]] = detailed

    for report_deleted_product in db_report.find({"product_status": "deleted"}):
        detailed = {
            "product_id": int(report_deleted_product["product_id"]),
            "product_name": db_products.find_one(
                {"product_id": int(report_deleted_product["product_id"])})["product_name"],
            "product_url": db_products.find_one(
                {"product_id": int(report_deleted_product["product_id"])})["product_url"]
        }
        deleted_product_dict[report_deleted_product["product_id"]] = detailed

    for report_price_change_product in db_report.find({"product_status": "price_change"}):
        detailed = {
            "product_id": int(report_price_change_product["product_id"]),
            "product_name": db_products.find_one(
                {"product_id": int(report_price_change_product["product_id"])})["product_name"],
            "product_url": db_products.find_one(
                {"product_id": int(report_price_change_product["product_id"])})["product_url"],
            "product_price": db_status.find_one(
                {"product_id": int(report_price_change_product["product_id"])})["product_price"],
            "product_price_old": db_status.find_one(
                {"product_id": int(report_price_change_product["product_id"])})["product_price_old"],
            "product_availability": db_status.find_one(
                {"product_id": int(report_price_change_product["product_id"])})["product_availability"]
        }
        price_change_product_dict[report_price_change_product["product_id"]] = detailed

    for report_availability_change_product in db_report.find({"product_status": "avaiability_change"}):
        detailed = {
            "product_id": int(report_availability_change_product["product_id"]),
            "product_name": db_products.find_one(
                {"product_id": int(report_availability_change_product["product_id"])})["product_name"],
            "product_url": db_products.find_one(
                {"product_id": int(report_availability_change_product["product_id"])})["product_url"],
            "product_price": db_status.find_one(
                {"product_id": int(report_availability_change_product["product_id"])})["product_price"],
            "product_availability": db_status.find_one(
                {"product_id": int(report_availability_change_product["product_id"])})["product_availability"]
        }
        availability_change_product_dict[report_availability_change_product["product_id"]] = detailed

    email_title, email_main_report = report.prepare_email(
        new_product_dict,
        deleted_product_dict,
        price_change_product_dict,
        availability_change_product_dict
    )
    report.send_email(email_title, email_main_report)
    db_report.delete_many({})
else:
    print(str(datetime.now()) + " - brak zmiany")
exit()
