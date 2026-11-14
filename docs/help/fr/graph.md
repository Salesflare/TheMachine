---
title: The Graph
area: graph
summary: Les personnes, organisations et projets dans vos messages, mis à jour automatiquement.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 850a4e2905f54511
---
Votre Machine crée une carte des personnes avec qui vous échangez et de ce qui se passe, à partir de vos messages, réunions et décisions. Rien à configurer, et tout reste sur votre Machine.

- [Personnes](people.md) : toutes les personnes avec qui vous êtes en contact, avec un résumé et une chronologie pour chacune.
- [Organisations](organizations.md) : les entreprises où elles travaillent, avec leurs personnes et leurs projets.
- [Projets](projects.md) : ce qui se passe, sur des tableaux avec des étapes, comme les affaires dans un CRM.

## Mis à jour aujourd’hui

Une discrète ligne en haut de chaque liste indique ce que votre Machine a mis à jour aujourd’hui, par exemple **4 personnes mises à jour aujourd’hui**. Touchez-la pour voir qui et ce qui a changé. Le nom d’une personne ouvre sa page, avec **Modifications récentes** affiché. Un petit point marque chaque ligne et chaque tuile de tableau modifiée aujourd’hui. Seules les modifications effectuées par votre Machine depuis minuit sont comptabilisées.

## Filtrer et trier

**Filtrer**, à côté des onglets, permet de réduire la liste. Chaque liste a ses propres filtres. Personnes : proximité, dernier contact, organisation, propriétaire, tag et **A un projet ouvert**. Organisations : secteur, spécialité, taille, pays, dernier contact, propriétaire, tag et **A un projet ouvert**. Projets : propriétaire, tableau, étape, tag, organisation, valeur, date de clôture prévue et **Sans réponse depuis plus de 10 jours**.

Les filtres sélectionnés s’affichent au-dessus de la liste, avec **Effacer**. Dans Projets, la liste et le tableau utilisent le même filtre. Sur un téléphone, les filtres s’ouvrent dans un panneau.

Le menu de tri permet de trier la liste. Personnes et Organisations peuvent être triées par proximité, contact le plus récent ou le plus ancien, et par nom. Organisations peut aussi être triée par taille. Projets peut être trié par dernière activité, nom, étape, **Valeur** et **Date de clôture**. **Télécharger le CSV**, sous le menu de tri, enregistre l’onglet ouvert dans un tableur.

## Champs et tags

Dans la section Champs d’une personne, d’une organisation ou d’un projet, cliquez sur une valeur pour la modifier : **Enregistrer** ou Entrée la conserve, **Annuler** ou Échap annule la modification, et **Retirer** la supprime.

**Gérer les champs** (**Ajouter un champ** si aucun champ n’est présent) permet d’ajouter ou de supprimer des champs pour toutes les fiches de ce type. **Nouveau champ** en ajoute un : texte, nombre, date ou choix dans une liste.

**+ Tag** ajoute un tag, comme VIP ou partenaire ; **×** le supprime. Les tags s’affichent dans les listes et **Filtrer** permet de les trouver.

## Anniversaire

L’anniversaire d’une personne s’affiche sous Contact, avec sa source : son contact Google, un anniversaire dans Google Calendar (la routine Anniversaires l’enregistre pour les personnes proches), un import Facebook, vos notes ou vous-même. **Modifier** permet de l’ajouter ou de le corriger : indiquez le mois et le jour, ainsi que l’année si vous la connaissez. Son âge s’affiche alors aussi.

La valeur que vous indiquez remplace toutes les autres et reste enregistrée. **Retirer** la supprime ; un contact ou un import ne la rétablira pas.

Si aucune date n’est indiquée, **Ajouter l’anniversaire** sous Champs permet de l’ajouter. La routine Anniversaires utilise la même date que celle affichée sur la page. Un anniversaire est une information personnelle : il n’est jamais partagé avec votre équipe, même sur une fiche partagée.

## Importer un tableur

**Importer un CSV…**, sous le menu de tri de Personnes, Organisations ou Projets, permet d’ajouter un tableur enregistré au format CSV.

1. Vérifiez les colonnes. Votre Machine devine leur contenu à partir des en-têtes et des données qu’elles contiennent ; vous pouvez modifier ces choix. Lorsque votre modèle peut s’exécuter, il vérifie aussi les colonnes et indique brièvement ses doutes. Il ne voit que les en-têtes, quelques valeurs par colonne et les cellules que les règles n’ont pas pu lire.
2. Vérifiez les corrections. **Vérifier** les présente avant et après : espaces en trop, noms en majuscules, numéros de téléphone au format international, erreurs dans les adresses e-mail (gmial.com), sites web réduits à leur domaine, dates et valeurs dans n’importe quel format (« €12k » correspond à 12000), plusieurs tags dans une même cellule, étape écrite différemment et ligne en double. Décochez un type de correction ou une ligne pour ne pas la modifier.
3. Vérifiez l’aperçu. Chaque ligne est nouvelle, correspond à une fiche déjà présente dans votre Graph ou est ignorée, avec une explication. Une personne est associée par son adresse e-mail (sinon par son nom et son organisation), une organisation par son site web ou son nom, et un projet par son nom.
4. **Importer** ajoute les nouvelles fiches et complète celles qui correspondent. Une cellule vide ne change rien.

**Annuler** juste après l’import, ou **Annuler le dernier import** sous le menu de tri, annule le dernier import si les fiches n’ont pas été modifiées depuis. Si cela risque d’écraser une correction apportée entre-temps, un message vous en explique la raison. Le fichier reste sur votre Machine.

## Propriétaire

Dans une Fleet de travail, chaque personne, organisation et projet a un propriétaire : **Propriétaire**, sous Avec vous sur sa page. C’est vous, sauf si vous choisissez une personne de votre Fleet de travail. **Propriétaire** dans Filtrer affiche uniquement vos fiches. Chaque modification apparaît dans la chronologie.

## Équipe

**Équipe**, à côté de À moi, affiche les éléments partagés par vos collègues, avec les mêmes onglets et le même menu de tri. **Filtrer** permet de réduire la liste selon la personne qui a partagé l’élément, une organisation (Personnes) ou un état (Projets). Les éléments que vous ajoutez ici vous appartiennent.

Les données liées aux clients sont partagées avec les Machines de vos collègues, avec leur propriétaire, leurs champs et leurs tags. Les leurs s’affichent aussi dans la vôtre. Chaque fil indique **Équipe** ou **Vous seul**. Consultez [Graph d’équipe](team-graph.md).
