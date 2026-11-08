---
title: La connexion maison de ton navigateur
area: troubleshooting
summary: Fais passer le navigateur de ta Machine hébergée par ton internet à la maison avec Tailscale, pour que les sites acceptent ses connexions.
code: browser_login.py
site: Tailscale, Sign in to Tailscale, Use this exit node, Open it in Tailscale, Test it, Sign in again, Stop using it, Sign it out of Tailscale too
keywords: tailscale, exit node, home internet, ip address, cloudflare, linkedin
order: 4
---
Certains sites, comme LinkedIn, X et les sites derrière une vérification Cloudflare, refusent les connexions d'un navigateur dans le cloud. Ta page de configuration peut faire passer le navigateur de ta Machine hébergée par ton internet à la maison, avec Tailscale. C'est gratuit, ça prend environ 10 minutes, et presque tout se fait tout seul.

## Le configurer

1. Sur ta page de configuration, au navigateur de ta Machine, choisis **Tailscale** et appuie sur **Se connecter à Tailscale**. Connecte-toi, ou crée un compte gratuit là-bas.
2. Installe Tailscale sur un ordinateur à la maison qui reste allumé, et connecte-toi avec le même compte. Pas un téléphone : il se met en veille.
3. Fais de cet ordinateur un nœud de sortie. La page de configuration montre le menu pour son système. Sous Linux, lance `sudo tailscale set --advertise-exit-node`.
4. Appuie sur **L'ouvrir dans Tailscale** et autorise-le : Machine settings, Edit route settings, Use as exit node, Save. Dans le même menu, choisis Disable key expiry.

La page de configuration coche chaque étape toute seule. Avec un seul nœud de sortie, ton navigateur l'utilise tout de suite. S'il y en a plusieurs, choisis-en un et appuie sur **Utiliser ce nœud de sortie**.

## Vérifier

Appuie sur **Tester**. La page montre où le web voit ton navigateur : ta ville et ton fournisseur internet.

## Quand ton ordinateur à la maison est éteint

Ton navigateur sort alors directement depuis ta Machine, et repasse par chez toi dès que l'ordinateur est rallumé. Déconnecté de Tailscale ? Appuie sur **Se reconnecter**. Tailscale déconnecte les appareils après 6 mois, sauf si key expiry est désactivé. La page de configuration montre la date.

## Arrêter

Appuie sur **Ne plus l'utiliser** pour repasser en direct. **Le déconnecter aussi de Tailscale** déconnecte aussi le navigateur de ta Machine de Tailscale. La console d'administration de Tailscale l'affiche alors comme Expired, et tu peux l'y supprimer.
