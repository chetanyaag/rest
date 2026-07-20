import logging
import os
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "creatorsapi-python-sdk"))

LOG_DIR = Path(__file__).resolve().parent / 'logs'
LOG_DIR.mkdir(exist_ok=True)
LOGGER = logging.getLogger('product_api_helper')
LOGGER.setLevel(logging.ERROR)
if not LOGGER.handlers:
    file_handler = logging.FileHandler(LOG_DIR / 'product_api.log')
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    LOGGER.addHandler(file_handler)

from creatorsapi_python_sdk.api.default_api import DefaultApi
from creatorsapi_python_sdk.api_client import ApiClient
from creatorsapi_python_sdk.exceptions import ApiException
from creatorsapi_python_sdk.models.get_items_request_content import GetItemsRequestContent


def load_env_value(key: str, default: str = "") -> str:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if line.startswith(f"{key}="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return os.getenv(key, default)


credential_id = load_env_value("CREDS_ID", "")
credential_secret = load_env_value("CREDS_SECRET", "")
version = "3.2"
partner_tag = load_env_value("PARTNER_TAG", "bestdeal0013-21")
resources = [
    "images.primary.large",
    "itemInfo.title",
    "itemInfo.contentInfo",
    "itemInfo.classifications",
    "itemInfo.features",
    "itemInfo.manufactureInfo",
    "itemInfo.productInfo",
    "itemInfo.technicalInfo",
    "offersV2.listings.isBuyBoxWinner",
    "offersV2.listings.merchantInfo",
    "offersV2.listings.price",
    "offersV2.listings.type",
    "offersV2.listings.availability",
    "offersV2.listings.condition",
    ]
marketplace = load_env_value("MARKETPLACE", "www.amazon.in")


def create_product_object(asin: str):
    return get_items(asin)


def get_items(asin: str):
    api_client = ApiClient(
        credential_id=credential_id,
        credential_secret=credential_secret,
        version=version,
    )


    api = DefaultApi(api_client)

    get_items_request = GetItemsRequestContent(
        partner_tag=partner_tag,
        item_ids=[asin],
        resources=resources,
    )

    try:
        response = api.get_items(
            x_marketplace=marketplace,
            get_items_request_content=get_items_request,
        )

        items_result = getattr(response, "items_result", None)
        items = getattr(items_result, "items", None) or []
        if not items:
            LOGGER.warning("No items found for ASIN: %s", asin)
            return None

        return items[0]
    except ApiException as exception:
        LOGGER.exception("Error calling Creators API for ASIN: %s", asin)
        return None
    except Exception as exception:
        LOGGER.exception("Unexpected error while fetching item for ASIN: %s", asin)
        return None


# if __name__ == "__main__":
#     get_items("B0DLFMFBJW")
