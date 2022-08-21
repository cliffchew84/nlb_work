import pandas as pd
from datetime import datetime
from zeep import Client, helpers

# Authenticating into the NLB API
API = pd.read_csv("api.csv")['api'].values[0]
PRODUCTION_URL = "https://openweb.nlb.gov.sg/OWS/CatalogueService.svc?singleWsdl"
client = Client(wsdl=PRODUCTION_URL)

# Setting up parameter inputs for Search
search_input = {
    "APIKey": API,
    "SearchItems": {
        "SearchItem": [
            {
                "SearchField": "Title", 
                "SearchTerms": "Robust Python"
            },
            {
                "SearchField": "Keywords", 
                "SearchTerms": "Python"
            },
            {
                "SearchField": "Author", 
                "SearchTerms": "XXX"
            },
            {
                "SearchField": "Subject",
                "SearchTerms": "XXX"
            },
            {
                "SearchField": "BranchID",
                "SearchTerms": "XXX"
            },
            {
                "SearchField": "MediaCode",
                "SearchTerms": "XXX"
            },
            {
                "SearchField": "Language",
                "SearchTerms": "XXX"
            }
        ]
    },
    "Modifiers": {
        "SortSchema": None,
        "StartRecordPosition": 1,
        "MaximumRecords": 100,
        "SetId": None
    }
}

# Use helpers.serial_object() to transfer zeep output into JSON
test_output = helpers.serialize_object(
    client.service.Search(**search_input)
)

## Available Titles
# bid_no = 205431306
isbn = 9781492057697

get_avail = {
    "APIKey": API,
    "ISBN": isbn,
    # "BID": bid_no,
    "Modifiers" : {
        "SortSchema": None,
        "StartRecordPosition": 1,
        "MaximumRecords": 100,
        "SetId": None
    },
}

avail_info = client.service.GetAvailabilityInfo(**get_avail)

# Converts zeep object into JSON, and then into dataframe
df = pd.DataFrame()
for i in pd.DataFrame(helpers.serialize_object(avail_info).get("Items").values()).T[0]:
    df = df.append(pd.DataFrame.from_dict(i, orient='index').T)
df['bid'] = bid_no
df.sort_values("BranchName")[["BranchName", "StatusDesc", "DueDate"]]