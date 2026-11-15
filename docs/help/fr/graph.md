---
title: Le Graph
area: graph
summary: Les personnes, les organisations et les projets de vos messages, mis à jour automatiquement.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: e437109f98725e65
---
Votre Machine crée une carte des personnes avec qui vous échangez et de ce qui se passe, à partir de vos messages, réunions et décisions. Rien à configurer, et tout reste sur votre Machine.

- [Personnes](people.md) : toutes les personnes avec qui vous échangez, avec un résumé et une chronologie pour chacune.
- [Organisations](organizations.md) : les entreprises où elles travaillent, avec leurs personnes et leurs projets.
- [Projets](projects.md) : ce qui se passe, dans des tableaux avec des étapes, comme les affaires dans un CRM.
- [Notes](notes.md) : une page facile à lire par sujet, par exemple un voyage ou votre Maison.

## Mis à jour aujourd’hui

Une discrète ligne en haut de chaque liste indique ce que votre Machine a mis à jour aujourd’hui, par exemple **4 personnes mises à jour aujourd’hui**. Touchez-la pour voir qui et quoi a changé. Touchez un nom pour ouvrir sa page, avec **Modifications récentes** affiché. Un petit point marque chaque ligne et chaque tuile de tableau modifiée aujourd’hui. Seules les modifications apportées par votre Machine depuis minuit sont comptabilisées.

## Filtrer et trier

**Filtrer**, à côté des onglets, permet d’affiner la liste. Chaque liste a ses propres filtres. Personnes : proximité, dernier contact, organisation, propriétaire, tag et **A un projet ouvert**. Organisations : secteur, spécialité, taille, pays, dernier contact, propriétaire, tag et **A un projet ouvert**. Projets : propriétaire, tableau, étape, tag, organisation, valeur, date de clôture prévue et **Sans réponse depuis plus de 10 jours**.

Les filtres sélectionnés s’affichent au-dessus de la liste, avec **Effacer**. Dans Projets, la liste et le tableau partagent le même filtre. Sur téléphone, les filtres s’ouvrent dans un panneau.

Le menu de tri permet de trier la liste. Personnes et Organisations peuvent être triées par proximité, date du contact, de la plus récente à la plus ancienne, ou par nom. Organisations peut aussi être triée par taille. Projets peut être trié par dernière activité, nom, étape, **Valeur** et **Date de clôture**. **Télécharger le CSV**, sous le menu de tri, enregistre l’onglet ouvert sous forme de feuille de calcul.

## Champs et tags

Sous Champs, sur la page d’une personne, d’une organisation ou d’un projet, cliquez sur une valeur pour la modifier : **Enregistrer** ou Entrée pour la conserver, **Annuler** ou Échap pour abandonner, **Retirer** pour la supprimer.

**Gérer les champs** (**Ajouter un champ** si aucun champ n’est présent) permet d’ajouter ou de supprimer des champs pour toutes les fiches de ce type. **Nouveau champ** permet d’en ajouter un : texte, nombre, date ou choix dans une liste.

**+ Tag** permet d’ajouter un tag, comme VIP ou partenaire. **×** permet de le retirer. Les tags s’affichent dans les listes et **Filtrer** permet de les rechercher.

## Anniversaire

L’anniversaire d’une personne s’affiche sous Contact, avec sa source : son contact Google, un anniversaire dans Google Calendar (la routine Birthdays l’enregistre pour les personnes proches), une importation Facebook, vos notes ou vous-même. **Modifier** permet de le saisir ou de le corriger : le mois et le jour, et l’année si vous la connaissez (son âge s’affiche alors aussi).

La date que vous saisissez prime sur toutes les sources et reste enregistrée. **Retirer** la supprime. Un contact ou une importation ne la rétablira pas.

Si aucun anniversaire n’est renseigné, **Ajouter l’anniversaire** sous Champs permet de l’ajouter. La routine Birthdays lit le même anniversaire que celui affiché sur la page. Un anniversaire est personnel : il n’est jamais transmis à votre équipe, même sur une fiche partagée.

## Importer une feuille de calcul

**Importer un CSV…**, sous le menu de tri de Personnes, Organisations ou Projets, permet d’ajouter une feuille de calcul enregistrée au format CSV.

1. Vérifiez les colonnes. Votre Machine devine à quoi elles correspondent à partir des en-têtes et de leur contenu. Vous pouvez les modifier. Lorsque votre modèle peut fonctionner, il les vérifie aussi et indique brièvement les points dont il n’est pas sûr. Il ne voit que les en-têtes, quelques valeurs par colonne et les cellules que les règles n’ont pas pu lire.
2. Vérifiez les corrections. **Vérifier** affiche les changements, avant et après : espaces en trop, noms en majuscules, numéros de téléphone au format international, fautes de frappe dans les adresses e-mail (gmial.com), sites web remplacés par leur nom de domaine, dates et valeurs dans n’importe quel format (« €12k » devient 12000), plusieurs tags dans une cellule, étape écrite différemment et même ligne en double. Décochez un type de correction ou une ligne pour la laisser telle quelle.
3. Vérifiez l’aperçu. Chaque ligne est nouvelle, correspond à une fiche déjà présente dans votre Graph ou est ignorée, avec une explication. Une personne correspond à une adresse e-mail (sinon, au nom et à l’organisation), une organisation à son site web ou à son nom, et un projet à son nom.
4. **Importer** ajoute les nouvelles fiches et complète les fiches correspondantes. Une cellule vide ne change rien.

**Annuler** juste après l’importation, ou **Annuler le dernier import** sous le menu de tri, permet d’annuler la dernière importation tant que les fiches concernées n’ont pas changé depuis. Si l’annulation écraserait une correction effectuée plus tard, un message vous en explique la raison. Le fichier reste sur votre Machine.

## Propriétaire

Dans une Fleet de travail, chaque personne, organisation et projet a un propriétaire : **Propriétaire**, sous Avec vous sur sa page. C’est vous, sauf si vous choisissez quelqu’un dans votre Fleet de travail. Le filtre **Propriétaire** affiche uniquement les fiches dont vous êtes propriétaire. Chaque modification apparaît dans la chronologie.

## Équipe

**Équipe**, à côté de À moi, affiche ce que vos collègues partagent, avec les mêmes onglets et le même menu de tri. **Filtrer** permet d’affiner la liste par personne ayant partagé la fiche, par organisation (Personnes) ou par état (Projets). Ce que vous ajoutez ici vous appartient.

Le travail client est partagé avec les Machines de vos collègues, avec son propriétaire, ses champs et ses tags. Leurs fiches s’affichent dans les vôtres. Chaque fil indique **Équipe** ou **Vous seul**. Consultez [Graph d’équipe](team-graph.md).
