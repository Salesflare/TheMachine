---
title: Déconnexion d’un site
area: troubleshooting
summary: LinkedIn ou X a déconnecté votre Machine. Reconnectez-la, une fois ou pour de bon.
covers:
code: browser_login.py, dashboard.html, dashboard/connections-signin.js
order: 2
translated: 96c09e57cd3dca62
---
Les sites comme LinkedIn et X s’ouvrent dans le navigateur de votre Machine. Parfois, un site la déconnecte.

## Se reconnecter

Dans **Connexions** et en haut de vos tâches, vous voyez que votre Machine est déconnectée. Appuyez sur **Connectez-vous ici**, puis connectez-vous dans une petite fenêtre sur le tableau de bord.

Cochez **Enregistrer pour la prochaine fois** pour vous reconnecter en un clic si cela se reproduit. Le mot de passe reste chiffré sur votre Machine, et l’IA ne le voit jamais.

## Mots de passe et codes

Saisissez vous-même vos mots de passe. Vous devez aussi saisir vos codes de validation en deux étapes.

Vos identifiants enregistrés se trouvent dans **Connexions**, sous **Connexions aux sites**. **Oublier** permet d’en supprimer un.

## Si le site refuse la connexion ou demande une vérification anti-robot

LinkedIn, X et les sites protégés par une vérification Cloudflare refusent souvent les connexions depuis un navigateur dans le cloud. Sur une Machine hébergée, l’option **Se connecter depuis votre connexion à domicile** s’affiche alors. Elle ouvre la page de configuration, où le navigateur de votre Machine peut accéder à Internet via votre connexion à domicile avec Tailscale, ou via votre propre proxy. Reconnectez-vous ensuite.

Sur votre propre ordinateur, ce n’est pas nécessaire : son navigateur est déjà chez vous.
