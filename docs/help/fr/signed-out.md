---
title: Déconnectée d’un site
area: troubleshooting
summary: LinkedIn ou X a déconnecté votre Machine. Reconnectez-la, une fois ou définitivement.
covers:
code: browser_login.py, login_import.py, dashboard.html, dashboard/connections-signin.js, dashboard/connections-logins.js
order: 2
translated: 060f7ca4f870ad0a
---
Les sites comme LinkedIn et X s’ouvrent dans le navigateur de votre Machine. Il arrive qu’un site la déconnecte.

## Se reconnecter

**Connexions** et le haut de vos tâches indiquent qu’elle est déconnectée. Appuyez sur **Connectez-vous ici**, puis connectez-vous dans une petite fenêtre sur le tableau de bord.

Cochez **Enregistrer pour la prochaine fois** pour vous reconnecter d’un seul geste si cela se reproduit. Le mot de passe reste chiffré sur votre Machine et l’IA ne le voit jamais. Si vous avez plusieurs comptes sur un même site, **Enregistrer sous** permet de nommer ce compte (Travail, Personnel). La boîte de dialogue vous demande lequel utiliser si la tâche ne le précise pas.

## Mots de passe et codes

Saisissez vous-même vos mots de passe. Vous devez aussi saisir vous-même les codes de validation en deux étapes.

Les identifiants enregistrés se trouvent dans **Connexions**, sous **Connexions aux sites**. **Oublier** en supprime un. **Importer** permet de les importer depuis un gestionnaire de mots de passe.

## Si le site refuse la connexion ou demande de vérifier que vous n’êtes pas un robot

LinkedIn, X et les sites protégés par une vérification Cloudflare refusent souvent les connexions depuis un navigateur dans le cloud. Sur une Machine hébergée, l’écran de connexion affiche alors **Se connecter depuis votre connexion à domicile**. Cette option ouvre votre page de configuration, où le navigateur de votre Machine peut accéder à Internet via votre connexion à domicile avec Tailscale, ou via votre propre proxy. Reconnectez-vous ensuite.

Sur votre propre ordinateur, vous n’en avez pas besoin : son navigateur utilise déjà votre connexion à domicile.
