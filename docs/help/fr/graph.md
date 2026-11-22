---
title: Le Graph
area: graph
summary: Les personnes, les organisations et les projets dans vos messages, automatiquement mis à jour.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 9052c679e45207f7
---
Votre Machine crée une carte des personnes avec qui vous échangez et de ce qui se passe, à partir de vos messages, réunions et décisions. Rien à configurer, et tout reste sur votre Machine.

- [Personnes](people.md) : toutes les personnes avec qui vous êtes en contact, avec un résumé et une chronologie pour chacune.
- [Organisations](organizations.md) : les entreprises où elles travaillent, avec leurs personnes et leurs projets.
- [Projets](projects.md) : ce qui se passe, dans des tableaux avec des étapes, comme les opportunités dans un CRM.

## Mis à jour aujourd’hui

Une ligne discrète en haut de chaque liste indique ce que votre Machine a mis à jour aujourd’hui, par exemple **4 personnes mises à jour aujourd’hui**. Touchez-la pour voir qui et ce qui a changé. Un nom ouvre sa page, avec **Modifications récentes** affiché. Un petit point signale chaque ligne et chaque vignette de tableau modifiées aujourd’hui. Seules les modifications effectuées par votre Machine depuis minuit sont comptabilisées.

## Filtrer et trier

**Filtrer**, à côté des onglets, réduit la liste. Chaque liste a ses propres filtres. Personnes : proximité, dernier contact, organisation, propriétaire, tag et **A un projet ouvert**. Organisations : secteur, spécialité, taille, pays, dernier contact, propriétaire, tag et **A un projet ouvert**. Projets : propriétaire, tableau, étape, tag, organisation, valeur, date de clôture prévue et **Sans réponse depuis plus de 10 jours**.

Les filtres sélectionnés s’affichent au-dessus de la liste, avec **Effacer**. Dans Projets, la liste et le tableau partagent le même filtre. Sur téléphone, les filtres s’ouvrent dans un panneau.

Le menu de tri permet de trier la liste. Les personnes et les organisations peuvent être triées par proximité, par contact le plus récent ou le plus ancien, et par nom. Les organisations peuvent aussi être triées par taille. Les projets peuvent être triés par dernière activité, nom, étape, **Valeur** et **Date de clôture**. **Télécharger le CSV**, sous le menu de tri, enregistre l’onglet ouvert dans un tableur.

## Champs et tags

Sous Champs, sur la page d’une personne, d’une organisation ou d’un projet, cliquez sur une valeur pour la modifier : **Enregistrer** ou Entrée pour la garder, **Annuler** ou Échap pour quitter sans l’enregistrer, **Retirer** pour la supprimer.

**Gérer les champs** (**Ajouter un champ** si aucun champ n’est présent) permet d’ajouter ou de retirer des champs pour toutes les fiches de ce type. **Nouveau champ** permet d’ajouter un champ de texte, un nombre, une date ou un choix dans une liste.

**+ Tag** permet d’ajouter un tag, par exemple VIP ou partenaire. **×** permet de le retirer. Les tags s’affichent dans les listes (sur téléphone, les tags d’une personne s’affichent sur sa page) et **Filtrer** permet de les trouver.

## Anniversaire

L’anniversaire d’une personne s’affiche sous Contact, avec sa provenance : son contact Google, un anniversaire dans Google Agenda (la routine Anniversaires l’enregistre pour les contacts proches), un import Facebook, vos notes ou vous-même. **Modifier** permet de le définir ou de le corriger : indiquez le mois et le jour, et l’année si vous la connaissez (son âge s’affiche alors aussi).

La date que vous indiquez est prioritaire sur toutes les sources et reste enregistrée. **Retirer** la supprime. Un contact ou un import ne la rétablira pas.

Si aucune date n’est renseignée, **Ajouter l’anniversaire**, sous Champs, permet de l’ajouter. La routine Anniversaires lit la même date que celle affichée sur la page. Un anniversaire est personnel : il n’est jamais transmis à votre équipe, même sur une fiche partagée.

## Importer un tableur

**Importer un CSV…**, sous le menu de tri dans Personnes, Organisations ou Projets, permet d’ajouter un tableur enregistré au format CSV.

1. Vérifiez les colonnes. Votre Machine devine à quoi elles correspondent d’après leurs en-têtes et leur contenu. Vous pouvez les modifier. Lorsque votre modèle peut s’exécuter, il les vérifie aussi et indique brièvement les éléments incertains. Il ne voit que les en-têtes, quelques valeurs par colonne et les cellules que les règles n’ont pas pu lire.
2. Vérifiez les corrections. **Vérifier** les affiche avant et après : espaces en trop, noms en majuscules, numéros de téléphone au format international, fautes de frappe dans les e-mails (gmial.com), sites web ramenés à leur nom de domaine, dates et valeurs dans n’importe quel format (« €12k » correspond à 12 000), plusieurs tags dans une cellule, étape écrite différemment et doublons de lignes. Décochez un type de correction ou une ligne pour ne pas l’appliquer.
3. Vérifiez l’aperçu. Chaque ligne est nouvelle, correspond à une fiche déjà présente dans votre Graph ou est ignorée, avec une explication. Une personne est identifiée par son e-mail (ou, à défaut, par son nom et son organisation), une organisation par son site web ou son nom, et un projet par son nom.
4. **Importer** ajoute les nouvelles fiches et complète celles qui correspondent. Une cellule vide ne change rien.

**Annuler**, juste après l’import, ou **Annuler le dernier import**, sous le menu de tri, annule le dernier import si les fiches n’ont pas changé depuis. Si cela risque d’écraser une correction apportée plus tard, un message vous explique pourquoi. Le fichier reste sur votre Machine.

## Propriétaire

Dans une Fleet Travail, chaque personne, organisation et projet a un propriétaire : **Propriétaire**, sous Avec vous sur sa page. C’est vous, sauf si vous choisissez quelqu’un de votre Fleet Travail. **Propriétaire** dans Filtrer affiche uniquement vos fiches. Chaque modification apparaît dans la chronologie.

## Équipe

**Équipe**, à côté de À moi, affiche ce que vos collègues partagent, avec les mêmes onglets et le même menu de tri. **Filtrer** permet de réduire la liste selon la personne qui a partagé la fiche, une organisation (Personnes) ou un état (Projets). Ce que vous ajoutez ici vous appartient.

Le travail client est partagé avec les Machines de vos collègues, avec son propriétaire, ses champs et ses tags. Leurs fiches s’affichent dans la vôtre. Chaque fil indique **Équipe** ou **Vous seul**. Consultez [Graph d’équipe](team-graph.md).
