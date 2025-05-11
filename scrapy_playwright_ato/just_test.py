from bookies_configurations import bookie_config, get_context_infos
from utilities import Helpers

# competitions = [x for x in bookie_config(bookie=["888Sport"]) if x["competition_id"] == "UEFAChampionsLeague"]
# match_filter = {"type": "bookie_and_comp", "params": ["888Sport", "UEFAChampionsLeague"]}
# print(competitions)
#
# all_competitions = Helpers().load_competitions_urls_and_sports()
# all_competitions = {x[1]: {"competition_name_es": x[2], "competition_url_id": x[0] } for x in all_competitions if x[4] == "888Sport"}
# # print(all_competitions)
#
# map_matches_urls = [x[0] for x in Helpers().load_matches_urls("888Sport")]
# # print(map_matches_urls)
# map_matches = {}
# for match in Helpers().load_matches():
#     try:
#         map_matches[match[6]].append(match[0])
#     except KeyError:
#         map_matches.update({match[6]: [match[0]]})
#
# print(map_matches)
import datetime
import time

start_time = datetime.datetime.now()
time.sleep(5.5)
end_time = datetime.datetime.now()
print("Execution time:",(end_time - start_time).total_seconds())
