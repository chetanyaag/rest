from creators_api.api.default_api import DefaultApi
from creators_api.models.search_items_request import SearchItemsRequest

credential_id = ""
credential_secret = ""
version = "3.2"  # Assigned when you create credentials
partner_tag = "bestdeal0013-21"


def add_a_product():






    api_instance = DefaultApi(
        credential_id=credential_id,
        credential_secret=credential_secret,
        version=version,
        marketplace="www.amazon.in"
    )



def get_items(asin:):
    # Initialize API client with credential details
    api_client = ApiClient(
        credential_id=credential_id,
        credential_secret=credential_secret,
        version="3.2",
        # marketplace="www.amazon.in"
    )
    
    # Initialize API
    api = DefaultApi(api_client)

    """
    Add marketplace. For more details, refer: https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/common-request-headers-and-parameters#marketplace-locale-reference
    """
    marketplace = "www.amazon.in"
    
    """
    Choose resources you want from GetItemsResource enum
    For more details, refer: https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items#resources-parameter
    """
    resources = [
        'images.primary.medium',
        'itemInfo.title',
        'itemInfo.features',
        'offersV2.listings.price',
        'offersV2.listings.availability',
        'offersV2.listings.condition',
        'offersV2.listings.merchantInfo'
    ]
    
    # Create GetItems request
    get_items_request = GetItemsRequestContent(
        partner_tag=partner_tag,
        item_ids=['B0DLFMFBJW', 'B0BFC7WQ6R', 'B00ZV9RDKK'],
        resources=resources
    )
    
    try:
        # Call the GetItems API
        response = api.get_items(x_marketplace=marketplace, get_items_request_content=get_items_request)
        
        print('API called successfully.')
        print('Complete Response:\n', json.dumps(response.to_dict() if hasattr(response, 'to_dict') else str(response), indent=2))
        
    except ApiException as exception:
        print('Error calling Creators API!')
        print(exception)
    except Exception as exception:
        print('Unexpected error:', exception)
