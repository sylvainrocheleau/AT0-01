matches = {'code': 0, 'rid': '171900382991317', 'data': {'subid': '-5008563620954894069', 'data': {'game': {'24941473': {'id': 24941473, 'market': 147}, '24941633': {'id': 24941633, 'market': 126}, '24941986': {'id': 24941986, 'market': 147}, '24924247': {'id': 24924247, 'market': 338}, '24924248': {'id': 24924248, 'market': 329}, '24924417': {'id': 24924417, 'market': 348}, '24924418': {'id': 24924418, 'market': 344}, '24924419': {'id': 24924419, 'market': 344}, '24924869': {'id': 24924869, 'market': 357}, '24924870': {'id': 24924870, 'market': 332}, '24924871': {'id': 24924871, 'market': 342}, '24944974': {'id': 24944974, 'market': 19}, '24946164': {'id': 24946164, 'market': 128}, '24946165': {'id': 24946165, 'market': 125}, '24946166': {'id': 24946166, 'market': 129}, '24984361': {'id': 24984361, 'market': 127}, '24984362': {'id': 24984362, 'market': 128}, '24984374': {'id': 24984374, 'market': 124}, '24930749': {'id': 24930749, 'market': 231}, '24930833': {'id': 24930833, 'market': 229}}}}}

matches = {'code': 0, 'rid': '171900382991317', 'data': {'data': {'game': {'24815902': {'id': 24815902, 'market': 592}, '24815903': {'id': 24815903, 'market': 534}, '24815904': {'id': 24815904, 'market': 483}, '24815905': {'id': 24815905, 'market': 600}, '24996992': {'id': 24996992, 'market': 384}, '24990481': {'id': 24990481, 'market': 373}}}}}


# list_of_competitions = {
#     "Amistosos Internacionales": {"ato_name": "Amistosos Internacionales"},
#     "Eurocopa 2024": {"ato_name": "Eurocopa 2024"},
#     "Serie A: Brasileirao": {"ato_name": "Serie A Brasil"},
#     "La Liga": {"ato_name": "La liga"},
#     "WNBA": {"ato_name": "WNBA"},
#     "NBA": {"ato_name": "NBA"},
#     "MLS": {"ato_name": "Major League Soccer USA"},
#     "Copa  América": {"ato_name": "Copa  América"},
# }

for key_06, value_06 in matches["data"]["data"]["game"].items():
    print(key_06)
