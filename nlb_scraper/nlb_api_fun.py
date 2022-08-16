from zeep import Client, helpers
import pandas as pd

API = pd.read_csv("api.csv")['api'].values[0]
PRODUCTION_URL = "https://openweb.nlb.gov.sg/OWS/CatalogueService.svc?singleWsdl"
client = Client(wsdl=PRODUCTION_URL)


def return_needed_url(id_: str) -> str:
    return f"https://eservice.nlb.gov.sg/item_holding.aspx?id={id_}&type=bid&app=mylibrary"


def make_get_avail_api_call(bid_no: str, client=client, API=API):
    """ 
    Takes in book NLB BID number and
    returns GetAvailabilityInfo Obj
    """
    get_avail = {
        "APIKey": API,
        "BID": bid_no,
        "Modifiers" : {
            "SortSchema": None,
            "StartRecordPosition": 1,
            "MaximumRecords": 10,
            "SetId": None
        },
    }

    return client.service.GetAvailabilityInfo(**get_avail)


def df_get_avail_data(bid_no: str, avail_info_obj):
    
    return pd.DataFrame(
        helpers.serialize_object(avail_info_obj).get("Items").get("Item")
    ).sort_values("BranchName")


def make_get_title_details_api_call(bid_no: str, client=client, API=API):
    
    title_inputs = { "APIKey": API, "BID": bid_no }
    return client.service.GetTitleDetails(**title_inputs)


def df_get_title_data(title_detail_obj):
    
    return pd.DataFrame(
        helpers.serialize_object(title_detail_obj).get("TitleDetail"))


def final_book_avail_df(
    avail_df: pd.DataFrame, 
    title_df: pd.DataFrame
    ) -> pd.DataFrame:
    
    """ Combining book available data and title data """
    book_output = avail_df[['BranchName', 'CallNumber', 'StatusCode', 'StatusDesc', 'StatusDate', 'DueDate']]
    book_output['TitleName'] = title_df.TitleName.values[0]
    return book_output

