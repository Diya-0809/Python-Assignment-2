import re
import os

def parse_and_rank_products(file_paths, k):
    # Regex patterns for HTML extraction
    name_pattern = re.compile(r'class=["\']product-name["\'][^>]*>(.*?)<\/|\bname\b["\']?:\s*["\']([^"\']+)["\']', re.IGNORECASE)
    price_pattern = re.compile(r'[\$₹]?\s*(\d+(?:\.\d+)?)')
    rating_pattern = re.compile(r'(\d+(?:\.\d+)?)\s*(?:\/\s*5|\s*stars?|\s*rating)', re.IGNORECASE)

    products = {} # name -> (rating, price)

    for path in file_paths:
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
            # Simple line/block parsing for product items
            blocks = re.findall(r'<div[^>]*class=["\']product["\'][^>]*>(.*?)</div>', content, re.DOTALL | re.IGNORECASE)
            if not blocks:
                blocks = [content]

            for block in blocks:
                names = name_pattern.findall(block)
                prices = price_pattern.findall(block)
                ratings = rating_pattern.findall(block)

                if names and prices and ratings:
                    name = (names[0][0] or names[0][1]).strip()
                    price = float(prices[0])
                    rating = float(ratings[0])

                    if name not in products:
                        products[name] = (rating, price)
                    else:
                        # Keep better rating or lower price if tied
                        curr_rating, curr_price = products[name]
                        if rating > curr_rating or (rating == curr_rating and price < curr_price):
                            products[name] = (rating, price)

    # Sorting criteria: Highest rating (-rating), Lowest price (price), Lexicographical name (name)
    sorted_products = sorted(products.items(), key=lambda x: (-x[1][0], x[1][1], x[0]))

    for name, (rating, price) in sorted_products[:k]:
        print(f"{name} {int(price) if price.is_integer() else price} {rating}")

if __name__ == "__main__":
    p_k = input().strip().split()
    if p_k:
        p, k = int(p_k[0]), int(p_k[1])
        files = [input().strip() for _ in range(p)]
        parse_and_rank_products(files, k)
