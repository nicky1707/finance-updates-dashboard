import concurrent.futures
import requests
from bs4 import BeautifulSoup
from watchlist.models import Watchlist


# ====== Parse multiple news for multiple companies


def process_query(query, max_queries):
    base_url = "https://news.google.com/rss/search?q="
    # Modify to use company name from the portfolio dictionary
    url = base_url + "+".join(query["name"].split())
    response = requests.get(url)
    xml_content = response.text
    soup = BeautifulSoup(xml_content, "lxml-xml")

    query_results = []
    query_count = 0

    for item in soup.find_all("item"):
        title = item.find("title").text
        link = item.find("link").text
        date = item.find("pubDate").text
        source = item.find("source").text
        # Modify to use company name from the portfolio dictionary
        img_link = "-".join(query["name"].split()).lower()
        src_link = f"images/{img_link}.svg"
        result = {
            "title": title,
            "link": link,
            "date": date[0:16],
            "source": source,
            "src_link": src_link,
            # Include the industry from the portfolio dictionary
            "industry": query["industries"][0],
        }
        query_results.append(result)

        query_count += 1
        if query_count == max_queries:
            break

    return query, query_results


def get_news(queries, max_queries):
    results = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for query in queries:
            futures.append(executor.submit(process_query, query, max_queries))

        for future in concurrent.futures.as_completed(futures):
            query, query_results = future.result()
            # Modify to use company name from the portfolio dictionary
            results[query["name"]] = query_results

    return results


# ====== parse multiple news for single company


def search_news(query, max_query):
    url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}"
    results = {}  # Dictionary to store the results for each query
    response = requests.get(url)
    xml_content = response.text
    soup = BeautifulSoup(xml_content, "lxml-xml")
    query_results = (
        []
    )  # List to store the dictionaries of title and link for each query
    query_count = 0  # Counter variable for each query

    for item in soup.find_all("item"):
        title = item.find("title").text
        link = item.find("link").text
        date = item.find("pubDate").text
        source = item.find("source").text
        img_link = "-".join(query.split()).lower()
        src_link = f"images/{img_link}.svg"
        result = {
            "title": title,
            "link": link,
            "date": date[0:16],
            "source": source,
            "src_link": src_link,
        }
        query_results.append(result)

        query_count += 1
        if (
            query_count == max_query
        ):  # Break the loop when the maximum query count is reached
            break

        results[query] = query_results
    return results


# ====== parse exchange rate and gold rate


def process_item(item):
    try:
        response = requests.get(item["url"])
        soup = BeautifulSoup(response.content, "html.parser")

        if item["method"] == "usd":
            element = soup.find(
                "p", class_="result__BigRate-sc-1bsijpp-1 iGrAod"
            ).get_text()
        elif item["method"] == "gold":
            element = soup.find(id=item["element_id"]).get_text()

        if element is not None:
            return element.strip()
    except (requests.exceptions.RequestException, AttributeError):
        pass

    return None


def get_price(item):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(process_item, item)
        result = future.result()

    return result


def get_current_price():
    gold = {
        "url": "https://www.goodreturns.in/gold-rates/chennai.html",
        "element_id": "el",
        "method": "gold",
    }

    usd = {
        "url": "https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=INR",
        "element_id": "result__BigRate-sc-1bsijpp-1 iGrAod",
        "method": "usd",
    }

    with concurrent.futures.ThreadPoolExecutor() as executor:
        gold_future = executor.submit(process_item, gold)
        usd_future = executor.submit(process_item, usd)

        gold_price = gold_future.result()
        usd_rate = usd_future.result()

    if gold_price != None:
        current_price = {"gold": gold_price[1:], "usd": usd_rate[0:6]}
    else:
        current_price = "site error"

    return current_price

# ====== Get list of company associated with given watchlist name


def get_companies(watchlist_name):
    watchlist = Watchlist.objects.get(name=watchlist_name)
    companies = watchlist.companies.all()
    company_list = []
    for company in companies:
        # Get all related industries for the company
        industries = company.industries.all()
        industry_names = [industry.name for industry in industries]

        company_list.append({"name": company.name, "industries": industry_names})

    return company_list, watchlist
