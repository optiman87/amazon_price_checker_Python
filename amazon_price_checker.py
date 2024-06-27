# Define a function that checks the price of the first 10 products from an Amazon search result for 'Amazon Fire TV'

def amazon_price_checker():
    # Define URL and header
    url='https://www.amazon.ca/s?k=amazon+fire+tv&ref=nb_sb_noss'
    header= { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
    "Accept-Encoding": "gzip, deflate, br, zstd", 
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8", 
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36", 
    "X-Amzn-Trace-Id": "Root=1-6679a18f-21bfa3de425573336f51407a"}
  
    # Use requests to get response with the URL and header
    page= requests.get(url, headers= header)
  
    # Convert response to html format
    soup= BeautifulSoup(page.text, 'html')
    soup2= BeautifulSoup(soup.prettify(), 'html')
  
    # Retrieve the first 10 products and their prices (and decimal)
    title =soup2.find_all('span',class_='a-size-base-plus a-color-base a-text-normal')[:10]
    price =soup2.find_all('span',class_='a-price-whole')[:10]
    pricedecimal=soup2.find_all('span',class_='a-price-fraction')[:10]
  
    # Strip all unnecessary characters from the products and prices
    title2=[i.text.strip() for i in title]
    price2=[i.text.strip() for i in price]
    price2=[i.rstrip('r\n. ')+'.' for i in price2]
    pricedecimal2= [i.text.strip() for i in pricedecimal]
  
    # Concatenate the whole number with decimal number in each price
    pricelist= [a+b for a,b in zip(price2,pricedecimal2)]
  
    # Create a new dataframe to store the items and prices
    df= pd.DataFrame({'Product Name':title2,'Price':pricelist})
  
    # Add timestamp to the dataframe
    df['Timestamp']= pd.to_datetime('now')

    # Store the dataframa as a csv file, if the csv file exists, the dataframe will be appended to the existing csv file.
    if not os.path.isfile('/Users/ek/Desktop/PythonPortfolio/price_extract.csv'):
        df.to_csv('/Users/ek/Desktop/PythonPortfolio/price_extract.csv', header='column_names')
    else:
        df.to_csv('/Users/ek/Desktop/PythonPortfolio/price_extract.csv', mode='a',header=None)

# Schedule timer to run the Amazon Price Checker every minute (60s).
while True:
    amazon_price_checker()
    print('Amazon Price Checker run successfully!')
    time.sleep(60)
