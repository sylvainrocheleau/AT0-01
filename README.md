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
4. Faire tourner comp_spider_01
5. Vérifier que les noms d'équipe sont normalisés dans V2_Team_Names
6. Si les équipes ne sont pas normalisées, aller dans Dash_Teams_to_update et filter par bookie et compétition
7. Suivre les instructions [pour normaliser les noms d'équipe](https://docs.google.com/document/d/1btxYAmFdTrhuHYIDWfrwl2DV_G3_HD1DXYhBupCqMlk/edit?tab=t.0#bookmark=id.b0ho7maigb5s)
8. Faire tourner comp_spider_01 pour s'assurer que les noms de match sont sauvegardés dans V2_Matches_Urls
9. Ajouter les valeurs "Markets" dans le dictionnaire list_of_markets_V2 de bookies_config
10. Aller dans def parse_match dans parsing_logic.py et s'assure rque le xpatch de selections_keys fonctionne
11. Faire tourner match_spider_01
