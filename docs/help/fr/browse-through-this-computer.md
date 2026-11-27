---
title: Naviguer via l’application de bureau
area: troubleshooting
summary: Faites passer le navigateur de votre Machine hébergée par l’ordinateur où tourne l’application de bureau, pour que les sites voient votre propre connexion Internet.
code: desktop/src/exit.rs, desktop/src/settings.rs
keywords: desktop app, exit node, home internet, office, ip address, linkedin, sign in, proxy
order: 5
translated: 6da69c78d7e60574
---
Certains sites, comme LinkedIn, refusent les connexions depuis un navigateur dans le cloud. Si vous êtes connecté à l’[application de bureau](desktop-app.md), le navigateur de votre Machine hébergée peut passer par cet ordinateur. Les sites voient alors la connexion Internet de votre domicile ou de votre bureau, et non celle d’un centre de données.

## Activer cette option

Cette option est activée par défaut dès que votre Machine en dispose. Dans les **Paramètres** de l’application de bureau, le bouton est **Autoriser ma Machine à naviguer via cet ordinateur**. Désactivez-le pour que le navigateur de votre Machine navigue à nouveau directement, sans attendre.

Pendant que le navigateur de votre Machine l’utilise, l’encadré du robot et l’icône de l’application dans la barre des menus ou la barre des tâches affichent **Votre Machine navigue via cet ordinateur**.

## Ce qui transite par cet ordinateur

Seul le navigateur de votre Machine, vers des sites Web : les ports 80 et 443 sur des adresses Internet publiques. L’application ne se connecte jamais à cet ordinateur, à votre réseau domestique ou professionnel, ni à d’autres adresses privées. Elle n’ouvre aucun port sur votre ordinateur. Le débit est limité à 4 Mo/s en téléchargement, 1 Mo/s en envoi et 2 Go par jour.

## Quand l’ordinateur est éteint

Le navigateur de votre Machine navigue directement depuis votre Machine, puis repasse par l’ordinateur dès que l’application fonctionne à nouveau.
