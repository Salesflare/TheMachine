---
title: La connexion maison de votre navigateur
area: troubleshooting
summary: Faites passer le navigateur de votre Machine hébergée par votre internet à la maison avec Tailscale, pour que les sites acceptent ses connexions.
code: browser_login.py
site: Tailscale, Sign in to Tailscale, Use this exit node, Open it in Tailscale, Test it, Sign in again, Stop using it, Sign it out of Tailscale too
keywords: tailscale, exit node, home internet, ip address, cloudflare, linkedin
order: 4
translated: 9935ac3c09fa5c00
---
Certains sites, comme LinkedIn, X et les sites derrière une vérification Cloudflare, refusent les connexions d’un navigateur dans le cloud. Votre page de configuration peut faire passer le navigateur de votre Machine hébergée par votre internet à la maison, avec Tailscale. C’est gratuit, ça prend environ 10 minutes, et presque tout se fait tout seul.

## Le configurer

1. Sur votre page de configuration, au navigateur de votre Machine, choisissez **Tailscale** et appuyez sur **Se connecter à Tailscale**. Connectez-vous, ou créez un compte gratuit là-bas.
2. Installez Tailscale sur un ordinateur à la maison qui reste allumé, et connectez-vous avec le même compte. Pas un téléphone : il se met en veille.
3. Faites de cet ordinateur un nœud de sortie. La page de configuration montre le menu pour son système. Sous Linux, lancez `sudo tailscale set --advertise-exit-node`.
4. Appuyez sur **L’ouvrir dans Tailscale** et autorisez-le : Machine settings, Edit route settings, Use as exit node, Save. Dans le même menu, choisissez Disable key expiry.

La page de configuration coche chaque étape toute seule. Avec un seul nœud de sortie, votre navigateur l’utilise tout de suite. S’il y en a plusieurs, choisissez-en un et appuyez sur **Utiliser ce nœud de sortie**.

## Vérifier

Appuyez sur **Tester**. La page montre où le web voit votre navigateur : votre ville et votre fournisseur internet.

## Quand votre ordinateur à la maison est éteint

Votre navigateur sort alors directement depuis votre Machine, et repasse par chez vous dès que l’ordinateur est rallumé. Déconnecté de Tailscale ? Appuyez sur **Se reconnecter**. Tailscale déconnecte les appareils après 6 mois, sauf si key expiry est désactivé. La page de configuration montre la date.

## Arrêter

Appuyez sur **Ne plus l’utiliser** pour repasser en direct. **Le déconnecter aussi de Tailscale** déconnecte aussi le navigateur de votre Machine de Tailscale. La console d’administration de Tailscale l’affiche alors comme Expired, et vous pouvez l’y supprimer.
