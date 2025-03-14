from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Multi-Store Electronic Parts Scraper API!"

@app.route('/search')
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    stores = [
        {"name": "Kotit Tech", "url": f"https://kotit-tech.com/?s={query}", "selector": ".product"},
        {"name": "Makers Electronics", "url": f"https://makerselectronics.com/?s={query}", "selector": ".product"},
        {"name": "UGE-One", "url": f"https://uge-one.com/?s={query}", "selector": ".product"},
        {"name": "Electra Store", "url": f"https://electra.store/?s={query}", "selector": ".product"},
        {"name": "Free Electronic", "url": f"https://free-electronic.com/?s={query}", "selector": ".product"},
        {"name": "Adel Elsamman", "url": f"https://www.adel-elsamman.com/?s={query}", "selector": ".product"},
        {"name": "Fut Electronics", "url": f"https://store.fut-electronics.com/?s={query}", "selector": ".product"},
        {"name": "Ram E-Shop", "url": f"https://www.ram-e-shop.com/?s={query}", "selector": ".product"},
        {"name": "Lampatronics", "url": f"https://lampatronics.com/?s={query}", "selector": ".product"},
        {"name": "Maamoon", "url": f"https://www.maamoon.com/?s={query}", "selector": ".product"},
        {"name": "MostElectronic", "url": f"https://mostelectronic.com/?s={query}", "selector": ".product"},
        {"name": "HD Electronics", "url": f"https://hdelectronicseg.com/?s={query}", "selector": ".product"},
        {"name": "MicroOhm", "url": f"https://microohm-eg.com/?s={query}", "selector": ".product"},
        {"name": "Circuits Elec", "url": f"https://circuits-elec.com/?s={query}", "selector": ".product"},
        {"name": "APQrino", "url": f"https://apqrino.com/?s={query}", "selector": ".product"},
        {"name": "Electrobom", "url": f"https://www.electrobom.com/?s={query}", "selector": ".product"},
        {"name": "Elnekhely", "url": f"https://elnekhely.com:8443/ords/r/org1/a13320221209064449961/nekhely?search={query}", "selector": ".product"},
        {"name": "IC Hat", "url": f"https://ic-hat.com/ar/?s={query}", "selector": ".product"},
        {"name": "Ampere Electronics", "url": f"https://ampere-electronics.com/?s={query}", "selector": ".product"}
    ]

    all_results = []

    for store in stores:
        try:
            response = requests.get(store["url"], headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            products = []

            for product in soup.select(store["selector"]):
                title = product.select_one('.woocommerce-loop-product__title')
                link = product.find('a')['href'] if product.find('a') else None
                price = product.select_one('.price')
                image = product.find('img')['src'] if product.find('img') else None

                products.append({
                    "title": title.text.strip() if title else "No Title",
                    "link": link,
                    "price": price.text.strip() if price else "No Price",
                    "image": image,
                })

            all_results.append({
                "store": store["name"],
                "results": products
            })

        except Exception as e:
            all_results.append({
                "store": store["name"],
                "error": str(e)
            })

    return jsonify(all_results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
