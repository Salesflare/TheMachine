---
title: L’action Faire et ce qui est envoyé
area: cards
summary: Faire prépare le travail. Rien n’est envoyé, payé ni modifié avant que vous approuviez cette étape.
covers: do-it
code: dashboard.html, next_actions.py, assistant.py
order: 2
translated: f6078d1de97851ae
---
## Ce que fait Faire

**Faire** demande à votre Machine de préparer la tâche : rédiger une réponse, faire des recherches, remplir un formulaire. Elle utilise vos comptes et son propre navigateur, comme vous le feriez.

Pendant qu’elle travaille dans son navigateur, la tâche et son chat affichent la page en direct, y compris entre les étapes, jusqu’à ce qu’elle ait terminé. Cliquez sur l’image pour ouvrir le navigateur. Dans la tâche, la page s’affiche en plus grand, avec **Arrêter** : une pression met fin à cette exécution immédiatement.

Avant un suivi ou un transfert, elle vérifie s’il y a de nouvelles réponses, y compris celles d’un collègue. Si la demande a déjà été traitée, la tâche vous l’indique. Si elle a modifié un document ou une page, la tâche contient un lien vers celui-ci.

Quand une tâche difficile aboutit sur un site ou dans un processus, votre Machine conserve les étapes sous forme de compétence, sans les informations personnelles de qui que ce soit. Les tâches suivantes sur ce site s’en servent comme guide, jamais comme autorisation : l’envoi ou le paiement attend toujours votre accord. Elles apparaissent dans **Paramètres > Compétences**, avec la mention **Appris lors d’une tâche**.

Si les étapes d’une compétence ne fonctionnent plus pour trois tâches consécutives, votre Machine la désactive. Elle le restera jusqu’à ce qu’une tâche ultérieure montre ce qui fonctionne maintenant ou que vous la réactiviez.

## Rien n’est envoyé sans votre accord

- Une réponse est préparée sous forme de brouillon. **Vérifier et envoyer** l’ouvre pour que vous puissiez le modifier. Elle n’est envoyée que lorsque vous appuyez sur **Envoyer maintenant**.
- Pour deux e-mails ou plus dans une même tâche, un seul bouton dans le chat permet de tous les vérifier. Ils s’affichent l’un après l’autre avec **Suivant**, et la dernière étape les envoie tous. Chacun n’est indiqué comme envoyé qu’une fois parti.
- Un e-mail s’affiche tel qu’il apparaîtra, avec le texte en gras, les listes et les liens. Un message Slack ou un message de chat est en texte brut.
- **Demander des modifications** dans la même fenêtre : indiquez ce qu’il faut changer et votre Machine refait le brouillon.
- Une réponse répond au dernier e-mail du fil, et la source de la tâche ouvre cet e-mail.
- Une étape qui valide une action, comme envoyer un formulaire, payer ou réserver, attend votre confirmation ou votre demande dans le chat. La confirmation d’une étape laisse les autres en attente : la tâche ne se termine que lorsque toutes les étapes sont terminées.
- La tâche et son chat indiquent ce qu’une telle étape enverra avant que vous appuyiez dessus. Une invitation d’agenda affiche son titre, son horaire, ses invités et précise si un lien de réunion sera ajouté.
- Les agendas connectés sont pris en compte dans la recherche d’un créneau : elle consulte vos réunions pour ces jours avant de vous proposer des horaires.
- Dans le chat d’une tâche, un brouillon n’est jamais envoyé dans le même message que celui qui l’a rédigé.
- Tant que vous n’avez pas approuvé le résultat, la tâche reste dans **Pour vous** avec le statut **Préparée**, et la liste indique une seule fois que rien ne sera envoyé avant votre approbation. **Préparée** signifie qu’un brouillon ou un résultat est prêt à être approuvé. Si le travail se termine sans résultat parce qu’elle a besoin de vous (pour une décision, une information manquante, une connexion ou un choix), la tâche affiche plutôt **Vous attend**, avec une ligne qui précise ce dont elle a besoin. C’est aussi le cas si elle s’est contentée de répondre ou d’expliquer (« Réponse donnée. Rien n’a encore été fait. »), avec **Faire** comme action principale. Il en va de même pour sa notification et le récap du matin. Elle indique qu’un brouillon a été envoyé uniquement après son envoi.
- Un long brouillon affiche ses trois premières lignes. **Afficher plus**, ou une pression sur le texte, ouvre le reste. **Vérifier et envoyer** affiche toujours le brouillon en entier.

