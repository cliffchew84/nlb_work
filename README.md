## My Singapore National Library Board (NLB) Scraper
Hi all. This is my web scraper that extractions information from the Singapore NLB site, 
so as to allow me a better way to understand what books are availability in which libraries all over Singapore. 

This web scraper serves two main functions:
1. Gathers all the books that you have bookmarked in your NLB account.
2. Gathers all the physical books that you have borrowed from the NLB.
3. Both scripts will push the information as a DataFrame (table) into your selected Google Sheets. 

Some points to take note:
1. The **requirements.txt** will be provided.
2. You will need to include a "nlb_credentials.csv" file to log in into your account.
3. Set up to authenticate into Google Sheets will not be shared here. The script can be modified to save the information as a local csv file. 
4. As all scrapers, the code may break if the NLB website UI changes, and I may not have the time to ensure the full functionality of the scraper.
5. If anyone is planning to use this, please use it sparingly. I love the NLB 

For those interested, this is the attached Medium post (WIP) for this repo. 
