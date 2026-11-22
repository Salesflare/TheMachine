---
title: Le Graph
area: graph
summary: Les personnes, organisations et projets de vos messages, mis à jour automatiquement.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 181ff5fa2a9d8f47
---
Votre Machine crée une carte des personnes avec qui vous échangez et de ce qui se passe, à partir de vos messages, réunions et décisions. Rien à configurer, et tout reste sur votre Machine.

- [Personnes](people.md) : toutes les personnes avec qui vous êtes en contact, avec un résumé et une chronologie pour chacune.
- [Organisations](organizations.md) : les entreprises où elles travaillent, avec leurs personnes et leurs projets.
- [Projets](projects.md) : ce qui se passe, dans des tableaux avec des étapes, comme les opportunités dans un CRM.

Vos propres modifications apparaissent immédiatement. Les nouvelles personnes, les nouveaux messages dans leurs chronologies et les informations recherchées apparaissent sous 30 minutes.

## Mis à jour aujourd’hui

Une ligne discrète en haut de chaque liste indique ce que votre Machine a mis à jour aujourd’hui, par exemple **4 personnes mises à jour aujourd’hui**. Touchez-la pour voir qui et quoi a changé. Un nom ouvre sa page avec **Modifications récentes** affiché. Un petit point marque chaque ligne et chaque tuile de tableau modifiées aujourd’hui. Seules les modifications faites par votre Machine depuis minuit sont comptabilisées.

## Filtrer et trier

**Filtrer**, à côté des onglets, permet de réduire la liste. Chaque liste a ses propres filtres. Personnes : proximité, dernier contact, organisation, propriétaire, tag et **A un projet ouvert**. Organisations : secteur, spécialité, taille, pays, dernier contact, propriétaire, tag et **A un projet ouvert**. Projets : propriétaire, tableau, étape, tag, organisation, valeur, date de clôture prévue et **Sans réponse depuis plus de 10 jours**.

Les filtres sélectionnés s’affichent au-dessus de la liste, avec **Effacer**. Dans Projets, la liste et le tableau partagent le même filtre. Sur téléphone, les filtres s’ouvrent dans un panneau.

Le menu de tri permet de trier la liste. Personnes et Organisations peuvent être triés par proximité, contact le plus récent ou le plus ancien, et nom. Organisations peut aussi être trié par taille. Projets peut être trié par dernière activité, nom, étape, **Valeur** et **Date de clôture**. **Télécharger le CSV**, sous le menu de tri, enregistre l’onglet ouvert sous forme de feuille de calcul.

## Champs et tags

Dans Champs, sur la page d’une personne, d’une organisation ou d’un projet, cliquez sur une valeur pour la modifier. **Enregistrer** ou Entrée confirme la modification. **Annuler** ou Échap l’abandonne. **Retirer** efface la valeur.

**Gérer les champs** (**Ajouter un champ** quand il n’y en a aucun) ajoute ou supprime des champs pour toutes les fiches de ce type. **Nouveau champ** en ajoute un : texte, nombre, date ou choix dans une liste.

**+ Tag** ajoute un tag, par exemple VIP ou partenaire. **×** le retire. Les tags apparaissent dans les listes. Sur téléphone, ceux d’une personne apparaissent sur sa page. **Filtrer** permet de les trouver.

## Anniversaire

L’anniversaire d’une personne apparaît sous Contact, avec sa source : son contact Google, un anniversaire dans Google Agenda (la routine Anniversaires l’enregistre pour un contact proche), un import Facebook, vos notes ou vous. **Modifier** permet de le définir ou de le corriger : mois et jour, et année si vous la connaissez. L’âge de la personne s’affiche alors aussi.

La date que vous saisissez remplace toutes les autres sources et est conservée. **Retirer** la supprime. Elle ne sera pas rétablie par un contact ni par un import.

Sans date, **Ajouter l’anniversaire** sous Champs permet de l’ajouter. La routine Anniversaires lit la même date que celle affichée sur la page. Un anniversaire est une information personnelle : il n’est jamais transmis à votre équipe, même sur une fiche partagée.

## Importer une feuille de calcul

**Importer un CSV…**, sous le menu de tri de Personnes, Organisations ou Projets, ajoute une feuille de calcul enregistrée au format CSV.

1. Vérifiez les colonnes. Votre Machine essaie de les identifier à partir de leurs en-têtes et de leur contenu. Vous pouvez modifier ses choix. Lorsque votre modèle peut s’exécuter, il vérifie aussi les colonnes et indique brièvement les cas incertains. Il ne voit que les en-têtes, quelques valeurs par colonne et les cellules que les règles n’ont pas pu lire.
2. Vérifiez les corrections. **Vérifier** les affiche avant et après : espaces superflus, noms en majuscules, numéros de téléphone au format international, erreurs dans les e-mails (gmial.com), sites web réduits à leur domaine, dates et valeurs dans n’importe quel format (« 12 k€ » devient 12000), plusieurs tags dans une même cellule, étape écrite différemment et ligne en double. Décochez un type de correction ou une ligne pour la laisser telle quelle.
3. Vérifiez l’aperçu. Chaque ligne est nouvelle, correspond à une fiche de votre Graph ou est ignorée, avec une explication. Une personne est reconnue par son e-mail, ou par son nom et son organisation si elle n’en a pas. Une organisation est reconnue par son site web ou son nom, et un projet par son nom.
4. **Importer** ajoute les nouvelles fiches et complète celles qui correspondent. Une cellule vide ne change rien.

**Annuler** juste après l’import, ou **Annuler le dernier import** sous le menu de tri, annule le dernier import tant que les fiches concernées n’ont pas changé depuis. Si cela risque d’écraser une correction ultérieure, le système indique pourquoi et n’annule pas l’import. Le fichier reste sur votre Machine.

## Propriétaire

Dans une Fleet Travail, chaque personne, organisation et projet a un propriétaire : **Propriétaire**, sous Avec vous sur sa page. Il s’agit de vous, sauf si vous choisissez quelqu’un de votre Fleet Travail. **Propriétaire** dans Filtrer affiche uniquement vos fiches. Chaque modification apparaît dans la chronologie.

## Équipe

**Équipe**, à côté de À moi, affiche les éléments que vos collègues partagent, avec les mêmes onglets et le même menu de tri. **Filtrer** permet de réduire la liste selon la personne qui a partagé l’élément, l’organisation (Personnes) ou l’état (Projets). Ce que vous ajoutez ici vous appartient.

Les informations sur les clients sont partagées avec les Machines de vos collègues, avec leur propriétaire, leurs champs et leurs tags. Leurs informations apparaissent aussi sur la vôtre. Chaque fil indique **Équipe** ou **Vous seul**. Consultez [Graph d’équipe](team-graph.md).
