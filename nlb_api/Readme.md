### Exploration of NLB Open API

Hi, if you are reading this, it means that you are interested in using the Singapore NLB Open API using Python. 

*This documentation is updated as of 23th August, 2022.*

You should already have the API key from NLB before proceeding through this repo. If not, please go to [here](https://www.nlb.gov.sg/main/partner-us/contribute-and-create-with-us/NLBLabs) to request for the keys first, and come back when you get them. 
### References
These are my references:
1. [Official NLB API documentation](https://opendata.nlb.gov.sg/content/SkillsFuture/NLB_Labs_TechDoc-V3.6.pdf)
2. [Unofficial NLB API Python Github repo](https://github.com/yi-jiayu/nlbsg) from [Jiayu](https://blog.jiayu.co/) - Recommended by the NLB API documentation.

## Authenticate into the API
- Use the Python `zeep` package. The NLB API uses SOAP, and using `zeep` makes it easy for you to use a dictionary set up to provide inputs into the API.
- I saved my NLB API key as a csv file.

```python
API = pd.read_csv("api.csv")['api'].values[0]
PRODUCTION_URL = "https://openweb.nlb.gov.sg/OWS/CatalogueService.svc?singleWsdl"
client = Client(wsdl=PRODUCTION_URL)
```

# The API endpoints
- The official documentation gave 3 endpoints and their respective methods:
   1. Catalogue Service
      1. Search
      2. GetTitleDetails
      3. GetAvailabilityInfo
   2. Read Alike Service - **Don't bother with this. I was told by email this endpoint isn't working.**
   3. eResource Service
      1. Search
      2. GetAvailabilityInfo 

## Search 
- There are 3 input sections for the `Catalogue Search` method - (1) APIKey (2) SearchItems (3) Modifiers.
   1. `API key` - Your API key from NLB.
   2. The following input parameters for `SearchItems`, where you include them as a dictionary of `SearchField` and `SearchTerms`. You do not need to include all of these input parameters.
      1. Keywords
      2. Author
      3. Subject
      4. Title
      5. Branch
      6. Media_code
      7. Language
   3. `Modifiers`. They don't directly affect the results, but they modify how the results are shown. Their input parameters are:
      1. SortSchema - I didn't use this
      2. **StartRecordPosition** - If you have results that are more than the maximum number of records that can be returned, you need to use this parameter to indicate the position where you want to show your results. This is like some kind of pagination feature. 
      3. **MaximumRecords** - The documentation says that the maximum number of records is 100, but the most I could get was only 50.
      4. SetId - I couldn't figure this out either, and it didn't seem to affect my returned results.

Here is an example of the inputs for the Catalogue Search method. 

```python
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
```

- The respective output can be converted into an ordered dictionary using `helpers.serialize_object` from the `zeep` package. 

```python
    test_output = helpers.serialize_object(
        client.service.Search(**search_input)
)
```

- This is how the ordered dictionary will look like. **Note: To get the output below, use only the inputs {"SearchField": "Title", "SearchTerms": "Robust Python"}**

```python
OrderedDict([('Status', 'OK'),
             ('Message', 'Operation completed successfully'),
             ('ErrorMessage', None),
             ('TotalRecords', 2),
             ('NextRecordPosition', 0),
             ('SetId', '367795457'),
             ('Titles',
              OrderedDict([('Title',
                            [OrderedDict([('BID', '205485970'),
                                          ('ISBN',
                                           '9781098100636 (electronic bk)|9781098100612 (electronic bk)'),
                                          ('TitleName',
                                           'Robust python. Patrick Viafore.'),
                                          ('Author', 'Viafore, Patrick.'),
                                          ('PublishYear', '2021'),
                                          ('MediaCode', 'BK'),
                                          ('MediaDesc', 'Books')]),
                             OrderedDict([('BID', '205499632'),
                                          ('ISBN',
                                           '9781098100667 (paperback)|1098100662 (paperback)'),
                                          ('TitleName',
                                           'Robust Python : write clean and maintainable code / Patrick Viafore.'),
                                          ('Author', 'Viafore, Patrick,'),
                                          ('PublishYear', '2021'),
                                          ('MediaCode', 'BK'),
                                          ('MediaDesc', 'Books')])])]))])
```

## Get Title Details
- `GetTitleDetails` only takes in `APIKey`, and either `BID` or `ISBN`, which are two type of book identifiers.
- This endpoint is so simple because I would expect to only get 1 book returned to me.
- I was told it was better to use BID, as BID has less issues compared to ISBN. However, to my understanding, ISBN seems to be the international standard if you referencing your book information from other sources.
- Below is an example of the input parameters for the `GetTitleDetails` method.
  
```python
title_inputs = {
    "APIKey": API,
    "BID": 204485571,
}
```

- And this is how the output looks like. 

```python
{
    'Status': 'OK',
    'Message': 'Operation completed successfully',
    'ErrorMessage': None,
    'TitleDetail': {
        'BID': '204485571',
        'TitleName': '40 algorithms every programmer should know : hone your problem-solving skills by learning different algorithms and their implementation in Python / Imran Ahmad.',
        'Author': 'Ahmad, Imran,',
        'OtherAuthors': None,
        'Publisher': None,
        'PhysicalDesc': 'x, 365 pages :illustrations ;24 cm',
        'Subjects': {
            'Subject': [
                'Computer programs',
                'Python (Computer program language)'
            ]
        },
        'Summary': None,
        'Notes': '\r\nIncludes index.',
        'ISBN': '1789801214 (paperback)|9781789801217 (paperback)',
        'ISSN': None,
        'NTitleName': None,
        'NAuthor': None,
        'NPublisher': None
    }
}
```

# GetAvailabilityInfo
Lastly, the `GetAvailabilityInfo` takes in `APIKey` and `BID` or `ISBN`, just like `GetTitleDetail`. There is also the `Modifiers` section, as the data returned from this endpoint is a dictionary of libraries that houses the particular book. 

```python
isbn = 9781492057697
get_avail = {
    "APIKey": API,
    "ISBN": isbn,
    "Modifiers" : {
        "SortSchema": None,
        "StartRecordPosition": 1,
        "MaximumRecords": 100,
        "SetId": None
    },
}
avail_info = client.service.GetAvailabilityInfo(**get_avail)
```

- And this is the long output of available books.

```python
{
    'Status': 'OK',
    'Message': 'Operation completed successfully',
    'ErrorMessage': None,
    'NextRecordPosition': 0,
    'SetId': '369196980',
    'Items': {
        'Item': [
            {
                'ItemNo': 'B36549693A',
                'BranchID': 'QUPL',
                'BranchName': 'Queenstown Public Library',
                'LocationCode': '____',
                'LocationDesc': 'Adult Lending',
                'CallNumber': 'English 005.133 GIF -[COM]',
                'StatusCode': 'S',
                'StatusDesc': 'Not on Loan',
                'MediaCode': 'BOOK',
                'MediaDesc': 'Book',
                'StatusDate': '07/06/2022',
                'DueDate': None,
                'ClusterName': None,
                'CategoryName': None,
                'CollectionCode': 'GGEN',
                'CollectionMinAgeLimit': None
            },
            {
                'ItemNo': 'B36549692K',
                'BranchID': 'TRL',
                'BranchName': 'Tampines Regional Library',
                'LocationCode': '____',
                'LocationDesc': 'Adult Lending',
                'CallNumber': 'English 005.133 GIF -[COM]',
                'StatusCode': 'C',
                'StatusDesc': 'On Loan',
                'MediaCode': 'BOOK',
                'MediaDesc': 'Book',
                'StatusDate': '15/08/2022',
                'DueDate': '24/09/2022',
                'ClusterName': None,
                'CategoryName': None,
                'CollectionCode': 'GGEN',
                'CollectionMinAgeLimit': None
            },
            {
                'ItemNo': 'B36549691J',
                'BranchID': 'WRL',
                'BranchName': 'Woodlands Regional Library',
                'LocationCode': '____',
                'LocationDesc': 'Adult Lending',
                'CallNumber': 'English 005.133 GIF -[COM]',
                'StatusCode': 'S',
                'StatusDesc': 'Not on Loan',
                'MediaCode': 'BOOK',
                'MediaDesc': 'Book',
                'StatusDate': '21/08/2022',
                'DueDate': None,
                'ClusterName': None,
                'CategoryName': None,
                'CollectionCode': 'GGEN',
                'CollectionMinAgeLimit': None
            },
            {
                'ItemNo': 'B36549690I',
                'BranchID': 'JRL',
                'BranchName': 'Jurong Regional Library',
                'LocationCode': '____',
                'LocationDesc': 'Adult Lending',
                'CallNumber': 'English 005.133 GIF -[COM]',
                'StatusCode': 'C',
                'StatusDesc': 'On Loan',
                'MediaCode': 'BOOK',
                'MediaDesc': 'Book',
                'StatusDate': '19/08/2022',
                'DueDate': '30/09/2022',
                'ClusterName': None,
                'CategoryName': None,
                'CollectionCode': 'GGEN',
                'CollectionMinAgeLimit': None
            },
            {
                'ItemNo': 'B36549689F',
                'BranchID': 'BIPL',
                'BranchName': 'Bishan Public Library',
                'LocationCode': '____',
                'LocationDesc': 'Adult Lending',
                'CallNumber': 'English 005.133 GIF -[COM]',
                'StatusCode': 'S',
                'StatusDesc': 'Not on Loan',
                'MediaCode': 'BOOK',
                'MediaDesc': 'Book',
                'StatusDate': '18/08/2022',
                'DueDate': None,
                'ClusterName': None,
                'CategoryName': None,
                'CollectionCode': 'GGEN',
                'CollectionMinAgeLimit': None
            },
            {
                'ItemNo': 'B36549687D',
                'BranchID': 'BEPL',
                'BranchName': 'Bedok Public Library',
                'LocationCode': '____',
                'LocationDesc': 'Adult Lending',
                'CallNumber': 'English 005.133 GIF -[COM]',
                'StatusCode': 'S',
                'StatusDesc': 'Not on Loan',
                'MediaCode': 'BOOK',
                'MediaDesc': 'Book',
                'StatusDate': '21/08/2022',
                'DueDate': None,
                'ClusterName': None,
                'CategoryName': None,
                'CollectionCode': 'GGEN',
                'CollectionMinAgeLimit': None
            },
            {
                'ItemNo': 'B36534717C',
                'BranchID': 'WDALLI',
                'BranchName': 'The LLiBrary (Lifelong Learning Institute)',
                'LocationCode': '____',
                'LocationDesc': 'Adult Lending',
                'CallNumber': 'English 005.133 GIF -[COM]',
                'StatusCode': 'C',
                'StatusDesc': 'On Loan',
                'MediaCode': 'BOOK',
                'MediaDesc': 'Book',
                'StatusDate': '10/08/2022',
                'DueDate': '03/09/2022',
                'ClusterName': 'Computer & IT',
                'CategoryName': None,
                'CollectionCode': 'GGEN',
                'CollectionMinAgeLimit': None
            },
            {
                'ItemNo': 'B36596333E',
                'BranchID': 'GEPL',
                'BranchName': 'Geylang East Public Library',
                'LocationCode': '____',
                'LocationDesc': 'Adult Lending',
                'CallNumber': 'English 005.133 GIF -[COM]',
                'StatusCode': 'C',
                'StatusDesc': 'On Loan',
                'MediaCode': 'BOOK',
                'MediaDesc': 'Book',
                'StatusDate': '30/07/2022',
                'DueDate': '22/08/2022',
                'ClusterName': None,
                'CategoryName': None,
                'CollectionCode': 'GGEN',
                'CollectionMinAgeLimit': None
            },
            {
                'ItemNo': 'B36596332D',
                'BranchID': 'AMKPL',
                'BranchName': 'Ang Mo Kio Public Library',
                'LocationCode': '____',
                'LocationDesc': 'Adult Lending',
                'CallNumber': 'English 005.133 GIF -[COM]',
                'StatusCode': 'S',
                'StatusDesc': 'Not on Loan',
                'MediaCode': 'BOOK',
                'MediaDesc': 'Book',
                'StatusDate': '15/08/2022',
                'DueDate': None,
                'ClusterName': None,
                'CategoryName': None,
                'CollectionCode': 'GGEN',
                'CollectionMinAgeLimit': None
            },
            {
                'ItemNo': 'B36596331C',
                'BranchID': 'TPPL',
                'BranchName': 'Toa Payoh Public Library',
                'LocationCode': '____',
                'LocationDesc': 'Adult Lending',
                'CallNumber': 'English 005.133 GIF -[COM]',
                'StatusCode': 'I',
                'StatusDesc': 'In-Transit',
                'MediaCode': 'BOOK',
                'MediaDesc': 'Book',
                'StatusDate': '21/08/2022',
                'DueDate': None,
                'ClusterName': None,
                'CategoryName': None,
                'CollectionCode': 'GGEN',
                'CollectionMinAgeLimit': None
            },
            {
                'ItemNo': 'B36596330B',
                'BranchID': 'JWPL',
                'BranchName': 'Jurong West Public Library',
                'LocationCode': '____',
                'LocationDesc': 'Adult Lending',
                'CallNumber': 'English 005.133 GIF -[COM]',
                'StatusCode': 'S',
                'StatusDesc': 'Not on Loan',
                'MediaCode': 'BOOK',
                'MediaDesc': 'Book',
                'StatusDate': '02/08/2022',
                'DueDate': None,
                'ClusterName': None,
                'CategoryName': None,
                'CollectionCode': 'GGEN',
                'CollectionMinAgeLimit': None
            }
        ]
    }
}
```

- To make it easier to manage the data, I wrote some simple code to take out the sections that I want.

```python
df = pd.DataFrame()
for i in pd.DataFrame(helpers.serialize_object(avail_info).get("Items").values()).T[0]:
    df = df.append(pd.DataFrame.from_dict(i, orient='index').T)
# Change this to bid if you use bid instead
df['isbn'] = isbn
```

## eResources
- I am not sure why, but this endpoint isn't covered by Jiayu's repo.
- I realised the `eResource Search` endpoints follow roughly the same structure as the `Catalogue Search` endpoint. This is an example of using `eResource`, but it does have some eResource specific inputs. However, rather than repeat what is written in the documentation, search for `1.3.2.1 EresourceService.Search` to look at the parameters needed.
- However, some things to note:
  - For DataFrom:
    - eBooks + Audio Books = Digital Books
    - The other DataFrom parameters don't return anything useful to me.
  - For ContentType:
    - Overdrive was the most useful one to me.
- Here is an example of an API call made to `eResource Search`.

```python
PRODUCTION_URL = "https://openweb.nlb.gov.sg/OWS/EresourceService.svc?wsdl"
client = Client(wsdl=PRODUCTION_URL)

ebook_search = {
    "APIKey": API,
    "SearchItems": {
        "SearchItem": [
            {
                "SearchField": "Title", 
                "SearchTerms": "Python"
            }
        ]
    },
    "ContentType": 'eBooks',
    "DataFrom": "Overdrive",
    "Modifiers": {
        "SortSchema": None,
        "StartRecordPosition": 1,
        "MaximumRecords": 1
    }
}

ebook_search_output = client.service.Search(**ebook_search)
ebook_search_output
```

- And the output looks like this

```python
{
    'Status': 'OK',
    'Message': 'Operation completed successfully',
    'ErrorMessage': None,
    'TotalRecords': 301,
    'NextRecordPosition': 2,
    'Results': {
        'Result': [
            {
                'ID': '2E8E924E-0F28-4E37-BB2A-565E7ADE3F1E',
                'Types': {
                    'Value': [
                        'Electronic Book'
                    ]
                },
                'Title': 'Programming microcontrollers with python [electronic resource] : Experience the power of embedded python. Armstrong Subero. ',
                'Author': 'Subero, Armstrong.',
                'Abstracts': {
                    'Value': [
                        "For the first time microcontrollers are powerful enough to be programmed in Python. The landscape of embedded systems development is changing, microcontrollers are becoming more powerful, and the rise of the internet of things is leading more developers to get into hardware. This book provides the solid foundation to start your journey of embedded systems development and microcontroller programming with Python.\xa0   You'll quickly realize the value of using Python. The theme of the book is simplicity and the cleanness and elegance of Python makes that possible. Featuring a step-by-step approach, this single source guide balances complexity and clarity with insightful explanations that you'll easily grasp.\xa0   Python is quickly becoming the language of choice for applications such as machine learning and computer vision on embedded devices. What would previously be daunting and exceedingly difficult to do in C or C++ is now possible with Python because of its level of abstraction.  Programming Microcontrollers with Python  is your path to bringing your existing skills to the embedded space.\xa0\xa0    What You'll Learn      Review microcontroller basics and the hardware and software requirements\xa0  Understand an embedded system's general architecture  Follow the steps needed to carry a product to market\xa0  Take a crash course in Python programming   Program a microcontroller  Interface with a microcontroller using LCD and Circuit Python  Use and control sensors      Who This Book Is For     Those getting started with microcontrollers, those new to C, C++, and Arduino programming, web developers looking to get into IoT, or Python programmers who wish to control hardware devices. "
                    ]
                },
                'Languages': {
                    'Value': [
                        'eng'
                    ]
                },
                'CreationDate': '01/01/2021 00:00:00',
                'DataFrom': 'Overdrive',
                'Url': 'https://search.nlb.gov.sg/onesearch/r/overdrive/?r=f1gmT0iyh7rMQ7vh91tmu3Rmoi1q05yhZ+Jg9Q5G/ptz8zfBexMGdVA7eqB1UVivMX2kvFgK6p/vB/0aeJfcHJK2lcBxrdpDdM63dgW/CYPGiPCV7cvpb/v9VIq8QtB+7YLbmu8FgQ9SxebGxeVpc05nJlIAiZ6M9MH5zblDB77BjdjwV+osn39sX6x39ix2UAYgSIDov6xxBrdrorl8F7kUmi2BCujkDn1ynRvJ+Iw=',
                'ResourceUrlExt': 'http://singapore.lib.overdrive.com/ContentDetails.htm?ID=2E8E924E-0F28-4E37-BB2A-565E7ADE3F1E',
                'CoverUrl': 'https://img1.od-cdn.com/ImageType-100/7614-1/%7B2E8E924E-0F28-4E37-BB2A-565E7ADE3F1E%7DImg100.jpg',
                'Subjects': 'Nonfiction,Computer Technology',
                'ISBN': '9781484270585 (electronic bk)'
            }
        ]
    }
}
```