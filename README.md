Étapes pour les modifications de code

1. Pull de Github
2. Modification d'un spider
3. Commit and push
4. Avertir le gestionnaire de projet
5. Test du code par le gestionnaire de projet

Étapes de débuggage
1. Pull de Github
2. Vérification du bogue:
   * Aller dans Zyte et constater que le bogue est réel
   * Si le bookie requiert des cookies, importer V2_Cookies
   * Dans settings.py, s'assurer que TEST_ENV est en local "local"
3. Tester le spider avec au moins une compéttiton
4. Pousser le code vers Github
5. Avertir SR

Étapes pour ajouter un le tennis à un bookie
1. S'assurer à chaque "pull" du code d'ajuster la variable `TEST_ENV` dans `settings.py` à "local" pour tester en local.
2. Ajouter une compétition de tennis ATP à un bookie dans la DB serveur
   * Ajouter la compétition dans la BD locale en suivant les directives de [Add or update competitions urls](https://docs.google.com/document/d/1btxYAmFdTrhuHYIDWfrwl2DV_G3_HD1DXYhBupCqMlk/edit?tab=t.0#bookmark=id.43abmljpfumc)
   *
3. Faire tourner le script de synchronistation de BD
4. Exécuter le fichier [the_janitor.py](scripts/the_janitor.py) pour pouvoir supprimer les matchs qui ne sont plus d'actualité
5. Faire tourner AllSportAPI (scrapy crawl AllSportAPI) pour effectuer une mise à jour des matchs dans la BD
4. Faire tourner comp_spider_01 pour s'assurer que les noms de match sont sauvegardés dans V2_Matches_Urls
5. Vérifier que les noms d'équipe sont normalisés dans V2_Team_Names
6. Si aucune équipe est normalisée, aller dans Dash_Teams_to_update et filter par bookie et compétition
7. Suivre les instructions [pour normaliser les noms d'équipe](https://docs.google.com/document/d/1btxYAmFdTrhuHYIDWfrwl2DV_G3_HD1DXYhBupCqMlk/edit?tab=t.0#bookmark=id.b0ho7maigb5s)
8. Reprendre à partir de l'étape 4
9. Ajouter les valeurs "Markets" dans le dictionnaire list_of_markets_V2 de bookies_config
10. Faire tourner check_list_of_markets de misc_tool.py pour s'assurer que les valeurs sont correctes
10. Aller dans def parse_match dans parsing_logic.py et s'assure que le xpatch de selections_keys fonctionne
11. Faire tourner match_spider_01 en mode raw_html et debugger dans parse_match de parsing_logic.py


Liste de bookies à ajouter ppour le tennis:
- EfBet: timeout
- Luckia: FAIT(multiple comp_url, tobereviewed)
- GoldenPark: timeout
- Bwin: FAIT
- BetWay: FALSE(Every atp tournament has their url)06/08
- AdmiralBet: Potentielles erreurs liées à la base de donnée(à revoir)
- AupaBet: ACCESS DENIED
- Bet777: timeout
- DaznBet: timeout
- Juegging : FALSE
- KirolBet : ACCESS DENIED
- BetfairSportsbook: PAS A FAIRE
- CasinoBarcelona: FALSE(NE CONTIENT QUE JUSTE UN SEUL TOURNOI)
- CasinoGranMadrid: FAIT
- RetaBet
- WilliamHill
- ZeBet : Erreur 403 sur lien de la competition(à revoir)
- EnRacha: FAIT
- JokerBet: FAIT
- LeoVegas: FAIT
- Paston: FAIT

