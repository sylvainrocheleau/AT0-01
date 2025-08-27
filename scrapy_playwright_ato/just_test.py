from utilities import Connect

connection = Connect().to_db(db="ATO_production", table=None)
cursor = connection.cursor()


def clone_bookies_values(source_bookie, value):
    cloned_bookies_values = []
    for cloned_bookie in cloned_bookies:
        print(cloned_bookie)
        cloned_bookies_values.append(values)

    return cloned_bookies_values


query_clones = """
               SELECT vb.bookie_id, vb.bookie_url, vb.cloned_of
               FROM ATO_production.V2_Bookies vb
               WHERE vb.cloned_of IS NOT NULL \
               """
cursor.execute(query_clones)

results = cursor.fetchall()
source_values = []
values = (1,2,3)
# if cloned_bookies:
#     cloned_bookies = {row[2]: ["source": row[0], "clone_url": row[1] for row in cloned_bookies]}

cloned_bookies = {result[2]:[] for result in results}
for result in results:
    cloned_bookies[result[2]].append({result[0]:result[1]})
print(cloned_bookies)
#
# if 'Betsson' in list(set([v["source"] for v in cloned_bookies.values()])):
#     test = clone_bookies_values('Betsson', values)
#     # print(test)
#     for x in test:
#         print(x)
#
