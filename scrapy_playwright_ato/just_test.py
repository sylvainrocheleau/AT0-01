data =  'https://www.betfair.es/sport/football/argentina-primera-divisi%C3%B3n/ca-platense-san-lorenzo/34564497'

if 'game=' in data:
    game_id = int(data.split("game=")[-1])
elif '/' in data:
    game_id = int(data.split("/")[-1])
else:
    game_id = None
    flag_error = True
print(game_id)


