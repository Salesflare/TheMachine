---
title: Détails des organisations
area: graph
summary: Secteur, taille, lieu et logo à côté de chaque organisation, recherchés à partir de son adresse web.
covers: enrichment
code: enrichment.py, graph.py, dashboard.html
order: 5
translated: a759d8e2c6274792
---
## D’où ils viennent

- Sur une Machine hébergée, les détails des organisations sont recherchés pour vous, gratuitement.
- Sur votre propre ordinateur, c’est désactivé jusqu’à ce que vous ajoutiez une clé pour un service de recherche que vous utilisez, comme Apollo, People Data Labs ou Hunter. Voir le [guide de configuration](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).

Seule l’adresse web d’une organisation est envoyée, jamais vos messages ni les personnes que vous y connaissez. Quelques-unes sont recherchées à la fois, 50 par jour au maximum, et actualisées tous les 90 jours. Les personnes ont leur propre recherche : voir [Poste et photo](people.md#job-title-and-photo). Les hébergeurs partagés et les fournisseurs de messagerie, comme google.com, sites.google.com ou gmail.com, ne sont jamais recherchés : ce n’est le site d’aucune entreprise en particulier.

Quand la recherche ne donne pas de logo, ou qu’il n’y a pas de recherche, le logo vient du site de l’organisation elle-même : l’icône que nomme sa page d’accueil. Il est enregistré sur votre Machine, ainsi aucun service de logos ne sait avec qui vous êtes en contact. Un site sans icône est de nouveau interrogé après 30 jours. Si la recherche a trouvé l’organisation mais pas de logo, elle est refaite une fois après une semaine, et le logo qu’elle trouve alors remplace l’icône du site. Les petits emplacements, comme la ligne d’une tâche, gardent l’icône carrée.

Quand la recherche les donne, jusqu’à 5 spécialités de l’organisation s’affichent sous sa description, et la liste des organisations peut être filtrée par l’une d’elles : **Filtrer**, puis **Spécialité**. Quand la recherche d’une personne apporte les détails de son entreprise, ils complètent aussi l’organisation, qui n’a alors pas besoin de sa propre recherche. Les détails recherchés il y a moins de 90 jours restent tels quels.

## Corriger une erreur

Sur la page de l’organisation :

- **Modifier** pour changer le nom, le secteur, la taille, le lieu, l’année de création, la description, le site web, LinkedIn et ce qu’elle représente pour vous. Vos modifications restent. Videz un champ pour reprendre la valeur trouvée.
- **Mauvaise entreprise, effacer les détails** si elle a choisi la mauvaise entreprise.
- **Rechercher à nouveau** pour récupérer des détails à jour.
