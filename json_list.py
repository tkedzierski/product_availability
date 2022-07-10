def product_main_data_def(p_id, p_name, p_url, p_category, p_brand, p_reference, p_status):
    product_main_data = {
        "product_id": int(p_id),
        "product_name": str(p_name.strip()),
        "product_url": str(p_url.strip()),
        "product_category": str(p_category.strip()),
        "product_brand": str(p_brand.strip()),
        "product_reference": str(p_reference.strip()),
        "product_status": str(p_status)  # current/archive
    }
    return product_main_data


def product_check_def(p_id, p_price, p_price_old, p_availability, p_timestamp, p_status, p_checked):
    product_check = {
        "product_id": int(p_id),
        "product_price": str(p_price),
        "product_price_old": str(p_price_old),
        "product_availability": str(p_availability.strip()),
        "product_timestamp": str(p_timestamp),
        "product_status": p_status,  # stable/update/deleted/new
        "product_checked": p_checked  # True/False
    }
    return product_check


def product_archive_def(p_id, p_price, p_availability, p_timestamp):
    product_archive = {
        "product_id": int(p_id),
        "product_price": str(p_price),
        "product_availability": str(p_availability.strip()),
        "product_timestamp": str(p_timestamp)
    }
    return product_archive


def product_report_def(result_p_id, p_status):
    product_report = {
        "product_id": int(result_p_id),
        "product_status": p_status      # new/deleted/price_change/avaiability_change
    }
    return product_report
