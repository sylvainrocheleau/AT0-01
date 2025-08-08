PATH = "/home/sylvain/info@sylvainrocheleau.com/projets/AgainstTheOdds/Scrapy_Playwright/scrapy_playwright_ato/spider_log.txt"
CHUNK = 25000
import os
with open(PATH, "r", encoding="utf-8", errors="replace") as f:
    s = f.read()
total = len(s)
parts = (total + CHUNK - 1) // CHUNK
base, ext = os.path.splitext(PATH)
for i in range(parts):
    start = i * CHUNK
    end = min(start + CHUNK, total)
    out_path = f"{base}.part_{i+1:04d}.txt"
    with open(out_path, "w", encoding="utf-8") as out:
        out.write(s[start:end])
    print(f"Wrote {out_path} ({end-start} chars)")
print(f"Total chars: {total}, Parts: {parts}")
