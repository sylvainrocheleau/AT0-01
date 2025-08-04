from utilities import Helpers

# competitions = Helpers().load_competitions()
#
# def add_bigrams(names):
#     variants = set(names)
#     for name in names:
#         words = name.split()
#         for i in range(len(words) - 1):
#             bigram = f"{words[i]} {words[i+1]}"
#             variants.add(bigram)
#     return list(variants)
#
# competitions_names_and_variants = {}
# for x in competitions:
#     if x[3] == "3":
#         base_names = list({x[1], x[2]})
#         competitions_names_and_variants[x[0]] = add_bigrams(base_names)
#
# print(competitions_names_and_variants)

print(Helpers().load_competiton_names_and_variants(sport_id="3"))
