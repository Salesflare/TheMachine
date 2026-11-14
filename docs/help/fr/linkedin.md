---
title: LinkedIn
area: connections
summary: Vos messages LinkedIn, lus dans le navigateur de votre Machine où vous êtes connecté. Les réponses ne sont envoyées qu’après votre approbation.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py, linkedin_connections.py
site: Connect, More sources, Remove
translated: 850b91f79b9e23fc
---
## Ce que la Machine lit

Vos messages LinkedIn. La Machine les lit de temps à autre, pendant vos heures d’éveil, dans son propre navigateur où vous êtes connecté. Elle ne marque aucun message comme lu. Les conversations que vous avez archivées et les demandes de message sont aussi prises en compte. Les spams sont exclus.

## Titres et entreprises

La Machine tient aussi à jour les titres et les entreprises de vos contacts LinkedIn déjà présents dans votre Graph, à partir de votre liste Connexions. Elle n’ouvre pas leurs profils et n’ajoute personne. Quand le titre ou l’entreprise d’une personne change, sa chronologie l’indique, par exemple : « Maintenant Head of Sales chez Acme, auparavant Sales Lead chez Acme ».

Le titre vient de son titre de profil, par exemple « Head of Sales chez Acme » ou « VP Sales and Strategy », jamais d’un slogan. La Machine retrouve les personnes grâce au lien vers leur profil, ou à leur nom et à leur entreprise. Si aucune entreprise ne permet de faire la comparaison, il suffit que leur nom complet soit celui d’une seule personne dans votre Graph. Leur page indique aussi depuis quand vous êtes en relation.

La lecture est très lente : une page à la fois, à quelques minutes d’intervalle, quelques dizaines de pages par jour, et seulement pendant la journée. Il faut environ quatre jours pour traiter quelque 3 000 contacts. Si LinkedIn bloque la Machine, elle s’arrête jusqu’au lendemain.

## Ce qu’elle peut envoyer

Une réponse à un message ou un nouveau message à un profil que vous indiquez, et seulement après votre approbation dans la tâche. D’ici là, la Machine ne fait que rédiger des brouillons.

LinkedIn ne propose pas de méthode officielle pour cela. La lecture et l’envoi occasionnel d’un message que vous avez approuvé ne devraient pas poser de problème. En revanche, l’envoi massif ou automatisé peut entraîner le blocage d’un compte.

## Connecter LinkedIn

Sur une Machine hébergée :

1. Ouvrez votre page de configuration sur app.themachine.computer/setup, puis allez dans **Plus de sources**.
2. Ouvrez LinkedIn, connectez-vous à LinkedIn dans le navigateur de votre Machine lorsqu’elle vous le demande, puis appuyez sur **Se connecter**.

Sur votre propre ordinateur :

1. Dans le tableau de bord, ouvrez **Connexions**, puis **Chat**, et choisissez LinkedIn.
2. Choisissez **Travail** (avec son entreprise) ou **Perso**, puis appuyez sur **Se connecter**.
3. Appuyez sur **Se connecter à LinkedIn**, puis connectez-vous dans le navigateur de votre Machine. La connexion se fait automatiquement une fois connecté.

Vous pouvez aussi exécuter `assistant connect linkedin`.

Un deuxième compte LinkedIn dispose de son propre navigateur. Si LinkedIn déconnecte votre Machine, consultez [Déconnecté d’un site](signed-out.md).

## Si LinkedIn vous demande un code

La première fois que votre Machine se connecte, LinkedIn envoie souvent un code par e-mail. Saisissez-le dans la fenêtre de connexion, sous **Code**, puis appuyez sur **Se connecter**. La page reste affichée pendant que vous saisissez le code.

Si LinkedIn revient au début ou si rien ne se passe pendant deux minutes, attendez une minute, puis appuyez sur **Réessayer**. Si LinkedIn affiche une vérification antirobot, effectuez-la dans le navigateur de votre Machine.

## Retirer LinkedIn

- Dans le tableau de bord : ouvrez **Connexions**, puis LinkedIn, **Détails**, et enfin **Déconnecter**. La lecture s’arrête. Les informations déjà importées restent.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté de LinkedIn sur votre page de configuration.

## Déconnecter votre session sur LinkedIn

Dans LinkedIn, ouvrez Paramètres, Connexion et sécurité, Où vous êtes connecté, puis déconnectez la session du navigateur de votre Machine.
