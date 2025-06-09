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
2. S'assurer que la table "V2_Cookies" est exportée dans la base de données locale, tous les 5 jours.
3. Ajouter une compétition de tennis ATP à un bookie dans une BD locale
   * Ajouter la compétition dans la BD locale en suivant les directives de [Add or update competitions urls](https://docs.google.com/document/d/1btxYAmFdTrhuHYIDWfrwl2DV_G3_HD1DXYhBupCqMlk/edit?tab=t.0#bookmark=id.43abmljpfumc)
   *
