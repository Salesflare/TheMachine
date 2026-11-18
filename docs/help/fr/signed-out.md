---
title: Déconnexion d’un site
area: troubleshooting
summary: LinkedIn ou X a déconnecté votre Machine. Reconnectez-la, ponctuellement ou pour de bon.
covers:
code: browser_login.py, login_import.py, dashboard.html, dashboard/connections-signin.js, dashboard/connections-logins.js, dashboard/connections-login-import.js
order: 2
translated: 9a9b91270954c031
---
Les sites comme LinkedIn et X s’ouvrent dans le navigateur de votre Machine. Il arrive qu’un site déconnecte votre Machine.

## Se reconnecter

Dans **Connexions** et en haut de vos tâches, un message indique que votre Machine est déconnectée. Cliquez sur **Connectez-vous ici** et connectez-vous dans une petite fenêtre du tableau de bord.

Cochez **Enregistrer pour la prochaine fois** pour vous reconnecter en un clic si cela se reproduit. Le mot de passe reste chiffré sur votre Machine et l’IA ne le voit jamais. Si vous avez plusieurs comptes sur un même site, **Enregistrer sous** vous permet de nommer ce compte (Travail, Personnel). Une boîte de dialogue vous demande lequel utiliser si la tâche ne le précise pas.

## Mots de passe et codes

Saisissez vous-même vos mots de passe. Vous devez aussi saisir vous-même les codes de vérification en deux étapes.

Les identifiants enregistrés se trouvent dans **Connexions**, sous **Connexions aux sites**. **Oublier** en supprime un. **Importer** permet de les importer depuis un gestionnaire de mots de passe, à partir de sa page d’exportation ouverte dans le navigateur de votre Machine ou d’un fichier d’exportation.

## Si le site refuse la connexion ou demande une vérification anti-robot

LinkedIn, X et les sites protégés par une vérification Cloudflare refusent souvent les connexions depuis un navigateur dans le cloud. Sur une Machine hébergée, l’option **Se connecter depuis votre connexion à domicile** s’affiche alors. Elle ouvre votre page de configuration, où le navigateur de votre Machine peut accéder à Internet via votre connexion à domicile avec Tailscale, ou via votre propre proxy. Réessayez ensuite de vous connecter.

Sur votre propre ordinateur, vous n’en avez pas besoin : son navigateur est déjà sur votre réseau domestique.
