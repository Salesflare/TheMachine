---
title: Graph
area: graph
summary: Les personnes, organisations et projets de vos messages, mis à jour automatiquement.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 850a4e2905f54511
---
Votre Machine crée une carte des personnes avec qui vous échangez et de ce qui se passe, à partir de vos messages, réunions et décisions. Rien à configurer, tout reste sur votre Machine.

- [Personnes](people.md) : toutes les personnes avec qui vous êtes en contact, avec un résumé et une chronologie pour chacune.
- [Organisations](organizations.md) : les entreprises où elles travaillent, avec leurs personnes et leurs projets.
- [Projets](projects.md) : ce qui se passe, dans des tableaux avec des étapes, comme les ventes dans un CRM.

## Mise à jour du jour

Une ligne discrète en haut de chaque liste indique ce que votre Machine a mis à jour aujourd’hui, par exemple **4 personnes mises à jour aujourd’hui**. Touchez-la pour voir qui et ce qui a changé. Un nom ouvre sa page avec **Modifications récentes** affiché. Une petite pastille marque chaque ligne et chaque vignette de tableau modifiées aujourd’hui. Seules les modifications effectuées par votre Machine depuis minuit sont comptabilisées.

## Filtrer et trier

**Filtrer**, à côté des onglets, permet d’affiner la liste. Chaque liste a ses propres filtres. Personnes : proximité, dernier contact, organisation, propriétaire, tag et **A un projet ouvert**. Organisations : secteur, spécialité, taille, pays, dernier contact, propriétaire, tag et **A un projet ouvert**. Projets : propriétaire, tableau, étape, tag, organisation, valeur, date de clôture prévue et **Sans réponse depuis plus de 10 jours**.

Les filtres sélectionnés s’affichent au-dessus de la liste, avec **Effacer**. Dans Projets, la liste et le tableau partagent le même filtre. Sur un téléphone, les filtres s’ouvrent dans un panneau.

Le menu de tri permet de trier la liste. Les personnes et les organisations sont classées par proximité, contact le plus récent ou le plus ancien, et par nom. Les organisations peuvent aussi être classées par taille. Les projets sont classés par activité la plus récente, nom, étape, **Valeur** et **Date de clôture**. **Télécharger le CSV**, sous le menu de tri, enregistre l’onglet ouvert dans un tableur.

## Champs et tags

Dans la section Champs d’une personne, d’une organisation ou d’un projet, cliquez sur une valeur pour la modifier : **Enregistrer** ou Entrée la conserve, **Annuler** ou Échap annule la modification, et **Retirer** l’efface.

**Gérer les champs** (**Ajouter un champ** si aucun champ n’est présent) permet d’ajouter ou de retirer des champs pour toutes les fiches de ce type. **Nouveau champ** en ajoute un : texte, nombre, date ou choix dans une liste.

**+ Tag** ajoute un tag, comme VIP ou partenaire. **×** le retire. Les tags apparaissent dans les listes et **Filtrer** permet de les rechercher.

## Anniversaire

L’anniversaire d’une personne apparaît sous Contact, avec sa source : son contact Google, un anniversaire dans Google Calendar (la routine Anniversaires l’enregistre pour un contact proche), un import Facebook, vos notes ou vous-même. **Modifier** permet de le définir ou de le corriger : indiquez le mois et le jour, et l’année si vous la connaissez. Dans ce cas, son âge s’affiche aussi.

La date que vous saisissez a priorité sur toutes les sources et reste enregistrée. **Retirer** la supprime. Un contact ou un import ne la rétablit pas.

Si aucun anniversaire n’est indiqué, **Ajouter l’anniversaire** dans Champs permet de l’ajouter. La routine Anniversaires lit le même anniversaire que celui affiché sur la page. Un anniversaire est une information personnelle : il n’est jamais transmis à votre équipe, même sur une fiche partagée.

## Importer un tableur

**Importer un CSV…**, sous le menu de tri de Personnes, Organisations ou Projets, permet d’ajouter un tableur enregistré au format CSV.

1. Vérifiez les colonnes. Votre Machine devine leur contenu à partir des en-têtes et des données. Vous pouvez modifier ses choix. Lorsque votre modèle peut s’exécuter, il vérifie aussi les colonnes et donne une courte explication en cas de doute. Il ne voit que les en-têtes, quelques valeurs par colonne et les cellules que les règles n’ont pas pu lire.
2. Vérifiez les corrections. **Vérifier** les présente avant et après : espaces superflus, noms en majuscules, numéros de téléphone au format international, erreurs dans les adresses e-mail (gmial.com), sites web réduits à leur nom de domaine, dates et valeurs dans n’importe quel format ("€12k" correspond à 12000), plusieurs tags dans une cellule, étape écrite différemment et lignes en double. Décochez un type de correction ou une ligne pour la laisser telle quelle.
3. Vérifiez l’aperçu. Chaque ligne est nouvelle, correspond à une fiche déjà présente dans votre Graph ou est ignorée, avec une explication. Une personne correspond à une adresse e-mail (sinon à son nom et à son organisation), une organisation à son site web ou à son nom, et un projet à son nom.
4. **Importer** ajoute les nouvelles fiches et complète les fiches correspondantes. Une cellule vide ne change rien.

**Annuler** juste après l’import, ou **Annuler le dernier import** sous le menu de tri, annule le dernier import si ces fiches n’ont pas changé depuis. Si l’annulation écraserait une correction faite plus tard, une explication s’affiche à la place. Le fichier reste sur votre Machine.

## Propriétaire

Dans une Fleet de travail, chaque personne, organisation et projet a un propriétaire : **Propriétaire** sous Avec vous, sur sa page. Il s’agit de vous, sauf si vous choisissez une personne de votre Fleet de travail. Le filtre **Propriétaire** n’affiche que vos fiches. Chaque modification apparaît dans la chronologie.

## Équipe

**Équipe**, à côté de **À moi**, affiche ce que vos coéquipiers partagent, avec les mêmes onglets et le même menu de tri. **Filtrer** permet d’affiner la liste selon la personne qui a partagé la fiche, une organisation (Personnes) ou l’état (Projets). Ce que vous y ajoutez vous appartient.

Le travail client est partagé avec les Machines de vos coéquipiers, avec son propriétaire, ses champs et ses tags. Leurs fiches apparaissent dans les vôtres. Chaque fil indique **Équipe** ou **Vous seul**. Consultez [Graph d’équipe](team-graph.md).
