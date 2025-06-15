import time
import hashlib
import requests


CLICK_BASE = "https://api.click.uz/v2/merchant/"


def create_click_invoice(
    amount: int,
    phone: str,
    service_id,
    merchant_id,
    secret_key,
):
    timestamp = str(int(time.time()))
    digest = hashlib.sha1(f"{timestamp}{secret_key}".encode()).hexdigest()
    auth = f"{merchant_id}:{digest}:{timestamp}"
    headers = {
        "Auth": auth,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    data = {"service_id": service_id, "amount": amount, "phone_number": phone}
    return requests.post(
        CLICK_BASE + "invoice/create", json=data, headers=headers
    ).json()


def confirm_click_payment(
    payment_id: str,
    service_id,
    secret_key,
    merchant_id,
):
    timestamp = str(int(time.time()))
    digest = hashlib.sha1(f"{timestamp}{secret_key}".encode()).hexdigest()
    auth = f"{merchant_id}:{digest}:{timestamp}"
    url = f"{CLICK_BASE}payment/status_by_mti/:{service_id}/:{payment_id}"
    return requests.get(url, headers={"Auth": auth}).json()
