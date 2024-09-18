import os
import json

# get current directory
cookie = [{}]
parent = os.path.dirname(os.getcwd())
with open(parent+"/scrapy_playwright_ato/spiders/cookies.json", "w") as f:
    f.write(json.dumps(cookie))
