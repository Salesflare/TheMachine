---
title: Graph
area: graph
summary: Les personnes, organisations et projets mentionnés dans vos messages, qui se mettent à jour tout seuls.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 4dbe1a4e1702b1c1
---
Votre Machine crée une carte des personnes avec qui vous échangez et de ce qui se passe, à partir de vos messages, réunions et décisions. Rien à configurer, et tout reste sur votre Machine.

- [Personnes](people.md) : toutes les personnes avec qui vous êtes en contact, avec un résumé et une chronologie pour chacune.
- [Organisations](organizations.md) : les entreprises où elles travaillent, avec leurs équipes et leurs projets.
- [Projets](projects.md) : ce qui se passe, dans des tableaux avec des étapes, comme les opportunités dans un CRM.

## Mis à jour aujourd’hui

Une petite ligne discrète en haut de chaque liste indique ce que votre Machine a mis à jour aujourd’hui, par exemple **4 personnes mises à jour aujourd’hui**. Touchez-la pour voir qui et quoi a changé. Un nom ouvre sa page, avec **Modifications récentes** affiché. Un petit point marque chaque ligne et chaque tuile de tableau modifiée aujourd’hui. Le décompte inclut uniquement les modifications faites par votre Machine, depuis minuit.

## Filtrer et trier

**Filtrer**, à côté des onglets, permet de limiter la liste. Chaque liste a ses propres filtres. Personnes : proximité, dernier contact, organisation, propriétaire, tag et **A un projet ouvert**. Organisations : secteur, spécialité, taille, pays, dernier contact, propriétaire, tag et **A un projet ouvert**. Projets : propriétaire, tableau, étape, tag, organisation, valeur, date de clôture prévue et **Sans réponse depuis plus de 10 jours**.

Les filtres sélectionnés s’affichent au-dessus de la liste, avec **Effacer**. Dans Projets, la liste et le tableau partagent le même filtre. Sur téléphone, les filtres s’ouvrent dans un panneau.

Le menu de tri permet de trier la liste. Personnes et Organisations peuvent être triées par proximité, contact le plus récent ou le plus ancien, et par nom. Organisations peut aussi être triée par taille. Projets peut aussi être trié par **Valeur** et **Date de clôture**. **Télécharger le CSV**, sous le menu de tri, enregistre l’onglet ouvert dans un fichier tableur.

## Champs et tags

Dans la section Champs d’une personne, organisation ou projet, cliquez sur une valeur pour la modifier : **Enregistrer** ou Entrée valide la modification, **Annuler** ou Échap l’abandonne, et **Retirer** efface la valeur.

**Gérer les champs** ajoute ou retire des champs pour toutes les fiches de ce type. **Nouveau champ** en ajoute un : texte, nombre, date ou choix dans une liste.

**+ Tag** ajoute un tag, comme VIP ou partenaire ; **×** le retire. Les tags s’affichent dans les listes et **Filtrer** permet de les retrouver.

## Anniversaire

L’anniversaire d’une personne s’affiche sous Contact, avec sa source : son contact Google, un anniversaire dans Google Calendar (la routine Anniversaires l’enregistre pour les contacts proches), un import Facebook ou vous-même. **Modifier** permet de l’ajouter ou de le corriger : indiquez le mois et le jour, et l’année si vous la connaissez (l’âge de la personne s’affichera aussi). La date que vous saisissez remplace celles des autres sources et est conservée. **Retirer** la supprime ; elle ne sera pas rétablie par un contact ou un import.

Si aucun anniversaire n’est indiqué, **Ajouter l’anniversaire** dans Champs permet de l’ajouter. La routine Anniversaires lit la même date que celle affichée sur la page. Un anniversaire est une information personnelle : il n’est jamais transmis à votre équipe, même sur une fiche partagée.

## Importer un tableur

**Importer un CSV…**, sous le menu de tri dans Personnes, Organisations ou Projets, permet d’ajouter un tableur enregistré au format CSV.

1. Vérifiez les colonnes. Votre Machine devine à quoi elles correspondent à partir de leurs en-têtes et de leur contenu. Vous pouvez modifier ses choix. Lorsque votre modèle peut s’exécuter, il vérifie aussi les colonnes et indique brièvement ce qui lui semble incertain. Il ne voit que les en-têtes, quelques valeurs par colonne et les cellules que les règles n’ont pas pu lire.
2. Vérifiez les corrections. **Vérifier** les présente avant et après : espaces en trop, noms en majuscules, numéros de téléphone au format international, fautes dans les e-mails (gmial.com), sites web réduits à leur domaine, dates et valeurs dans n’importe quel format (« €12k » devient 12000), plusieurs tags dans une même cellule, étape écrite différemment et lignes en double. Décochez un type de correction ou une ligne pour ne pas l’appliquer.
3. Vérifiez l’aperçu. Chaque ligne est nouvelle, correspond à une fiche déjà présente dans votre Graph ou est ignorée, avec une explication. Une personne est reconnue par son e-mail (ou, à défaut, par son nom et son organisation), une organisation par son site web ou son nom, et un projet par son nom.
4. **Importer** ajoute les nouvelles fiches et complète celles qui existent déjà. Une cellule vide ne change rien.

**Annuler** juste après l’import, ou **Annuler le dernier import** sous le menu de tri, annule le dernier import tant que ces fiches n’ont pas été modifiées depuis. Si l’annulation écrasait une correction faite après l’import, un message vous en explique la raison. Le fichier reste sur votre Machine.

## Propriétaire

Dans une Work Fleet, chaque personne, organisation et projet a un propriétaire : **Propriétaire**, sous Avec vous sur sa page. C’est vous, sauf si vous choisissez quelqu’un de votre Work Fleet. **Propriétaire** dans Filtrer n’affiche que vos fiches. Chaque modification apparaît dans la chronologie.

## Équipe

**Équipe**, à côté de Mes éléments, affiche ce que vos coéquipiers partagent, avec les mêmes onglets et le même menu de tri. **Filtrer** permet de limiter la liste selon la personne qui a partagé l’élément, une organisation (Personnes) ou un état (Projets). Ce que vous y ajoutez vous appartient.

Le travail client est partagé avec les Machines de vos coéquipiers, avec son propriétaire, ses champs et ses tags. Leurs éléments s’affichent aussi dans la vôtre. Chaque fil indique **Équipe** ou **Vous seul**. Consultez [Graph d’équipe](team-graph.md).
