---
title: Faire, et ce qui est envoyé
area: cards
summary: Faire prépare le travail. Rien n’est envoyé, payé ou modifié avant que vous approuviez cette étape.
covers: do-it
code: dashboard.html, next_actions.py, assistant.py
order: 2
translated: 81798e7a2a6fa66e
---
## Ce que fait Faire

**Faire** demande à votre Machine de préparer la tâche : rédiger une réponse, faire des recherches ou remplir un formulaire. Elle utilise vos propres comptes et son propre navigateur, comme vous le feriez.

Pendant qu’elle travaille dans son navigateur, la tâche et son chat affichent cette page en direct, même entre les étapes, jusqu’à ce que le travail soit terminé. Cliquez sur l’image pour ouvrir le navigateur. Dans la tâche, elle s’ouvre en plus grand, avec **Arrêter** : un seul appui interrompt immédiatement cette exécution.

Avant un suivi ou un transfert, elle vérifie s’il y a de nouvelles réponses, y compris celles d’un collègue. Si la tâche a déjà été traitée, elle vous le dit. Si elle a modifié un document ou une page, la tâche contient un lien vers celui-ci.

Quand une tâche complexe aboutit sur un site ou dans un processus, votre Machine conserve les étapes sous forme de compétence, sans aucune information personnelle. Les tâches suivantes sur ce site s’en servent comme guide, jamais comme autorisation : l’envoi ou le paiement attend toujours votre accord. Ces compétences apparaissent dans **Paramètres > Compétences**, sous **Appris lors d’une tâche**.

## Rien n’est envoyé sans votre accord

- Une réponse est renvoyée sous forme de brouillon. **Vérifier et envoyer** permet de l’ouvrir et de la modifier. Elle est envoyée uniquement lorsque vous appuyez sur **Envoyer maintenant**.
- Pour deux e-mails ou plus dans une même tâche, un bouton dans le chat permet de tous les vérifier. Ils s’affichent l’un après l’autre avec **Suivant**, et la dernière étape les envoie tous. Chacun n’apparaît comme envoyé qu’une fois qu’il l’a été.
- Un e-mail s’affiche tel qu’il apparaîtra, avec le texte en gras, les listes et les liens. Un message Slack ou un message de chat est en texte brut.
- **Demander des modifications** dans la même fenêtre : indiquez ce qu’il faut modifier et votre Machine reprend le brouillon.
- Une réponse répond au dernier e-mail du fil, et la source de la tâche ouvre cet e-mail.
- Une étape qui valide une action, comme envoyer un formulaire, payer ou réserver, attend votre confirmation ou que vous le demandiez dans le chat. Confirmer une étape laisse les autres en attente : la tâche ne se termine que lorsque toutes les étapes sont faites.
- La tâche et son chat indiquent ce qu’une telle étape enverra avant que vous appuyiez dessus. Une invitation d’agenda affiche son titre, son horaire, ses invités et indique si un lien de réunion est ajouté.
- Les agendas connectés sont pris en compte lors de la recherche d’un horaire : la tâche consulte vos réunions pour ces journées avant de vous proposer des horaires.
- Dans le chat d’une tâche, un brouillon n’est jamais envoyé dans le même message que celui qui l’a rédigé.
- Tant que vous n’avez pas approuvé, la tâche reste dans **Pour vous**, avec le statut **Préparée**, et la liste précise que rien ne sera envoyé avant votre approbation. **Préparée** signifie qu’un brouillon ou un résultat est prêt à être approuvé. Si le travail se termine sans résultat parce qu’il a besoin de vous, par exemple pour une décision, une information manquante, une connexion ou un choix, la tâche affiche plutôt **Vous attend**, avec une phrase indiquant ce dont elle a besoin. C’est aussi le cas si elle s’est contentée de répondre ou d’expliquer ("Réponse fournie. Rien n’a encore été fait."), avec **Faire** en premier. Il en va de même pour sa notification et le récap du matin. La tâche indique qu’un brouillon a été envoyé uniquement après son envoi.
- Les longs brouillons affichent leurs 3 premières lignes. **Afficher plus**, ou un appui sur le texte, permet d’ouvrir la suite ; **Vérifier et envoyer** affiche toujours le texte en entier.

