import base64
import json
import ast
from datetime import datetime
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

from stopping_utils import shutdown

script_dir = Path(__file__).resolve().parent
signed_key_path = Path("/ev-odoo/license/signed_key.json")
public_key_path = script_dir.parent / "resources/public_key.pem"
host_id_path = script_dir.parent / "resources/host_id"
saved_time_path = Path("/var/lib/odoo/saved_time")
LOG_TAG = ">> EXPERTS-VISION LICENSE >>"


def load_public_key():
    print(f"{LOG_TAG} Loading public key from {public_key_path} ...")
    try:
        with open(public_key_path, "rb") as f:
            return serialization.load_pem_public_key(f.read())
    except Exception as e:
        print(f"{LOG_TAG} Failed to load public key: {e}")
        shutdown()


def load_signed_key():
    print(f"{LOG_TAG} Loading signed key from {signed_key_path} ...")
    try:
        with open(signed_key_path, "r") as f:
            payload = json.load(f)
        data = base64.b64decode(payload["data"])
        signature = base64.b64decode(payload["signature"])
        return {"data": data, "signature": signature}
    except Exception as e:
        print(f"{LOG_TAG} Failed to load or decode signed key: {e}")
        shutdown()

def verify_license(data):
    data_dict = ast.literal_eval(data.decode('utf-8'))
    print(f"{LOG_TAG} License Data: {data_dict}")
    host_id = host_id_path.read_text().strip()
    current_date = datetime.now().strftime("%d-%m-%Y")
    print(f"{LOG_TAG} Actual host_id: {host_id}")
    print(f"{LOG_TAG} current_date: {current_date}")

    if host_id != data_dict["host_id"] or current_date > data_dict["expiry"]:
        shutdown()


def verify_current_time():
    now = datetime.now()
    if not saved_time_path.exists():
        saved_time_path.write_text(now.strftime("%Y-%m-%d %H:%M:%S"))
        print(f"First run: {saved_time_path.read_text().strip()}")
        return

    try:
        saved_time = datetime.strptime(saved_time_path.read_text().strip(), "%Y-%m-%d %H:%M:%S")
        if now < saved_time:
            print(f"{LOG_TAG} ❌ System time tampering detected !")
            shutdown()
    except Exception as e:
        print(f"{LOG_TAG} Error reading saved time: {e}")
        shutdown()

    saved_time_path.write_text(now.strftime("%Y-%m-%d %H:%M:%S"))


def verify_signature(public_key, data, signature):
    print(f"{LOG_TAG} Verifying signature ...")
    try:
        public_key.verify(signature, data, padding.PKCS1v15(), hashes.SHA512())
        verify_current_time()
        verify_license(data)
        print(f"{LOG_TAG} ✅ License is valid")
    except InvalidSignature:
        print(f"{LOG_TAG} ❌ License is invalid")
        shutdown()
