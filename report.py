def prepare_email(
        new_product_dict,
        deleted_product_dict,
        price_change_product_dict,
        availability_change_product_dict
        ):
    import settings
    new_line = '\n'
    new_line_x2 = '\n\n'
    email_main_report = ""
    email_title = settings.EmailReportTitle
    email_title_status = []
    if len(new_product_dict) > 0:
        email_main_report = str(email_main_report) + str("Nowe produkty: ") + str(new_line_x2)
        email_title_status.append("Nowe")
        for key, value in new_product_dict.items():
            product_name = value["product_name"]
            product_url = value["product_url"]
            product_price = "{:,.2f} zł".format(float(value["product_price"]))
            if value["product_availability"] == "":
                product_availability = "Produkt dostępny"
            else:
                product_availability = value["product_availability"]

            email_main_report = str(email_main_report) + \
                "Nazwa: " + str(product_name) + str(new_line) + \
                "Strona: " + str(product_url) + str(new_line) + \
                "Aktualna cena: " + str(product_price) + str(new_line) + \
                "Aktualna dostępność: " + str(product_availability) + str(new_line_x2)

    if len(deleted_product_dict) > 0:
        email_main_report = str(email_main_report) + str("Usunięte produkty: ") + str(new_line_x2)
        email_title_status.append("Usunięte")
        for key, value in deleted_product_dict.items():
            product_name = value["product_name"]
            product_url = value["product_url"]
            email_main_report = str(email_main_report) + \
                "Nazwa: " + str(product_name) + str(new_line) + \
                "Strona: " + str(product_url) + str(new_line) + str(new_line_x2)

    if len(price_change_product_dict) > 0:
        email_main_report = str(email_main_report) + str("Zmiana ceny: ") + str(new_line_x2)
        email_title_status.append("Cena")
        for key, value in price_change_product_dict.items():
            product_name = value["product_name"]
            product_url = value["product_url"]
            product_price = "{:,.2f} zł".format(float(value["product_price"]))
            product_price_old = "{:,.2f} zł".format(float(value["product_price_old"]))
            if value["product_availability"] == "":
                product_availability = "Produkt dostępny"
            else:
                product_availability = value["product_availability"]

            email_main_report = str(email_main_report) + \
                "Nazwa: " + str(product_name) + str(new_line) + \
                "Strona: " + str(product_url) + str(new_line) + \
                "Aktualna cena: " + str(product_price) + str(new_line) + \
                "Stara cena: " + str(product_price_old) + str(new_line) + \
                "Aktualna dostępność: " + str(product_availability) + str(new_line_x2)

    if len(availability_change_product_dict) > 0:
        email_main_report = str(email_main_report) + str("Zmiana dostępności: ") + str(new_line_x2)
        email_title_status.append("Dostępność")
        for key, value in availability_change_product_dict.items():
            product_name = value["product_name"]
            product_url = value["product_url"]
            product_price = "{:,.2f} zł".format(float(value["product_price"]))
            if value["product_availability"] == "":
                product_availability = "Produkt dostępny"
            else:
                product_availability = value["product_availability"]

            email_main_report = str(email_main_report) + \
                "Nazwa: " + str(product_name) + str(new_line) + \
                "Strona: " + str(product_url) + str(new_line) + \
                "Aktualna cena: " + str(product_price) + str(new_line) + \
                "Aktualna dostępność: " + str(product_availability) + str(new_line_x2)
    email_title = email_title + "/".join(email_title_status)
    print(email_title)
    print(email_main_report)
    return email_title, email_main_report


def send_email(email_title, email_main_report):
    import settings
    import smtplib
    from datetime import datetime
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    email = settings.EmailLogin
    password = settings.EmailPassword
    send_to_email = settings.EmailReportRecipient
    subject = email_title
    message = email_main_report

    msg = MIMEMultipart()
    msg["From"] = email
    msg["To"] = send_to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(message, 'plain'))
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        text = msg.as_string()
        server.sendmail(email, send_to_email, text)
        server.quit()
        print(str(datetime.now()) + " - raport wysłany")
    except:
        print(str(datetime.now()) + " - raport nie został wysłany")
