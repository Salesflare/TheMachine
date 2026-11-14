---
title: Détails de l’organisation
area: graph
summary: Secteur d’activité, taille, lieu et logo pour chaque organisation, recherchés à partir de son adresse Web.
covers: enrichment
code: enrichment.py, graph.py, dashboard.html
order: 5
translated: f403410953e50582
---
## D’où viennent ces informations

- Sur une Machine hébergée, les détails des organisations sont recherchés pour vous, sans frais.
- Sur votre propre ordinateur, cette option est désactivée jusqu’à ce que vous ajoutiez une clé pour un service de recherche, comme Apollo, People Data Labs ou Hunter. Consultez le [guide de configuration](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).

Seule l’adresse Web d’une organisation est envoyée, jamais vos messages ni les personnes que vous connaissez au sein de cette organisation. Une Machine hébergée ou une Machine sur The Machine Network effectue jusqu’à 1 000 recherches par jour. Dans les autres cas, la limite est de 50. Chaque recherche est actualisée tous les 90 jours. Les sites partagés et les fournisseurs de messagerie, comme gmail.com, ne sont jamais recherchés. Les personnes font l’objet de leur propre recherche : consultez [Intitulé de poste et photo](people.md#job-title-and-photo).

Si aucun logo n’est trouvé, The Machine utilise l’icône du site Web de l’organisation, enregistrée sur votre Machine. Aucun service de logos ne sait avec qui vous échangez. Si les deux sont disponibles, les petits éléments comme la ligne d’une tâche affichent l’icône carrée.

Quand les résultats de recherche le permettent, jusqu’à 5 spécialités de l’organisation s’affichent sous sa description. Vous pouvez aussi filtrer la liste des organisations par spécialité : **Filtrer**, puis **Spécialité**. Si la recherche sur une personne fournit aussi les détails de son entreprise, ils sont ajoutés à l’organisation, sans qu’il soit nécessaire d’effectuer une recherche distincte. Les détails recherchés au cours des 90 derniers jours restent inchangés.

## Corriger une erreur

Sur la page de l’organisation :

- **Modifier** pour changer le nom, le secteur d’activité, la taille, le lieu, l’année de fondation, la description, le site Web, LinkedIn, les notes et ce que l’organisation représente pour vous. Vos modifications sont conservées. Videz un champ pour réutiliser la valeur trouvée lors de la recherche.
- **Mauvaise entreprise, effacer les détails**, dans **Modifier**, si la mauvaise entreprise a été sélectionnée.
- **Rechercher à nouveau**, qui s’affiche une fois les détails effacés, permet d’obtenir des informations à jour.
