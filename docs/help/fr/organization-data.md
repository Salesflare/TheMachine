---
title: Détails de l’organisation
area: graph
summary: Le secteur, la taille, la localisation et un logo pour chaque organisation, recherchés à partir de son adresse web.
covers: enrichment
code: enrichment.py, graph.py, dashboard.html
order: 5
translated: 1690f417d7a70829
---
## D’où viennent ces informations

- Sur une Machine hébergée, les détails des organisations sont recherchés gratuitement pour vous.
- Sur votre propre ordinateur, cette fonction est désactivée jusqu’à ce que vous ajoutiez une clé pour un service de recherche, comme Apollo, People Data Labs ou Hunter. Consultez le [guide de configuration](https://github.com/Salesflare/TheMachine/blob/main/docs/configuration.md).

Seule l’adresse web de l’organisation est envoyée, jamais vos messages ni les personnes que vous connaissez dans cette organisation. Une Machine hébergée, ou une Machine sur The Machine Network, effectue jusqu’à 1 000 recherches par jour. Dans les autres cas, la limite est de 50. Les informations sont actualisées tous les 90 jours. Les sites partagés et les fournisseurs de messagerie, comme gmail.com, ne font jamais l’objet d’une recherche. Les personnes font l’objet d’une recherche distincte : consultez [Intitulé de poste et photo](people.md#job-title-and-photo).

Si la recherche ne fournit pas de logo, The Machine utilise l’icône indiquée par le site web de l’organisation et l’enregistre sur votre Machine. Aucun service de logos ne sait avec qui vous travaillez. Quand les deux sont disponibles, les petits espaces, comme la ligne d’une tâche, affichent l’icône carrée.

Si la recherche trouve des spécialités, jusqu’à 5 s’affichent sous la description de l’organisation. Vous pouvez aussi filtrer la liste des organisations par spécialité : **Filtrer**, puis **Spécialité**. Quand la recherche d’une personne fournit aussi les détails de son entreprise, ceux-ci complètent ceux de l’organisation, sans qu’une recherche distincte soit nécessaire. Les détails recherchés au cours des 90 derniers jours restent inchangés.

## Corriger une erreur

Sur la page de l’organisation :

- **Modifier** pour changer le nom, le secteur, la taille, la localisation, l’année de fondation, la description, le site web, LinkedIn, les notes et ce que cette organisation représente pour vous. Vos modifications sont conservées. Effacez un champ pour réutiliser la valeur trouvée.
- **Mauvaise entreprise, effacer les détails**, dans **Modifier**, si la mauvaise entreprise a été sélectionnée.
- **Rechercher à nouveau**, affiché une fois les détails effacés, pour obtenir des informations à jour.
