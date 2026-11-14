---
title: Pages web suivies
area: connections
summary: Une page web que vous suivez. Une tâche seulement quand quelque chose d’important y change.
covers: connector:web_page
code: connectors/web_page.py
---
## Ce qu’elle lit

Le texte d’une page web publique par connexion, toutes les quelques heures et au plus une fois par heure. Elle laisse de côté les menus, les pieds de page, les bandeaux de cookies et les publicités. Quand le texte a changé, The Machine regarde ce qui a changé et ne crée une tâche que si cela compte, comme un nouveau prix ou une politique modifiée. Les dates, les compteurs et les petites reformulations ne donnent jamais de tâche. Une page inchangée ne coûte rien.

Elle consulte d’abord le robots.txt du site et laisse la page tranquille si le site dit non. Les pages derrière une connexion ou construites uniquement en JavaScript ne peuvent pas être suivies.

## Ce qu’elle peut faire

Rien. Elle lit seulement la page.

## La connecter

1. Dans le tableau de bord, ouvrez **Connexions**, puis **Autres**, et choisissez Page web. Ou lancez `assistant connect web_page`.
2. Collez l’adresse de la page.

Ou demandez dans votre chat : « Suis cette page pour les changements de prix » avec son adresse. Demandez quelles pages vous suivez, ou d’arrêter d’en suivre une.

## La retirer

Dans le tableau de bord : **Connexions**, ouvrez la page, **Détails**, puis **Déconnecter**. Ou demandez à votre chat d’arrêter de la suivre.
