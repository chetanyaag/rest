import json
import os
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "creatorsapi-python-sdk"))

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

        print("API called successfully.")
        print(
            "Complete Response:\n",
            json.dumps(
                response.to_dict() if hasattr(response, "to_dict") else str(response),
                indent=2,
            ),
        )
        return response.items_result.items[0]
    except ApiException as exception:
        print("Error calling Creators API!")
        print(exception)
    except Exception as exception:
        print("Unexpected error:", exception)


if __name__ == "__main__":
    get_items("B0DLFMFBJW")