Selon la source, elle peut envoyer un e-mail, un message privé Slack, ou un message WhatsApp, Telegram, LinkedIn ou X. L’article de chaque connexion indique ce qu’elle peut envoyer.

## Modifier un e-mail

- Utilisez les boutons au-dessus du texte ou `Ctrl B` pour le gras, `Ctrl I` pour l’italique et `Ctrl K` pour un lien (`⌘` sur Mac). Des boutons permettent aussi de créer une liste à puces ou numérotée.
- Un lien doit pointer vers une adresse commençant par https://. Le texte collé est inséré sans mise en forme, couleurs ni images.
- Les mises en forme incompatibles avec l’e-mail sont d’abord supprimées. Le message affiche ensuite le résultat. Appuyez de nouveau sur **Envoyer maintenant** pour l’envoyer.
- L’e-mail est envoyé exactement comme il s’affiche, avec une copie en texte brut pour les applications de messagerie qui ne prennent pas en charge la mise en forme.

## Si elle ne peut pas continuer

- « Impossible d’envoyer cet élément d’ici. » signifie que vous devez copier le brouillon avec **Copier le brouillon** et l’envoyer vous-même.
- Si **Vous attend** s’affiche alors qu’il n’y a rien à envoyer, à ouvrir ou à lire, la tâche propose **Répondre** : indiquez ce dont elle a besoin et elle reprendra. Si seule une action que vous devez effectuer vous-même est possible, comme un paiement dans votre banque, elle propose **Marquer comme fait**.
- **Attend votre aide** signifie qu’elle a une question : **Répondre**. **Bloqué** signifie qu’elle s’est arrêtée sans poser de question. La tâche vous en indique la raison.
- Vous a-t-on demandé plusieurs choses ? Chaque question propose ses propres choix ou un champ de réponse court, parfois prérempli avec votre dernière réponse. **Répondre** envoie toutes vos réponses à la fois.
- Quelqu’un vous a demandé des informations ou des fichiers ? Elle rédige une réponse à partir de ce qu’elle a trouvé et ne vous demande que ce qui manque.
- Il manque une information que vous seul possédez ? Elle vous la demande et ne rédige que ce qui peut être envoyé sans cette information, comme une réponse pour confirmer une date. Elle ne rédige pas une réponse qui se contente de dire que l’information suivra.
- **Réessayer** relance la tâche. **Demander des modifications** permet de demander autre chose. Pour une tâche bloquée, **Réessayer** est l’action principale, et **Détails** affiche ce qu’elle a tenté.
- Si la tâche est bloquée parce que l’exécution a échoué, votre Machine la relance une fois après sa mise à jour.
- Elle relance automatiquement une exécution échouée deux fois au maximum. Ensuite, elle attend un nouvel élément, comme un nouveau message ou votre réponse dans son chat, ou que vous appuyiez sur **Réessayer**.
- Pendant la préparation, la tâche indique en une phrase simple ce que fait votre Machine, par exemple « Lecture des e-mails », « Lecture du PDF » ou « Rédaction du brouillon ». Les étapes détaillées restent dans le chat de la tâche.
- Une tâche marquée **En préparation…** démarre en quelques secondes. Si elle doit attendre, elle en indique la raison et donne une estimation, par exemple « Démarrera après la tâche en cours ».
- Une tâche préparée par votre Machine avant que vous ne la demandiez peut attendre pour économiser votre consommation. Elle affiche tout de même **Faire** : appuyez dessus pour la lancer immédiatement, avant les autres. Rien n’est envoyé sans votre accord. Si vous avez atteint la limite d’utilisation de votre forfait IA, Faire vous l’indique et la tâche démarre une fois la limite réinitialisée.
- Un site vous demande de vous connecter : appuyez sur **Se connecter**, ou sur **Ouvrir le navigateur** pour vous connecter depuis celui-ci. Elle reprend ensuite automatiquement. Si ce n’est pas le cas, appuyez sur **Continuer**.
- Un code envoyé sur votre téléphone ou une autorisation manquante l’arrête. La tâche indique ce dont elle a besoin, puis propose **Continuer** ou **Réessayer**. Si une source n’est pas connectée, comme Slack, **Connecter Slack** apparaît dans la tâche. Elle reprend automatiquement une fois Slack connecté.
