import re

def extract_competition_id(url):
    match = re.search(r'competition=(\d+)', url)
    if match:
        return int(match.group(1))
    return None

urls = ["https://sportsbook.betsson.es/#/sport/?type=0&region=20001&competition=566&sport=1",
 "https://sportsbook.betsson.es/#/sport/?type=0&sport=3&region=20003&competition=686",
 "https://sportsbook.betsson.es/#/sport/?type=0&region=20001&competition=1861&sport=1",
 "https://sportsbook.betsson.es/#/sport/?type=0&sport=1&competition=541&region=900001",
 "https://sportsbook.betsson.es/#/sport/?type=0&sport=1&competition=548&region=830001",
 "https://sportsbook.betsson.es/#/sport/?type=0&sport=1&competition=1685&region=180001",
 "https://sportsbook.betsson.es/#/sport/?type=0&sport=1&competition=1792&region=390001",
 "https://sportsbook.betsson.es/#/sport/?type=0&sport=1&competition=538&region=1850001",
 "https://sportsbook.betsson.es/#/sport/?type=0&sport=1&competition=543&region=1170001",
 "https://sportsbook.betsson.es/#/sport/?type=0&sport=1&competition=545&region=2150001",
 "https://sportsbook.betsson.es/#/sport/?type=0&region=20001&competition=18278410&sport=1",
 "https://sportsbook.betsson.es/#/sport/?type=0&game=25519596&competition=756&sport=3&region=50003",
 "https://sportsbook.betsson.es/#/sport/?type=0&game=27251301&region=10001&competition=4171&sport=1",
 "https://sportsbook.betsson.es/#/sport/?type=0&game=27404283&region=10001&competition=4171&sport=1",
 "https://sportsbook.betsson.es/#/sport/?type=0&game=25519596&competition=792&sport=3&region=2150003",
 "https://sportsbook.betsson.es/#/sport/?type=0&game=25582234&region=20001&competition=27844&sport=1",
 "https://sportsbook.betsson.es/#/sport/?type=0&game=25807433&region=2150001&competition=553&sport=1",
 "https://sportsbook.betsson.es/#/sport/?type=0&game=25848065&region=2570001&competition=564&sport=1",
 "https://sportsbook.betsson.es/#/sport/?type=0&game=26905490&region=20001&competition=27844&sport=1",
 "https://sportsbook.betsson.es/#/sport/?type=0&game=25432826&region=2420001&competition=3025&sport=1",
 "https://sportsbook.betsson.es/#/sport/?type=0&game=25590940&region=10001&competition=18278053&sport=1",
 "https://sportsbook.betsson.es/#/sport/?type=0&sport=1&competition=566&region=20001"]
# Example usage:
for url in urls:
    competition_id = extract_competition_id(url)
    print("from def", competition_id)
    print("from code",int(url.split("competition=")[1].split("&")[0])) # Alternative method
