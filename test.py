import requests as req
from bs4 import BeautifulSoup as bs

def decode_secret_message(url):
    response = req.get(url)
    response.raise_for_status()

    soup = bs(response.text, "html.parser")
    points = []

    for row in soup.find_all("tr"):
        cells = row.find_all(["td", "th"])
        
        if len(cells) < 3:
            continue

        values = [cell.get_text(strip=True) for cell in cells]

        try:
            x = int(values[0])
            char = values[1]
            y = int(values[2])
            points.append((x, y, char))
        except ValueError:
            continue

    if not points:
        raise ValueError("No char coordinate data found.")

    max_x = max(x for x, y, char in points)
    max_y = max(y for x, y, char in points)

    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for x, y, char in points:
        grid[y][x] = char

    for row in grid:
        print("".join(row))


print(decode_secret_message(
    "https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub",
))