Selon la source, elle peut envoyer un e-mail, un message direct Slack, ou un message WhatsApp, Telegram, LinkedIn ou X. L’article de chaque connexion indique ce qu’elle peut envoyer.

## Modifier un e-mail

- Utilisez les boutons au-dessus du texte, ou `Ctrl B` pour le gras, `Ctrl I` pour l’italique et `Ctrl K` pour un lien (`⌘` sur Mac). Des boutons permettent aussi de créer une liste à puces ou une liste numérotée.
- Un lien doit avoir une adresse commençant par https://. Le texte collé est inséré en texte brut, sans ses couleurs ni ses images.
- Les éléments de mise en forme incompatibles avec l’e-mail sont supprimés, et le message affiche le résultat. Appuyez de nouveau sur **Envoyer maintenant** pour l’envoyer.
- L’e-mail est envoyé exactement comme affiché, avec une copie en texte brut pour les applications de messagerie qui n’affichent pas la mise en forme.

## Quand elle ne peut pas

- « Impossible d’envoyer ceci depuis ici. » signifie que vous devez copier le brouillon avec **Copier le brouillon** et l’envoyer vous-même.
- Si le statut **Vous attend** n’est accompagné de rien à envoyer, ouvrir ou lire, la tâche commence par **Répondre** : indiquez ce dont elle a besoin et elle reprend. Si seule vous pouvez effectuer une étape, comme un paiement depuis votre banque, la tâche commence par **Marquer comme fait**.
- **Attend votre aide** signifie qu’elle a une question : **Répondre**. **Bloqué** signifie qu’elle s’est arrêtée sans poser de question ; la tâche en indique la raison.
- Vous avez demandé plusieurs choses ? Chaque question a ses propres choix ou un champ à remplir, parfois prérempli avec votre dernière réponse. **Répondre** les envoie toutes ensemble.
- Quelqu’un vous a demandé des informations ou des fichiers ? La tâche prépare une réponse avec ce qu’elle a trouvé et ne vous demande que le reste.
- Il manque quelque chose que vous seul avez ? La tâche vous le demande et ne prépare que ce qui peut être envoyé sans cet élément, par exemple une réponse confirmant une date. Elle ne prépare pas une réponse qui dit seulement que l’élément arrivera.
- **Réessayer** relance la tâche. **Demander des modifications** permet de demander autre chose. Pour une tâche bloquée, **Réessayer** apparaît en premier, et **Détails** indique ce qu’elle a tenté.
- La tâche est bloquée parce que l’exécution elle-même a échoué ? Après une mise à jour de votre Machine, elle réessaie cette tâche une fois automatiquement.
- Elle réessaie automatiquement une exécution échouée au maximum deux fois. Ensuite, elle attend un nouvel élément, comme un nouveau message ou votre message dans son chat, ou que vous appuyiez sur **Réessayer**.
- Pendant la préparation, la tâche indique en une phrase simple ce que fait votre Machine, par exemple « Lecture des e-mails », « Lecture du PDF » ou « Rédaction du brouillon ». Le détail des étapes reste dans le chat de la tâche.
- Une tâche avec le statut **En préparation…** démarre en quelques secondes. Si elle doit attendre, elle en indique la raison et le délai approximatif, par exemple « Démarrera après la tâche en cours ».
- Une tâche que votre Machine prépare avant que vous le lui demandiez peut attendre pour économiser votre utilisation. **Faire** reste affiché : appuyez dessus pour la démarrer immédiatement, avant les autres tâches. Rien n’est envoyé sans votre accord. Si la limite d’utilisation de votre forfait IA est atteinte, Faire vous l’indique et la tâche démarre lorsque la limite est réinitialisée.
- Un site vous demande de vous connecter : appuyez sur **Se connecter**, ou sur **Ouvrir le navigateur** et connectez-vous depuis celui-ci. La tâche reprend ensuite automatiquement. Si ce n’est pas le cas, appuyez sur **Continuer**.
- Un code envoyé sur votre téléphone ou une autorisation manquante interrompt la tâche. Elle indique ce dont elle a besoin, puis affiche **Continuer** ou **Réessayer**. Si une source n’est pas connectée, comme Slack, **Connecter Slack** apparaît dans la tâche. Elle reprend automatiquement une fois Slack connecté.
