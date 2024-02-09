import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd

headers = {"User-Agent": "Your User Agent"}


def scrape_mobile_prices(product_name, model_name):
    url_1 = "https://www.amazon.in/"
    url_2 = "https://www.flipkart.com/"
    url_list = [url_1, url_2]
    fetched_data = []
    for url in url_list:
        domain_name = urlparse(url).netloc.split('.')[1]
        if domain_name == "amazon":
            search_url = url + "s?k=" + "+".join(product_name.split()) + "+" + "+".join(model_name.split())
            fetched_data.extend(amazon_data_scrap(search_url, domain_name))
        elif domain_name == "flipkart":
            search_url = url + "search?q=" + "+".join(product_name.split()) + "+" + "+".join(model_name.split())
            fetched_data.extend(flipkart_data_scrap(search_url, domain_name))
    return fetched_data


def amazon_data_scrap(search_url, domain_name):
    response = requests.get(search_url, headers=headers)
    scraped_data = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        product_results = soup.find_all("div", {"data-component-type": "s-search-result"})

        for product_result in product_results:
            title_element = product_result.find("h2")
            if title_element:
                product_title = title_element.text.strip()

                price_element = product_result.find("span", {"class": "a-offscreen"})
                if price_element:
                    product_price = price_element.text.strip()

                    delivery_date_element = soup.find("span", attrs={"class": "a-color-base a-text-bold"})
                    if delivery_date_element:
                        delivery_date = delivery_date_element.text.strip()

                        delivery_charge_element = soup.find("a" , attrs={"class":"a-link-normal"})
                        if delivery_charge_element:
                            delivery_charge = delivery_charge_element.text.strip()

                        print("Domain:", domain_name)
                        print("Product Title:", product_title)
                        print("Product Price:", product_price)
                        print("Delivery Date:", delivery_date)
                        print("Delivery Charge:", delivery_charge)
                        scraped_data.append({
                            "Domain": domain_name,
                            "Product Title": product_title,
                            "Product Price": product_price,
                            "Delivery Date": delivery_date,
                            "Delivery Charge": delivery_charge
                        })
                        print("=" * 50)

    else:
        print("Failed to fetch search results")
    return scraped_data


def flipkart_data_scrap(search_url, domain_name):
    response = requests.get(search_url, headers=headers)
    scraped_data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        product_containers = soup.find_all("div", {"class": "_1AtVbE"})

        for container in product_containers:
            title_element = container.find("div", {"class": "_4rR01T"})
            if title_element:
                product_title = title_element.text.strip()

                price_element = container.find("div", {"class": "_30jeq3"})
                if price_element:
                    product_price = price_element.text.strip()

                    try:
                        delivery_date_element = container.find_all("div", {"class": "_2Tpdn3"})
                        if delivery_date_element:
                            delivery_date = delivery_date_element[1].get_text()

                            delivery_charge_element = soup.find("div", attrs={"class": "_2Tpdn3"})
                            if delivery_charge_element:
                                delivery_charge = delivery_charge_element.text.strip()

                            print("Domain:", domain_name)
                            print("Product Title:", product_title)
                            print("Product Price:", product_price)
                            print("Delivery Date:", delivery_date)
                            print("Delivery Charge:",delivery_charge)
                            scraped_data.append({
                                "Domain": domain_name,
                                "Product Title": product_title,
                                "Product Price": product_price,
                                "Delivery Date": delivery_date,
                                "Delivery Charge": delivery_charge
                            })
                            print("=" * 50)
                    except Exception as e:
                        print(f"ERROR {e}")

    else:
        print("Failed to fetch search results")
    return scraped_data


if __name__ == "__main__":
    product_name = input("Enter mobile product name: ")
    model_name = input("Enter mobile model name: ")
    scraped_data = scrape_mobile_prices(product_name, model_name)
    df = pd.DataFrame(scraped_data)
    excel_filename = "productlist.xlsx"
    df.to_excel(excel_filename, index=False)

    print(f"Scraped data saved to {excel_filename}")


