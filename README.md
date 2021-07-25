## My Singapore National Library Board (NLB) Scraper
Hi all. This is my web scraper that extracts information from the Singapore NLB site, 
so as to allow me a better way to understand what books are availability in which libraries all over Singapore. 
I have written my code in Jupyter Notebooks as I felt it was easier to interact and wrangle with my data. 

This web scraper serves two main functions:
1. Gathers all the books that you have bookmarked in your NLB account (Books_Borrowed.ipynb).
2. Gathers all the physical books that you have borrowed from the NLB (Books_in_Bookmarks.ipynb).
3. Both scripts will push the information as a DataFrame (table) into your selected Google Sheets.

Some points to take note:
1. As per best practice, credentials are placed in a separate folder and not commited into this repo.
2. My **NLB credentials** are saved as "nlb_credentials.csv". I used the os.environ method, and saved the pathname to my NLB credentials into **cred_folder**.
3. Set up to authenticate into Google Sheets will not be shared here. The script can be modified to save the information as a local csv file. 
4. As all scrapers, the code may break if the NLB website UI changes, and I may not have the time to ensure the full functionality of the scraper.
5. If anyone is planning to use this, please use it sparingly. I love the NLB, so don't abuse this code.

For those interested, this is the attached [Medium post](https://cliffy-gardens.medium.com/f74c541f1f94) for this repo. 
