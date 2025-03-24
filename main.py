# main.py
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

def fetch_listings():
    url = "https://www.sreality.cz/hledani/prodej/byty?region=ostrava-mesto,vsetin&velikost=2%2B1,3%2B1&cena-max=2100000"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    listings = soup.find_all("div", class_="property")
    results = []
    for listing in listings:
        title = listing.find("span", class_="name").text.strip()
        link = listing.find("a")["href"]
        results.append((title, "https://www.sreality.cz" + link))
    return results

def send_email(new_listings):
    msg_body = "\n".join([f"{title}: {link}" for title, link in new_listings])
    msg = MIMEText(msg_body)
    msg["Subject"] = "Nové byty na Sreality.cz"
    msg["From"] = os.getenv("EMAIL_FROM")
    msg["To"] = os.getenv("EMAIL_TO")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.getenv("EMAIL_FROM"), os.getenv("EMAIL_PASSWORD"))
        server.sendmail(msg["From"], [msg["To"]], msg.as_string())

if __name__ == "__main__":
    listings = fetch_listings()
    # Tady můžeš uložit poslední výpis do souboru a porovnat s předchozím, abys posílal jen nové
    if listings:
        send_email(listings)
