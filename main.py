from bs4 import BeautifulSoup
import requests
import lxml
import smtplib
import mycredentials

MY_EMAIL = mycredentials.MY_EMAIL
RECEIVER = mycredentials.RECEIVER
PASSWORD = mycredentials.PASSWORD
BUY_PRICE = 600

url = "https://www.amazon.ca/LG-UltraFine-27UN850-W-DisplayHDR-Connectivity/dp/B08CVTTNN4/ref=sr_1_1?crid=MI2XKE9DHN5V&keywords=lg+ultrafine+uhd+27-inch+4k+uhd+2160p+computer+monitor+27un850-w&qid=1704677411&sprefix=LG+UltraFine+UHD+27-Inch+4K+UHD+2160p+Computer+%2Caps%2C100&sr=8-1"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}


# Get the content of the amazon product page and retrieve price and title of the product
response = requests.get(url=url, headers=header)
soup = BeautifulSoup(response.content, "lxml")
title = soup.find(id="productTitle").getText().strip()
# print(title)
# print(soup.text)
price_text = soup.find(class_="a-offscreen").getText()
no_currency_price = price_text.split("$")[1]
price = float(no_currency_price)

# Send Email Alert if the price drops below buy price
if price < BUY_PRICE:
    message = f"{title} is now {price}"
    # Note:
    # `Gmail: smtp.gmail.com
    # Hotmail: smtp.live.com
    # Outlook: outlook.office365.com
    # Yahoo: smtp.mail.yahoo.com
    # If you use another email provider, just Google for your email provider e.g. "Gmail SMTP address"
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=RECEIVER,
            msg=f"Subject:Amazon Price Change Alert!\n\n{message}."
        )
