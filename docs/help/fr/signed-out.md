---
title: Déconnecté d’un site
area: troubleshooting
summary: LinkedIn ou X a déconnecté votre Machine. Reconnectez-la, une fois ou pour de bon.
covers: 
code: browser_login.py, dashboard.html, dashboard/connections-signin.js
order: 2
---
Des sites comme LinkedIn et X sont lus dans le navigateur de votre Machine. Parfois, un site la déconnecte.

## Se reconnecter

La source dans **Connexions**, et le haut de vos Tâches, indiquent qu’elle est déconnectée. Appuyez sur **Se reconnecter** et connectez-vous dans une petite fenêtre du tableau de bord.

Cochez **Enregistrer pour la prochaine fois** en vous connectant. La prochaine fois que le site déconnecte votre Machine, elle se reconnecte en un geste. Le mot de passe reste chiffré sur votre Machine, et l’IA ne le voit jamais.

## Mots de passe et codes

Tapez vous-même les mots de passe. Les codes de validation en deux étapes, c’est aussi à vous de les saisir.

Les identifiants enregistrés se trouvent sous **Connexions**, **Connexions aux sites**. **Oublier** en supprime un.

## Si le site refuse ou demande une vérification anti-robot

LinkedIn, X et les sites derrière une vérification Cloudflare refusent souvent les connexions depuis un navigateur dans le cloud. Sur une Machine hébergée, la connexion affiche alors **Se connecter depuis votre connexion à domicile**. Cela ouvre votre page de configuration, où le navigateur de votre Machine peut sortir par votre internet à domicile avec Tailscale, ou par votre propre proxy. Connectez-vous ensuite à nouveau.

Sur votre propre ordinateur, ce n’est pas nécessaire : son navigateur est déjà chez vous.
