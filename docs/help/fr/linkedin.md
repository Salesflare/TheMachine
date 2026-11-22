---
title: LinkedIn
area: connections
summary: Vos messages LinkedIn, lus dans le navigateur de votre Machine, connecté à votre compte. Les réponses ne sont envoyées qu’après votre approbation.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py, linkedin_connections.py
site: Connect, More sources, Remove
translated: bc67fbc21c77a97a
---
## Ce qu’elle lit

Vos messages LinkedIn. Elle les lit de temps à autre, pendant vos heures d’éveil, dans le navigateur de votre Machine, connecté à votre compte. Elle ne marque aucun message comme lu. Les conversations que vous avez archivées et les demandes de message sont aussi prises en compte, mais pas les spams.

## Intitulés de poste et entreprises

Elle met aussi à jour les intitulés de poste et les entreprises de vos relations LinkedIn qui figurent déjà dans votre Graph, à partir de votre liste **Relations**. Elle n’ouvre pas leurs profils et n’ajoute personne. Quand l’intitulé de poste ou l’entreprise d’une personne change, sa chronologie l’indique, par exemple : « Maintenant responsable des ventes chez Acme, auparavant responsable commerciale chez Acme ».

L’intitulé vient de son titre de profil, par exemple « Responsable des ventes chez Acme » ou « Vice-président des ventes et de la stratégie », jamais d’un slogan. Elle retrouve les personnes grâce au lien vers leur profil, ou à leur nom et à leur entreprise. Si aucune entreprise ne permet de faire la comparaison, un nom complet porté par une seule personne dans votre Graph suffit. Leur page indique aussi depuis quand vous êtes en relation.

Elle lit les pages très lentement : une à la fois, à quelques minutes d’intervalle, quelques dizaines par jour, et seulement pendant la journée. Il faut environ quatre jours pour traiter 3 000 relations. Si LinkedIn s’y oppose, elle s’arrête jusqu’au lendemain.

## Ce qu’elle peut envoyer

Une réponse à un message ou un nouveau message à un profil que vous indiquez, uniquement après que vous l’avez approuvé dans vos tâches. Jusque-là, elle ne rédige que des brouillons.

LinkedIn ne propose pas de méthode officielle pour cela. La lecture et l’envoi occasionnel d’un message que vous avez approuvé ne devraient très probablement pas poser de problème ; les envois massifs ou automatisés peuvent entraîner le blocage d’un compte.

## La connecter

1. Dans le tableau de bord, ouvrez **Connexions**, puis **Chat**, et choisissez LinkedIn.
2. Choisissez **Travail** (avec son entreprise) ou **Perso**, puis appuyez sur **Connecter**.
3. Appuyez sur **Se connecter à LinkedIn** et connectez-vous dans le navigateur de votre Machine. La connexion se fait automatiquement une fois que vous êtes connecté.

Sur une Machine hébergée, vous pouvez aussi utiliser votre page de configuration sur app.themachine.computer/setup : accédez à **Plus de sources**, ouvrez LinkedIn, connectez-vous quand la page vous le demande, puis appuyez sur **Connecter**. Sur votre propre ordinateur, `assistant connect linkedin` fait la même chose dans un terminal.

Un deuxième compte LinkedIn dispose de son propre navigateur. Si LinkedIn déconnecte votre Machine, consultez [Déconnectée d’un site](signed-out.md).

## Si LinkedIn demande un code

LinkedIn envoie souvent un code par e-mail la première fois que votre Machine se connecte. Saisissez-le dans la fenêtre de connexion, sous **Code**, puis appuyez sur **Se connecter**. La page reste affichée pendant que vous saisissez le code.

Si LinkedIn revient au début, ou si rien ne se passe pendant deux minutes, attendez une minute, puis appuyez sur **Réessayer**. Si LinkedIn affiche une vérification anti-robot, terminez-la dans le navigateur de votre Machine.

## La retirer

- Dans le tableau de bord : ouvrez **Connexions**, puis LinkedIn, appuyez sur **Détails**, puis sur **Déconnecter**. Elle cesse de lire vos messages. Les données déjà importées restent.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté de LinkedIn sur votre page de configuration.

## La déconnecter de LinkedIn

Dans LinkedIn, ouvrez **Paramètres**, **Connexion et sécurité**, puis **Où vous êtes connecté**, et déconnectez la session du navigateur de votre Machine.
