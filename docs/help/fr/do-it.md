---
title: Faire et ce qui est envoyé
area: cards
summary: Faire prépare le travail. Rien n’est envoyé, payé ni modifié avant que vous approuviez cette étape.
covers: do-it
code: dashboard.html, next_actions.py, assistant.py
order: 2
translated: 9351ad3d0f79316b
---
## Ce que fait Faire

**Faire** demande à votre Machine de préparer la tâche : rédiger la réponse, faire des recherches, remplir un formulaire. Elle utilise vos propres comptes et son propre navigateur, comme vous le feriez.

Pendant qu’elle travaille dans son navigateur, la tâche et son chat affichent cette page en direct, même entre les étapes, jusqu’à ce qu’elle ait terminé. Cliquez sur l’image pour ouvrir le navigateur. Dans la tâche, la page s’ouvre en plus grand, avec **Arrêter** : une seule pression met immédiatement fin à cette exécution.

Avant un suivi ou un transfert, elle vérifie s’il y a de nouvelles réponses, y compris celles d’un collègue. Si la tâche a déjà été traitée, elle vous l’indique. Si elle a modifié un document ou une page, la tâche contient un lien vers celui-ci.

Quand votre Machine réussit une tâche complexe sur un site ou dans un processus, elle enregistre les étapes sous forme de compétence, sans les informations propres à qui que ce soit. Les tâches suivantes sur ce site utilisent ces étapes comme guide, jamais comme autorisation : l’envoi ou le paiement attend toujours votre accord. Ces compétences apparaissent dans **Paramètres > Compétences**, sous **Appris lors d’une tâche**.

## Rien n’est envoyé sans votre accord

- Une réponse revient sous forme de brouillon. **Vérifier et envoyer** l’ouvre, prête à être modifiée. Elle n’est envoyée que lorsque vous appuyez sur **Envoyer maintenant**.
- S’il y a au moins deux e-mails dans une tâche, un bouton dans son chat permet de tous les vérifier. Ils s’affichent l’un après l’autre avec **Suivant**. La dernière étape les envoie tous. Chaque e-mail n’apparaît comme envoyé qu’une fois qu’il l’a été.
- Un e-mail s’affiche tel qu’il apparaîtra, avec le gras, les listes et les liens. Un message Slack ou un message de chat est en texte brut.
- **Demander des modifications** dans la même fenêtre : indiquez ce qu’il faut modifier et votre Machine refait le brouillon.
- Une réponse répond au dernier e-mail du fil, et la source de la tâche ouvre cet e-mail.
- Une étape qui valide une action, comme envoyer, payer ou réserver, attend votre confirmation ou que vous le demandiez dans le chat. La confirmation d’une étape laisse les autres en attente : la tâche ne se termine que lorsque toutes les étapes sont terminées.
- La tâche et son chat montrent ce qu’une telle étape enverra avant que vous appuyiez dessus. Une invitation d’agenda indique son titre, l’heure, les invités et si un lien de réunion est ajouté.
- Les agendas connectés sont pris en compte lors de la recherche d’un créneau : elle consulte vos réunions pour ces jours-là avant de proposer des horaires.
- Dans le chat d’une tâche, un brouillon n’est jamais envoyé dans le même message que celui qui l’a rédigé.
- Tant que vous n’avez pas donné votre accord, la tâche reste sous **Pour vous** avec le statut **Préparée**, et la liste indique une fois que rien ne sera envoyé avant votre accord. Si elle a encore besoin de vous, son statut est **Vous attend**. Elle indique qu’un brouillon a été envoyé uniquement une fois que c’est fait.
- Un long brouillon affiche ses 3 premières lignes. **Afficher plus**, ou une pression sur le texte, ouvre le reste. **Vérifier et envoyer** affiche toujours le texte en entier.

Selon la source, elle peut envoyer un e-mail, un message privé Slack, ou un message WhatsApp, Telegram, LinkedIn ou X. L’article de chaque connexion indique ce qu’elle peut envoyer.

## Modifier un e-mail

- Utilisez les boutons au-dessus du texte, ou `Ctrl B` pour le gras, `Ctrl I` pour l’italique et `Ctrl K` pour un lien (`⌘` sur Mac). Il y a aussi des boutons pour les listes à puces et numérotées.
- Un lien doit commencer par https://. Le texte collé est en texte brut, sans ses couleurs ni ses images.
- Les mises en forme incompatibles avec les e-mails sont d’abord supprimées, et le message affiche le résultat. Appuyez à nouveau sur **Envoyer maintenant** pour l’envoyer.
- L’e-mail est envoyé exactement comme il apparaît, avec une copie en texte brut pour les applications de messagerie qui n’affichent pas la mise en forme.

## Quand ça ne marche pas

- « Impossible d’envoyer depuis ici. » signifie que vous devez copier le brouillon avec **Copier le brouillon** et l’envoyer vous-même.
- **Attend votre aide** signifie qu’elle a une question : **Répondre**. **Bloqué** signifie qu’elle s’est arrêtée sans poser de question. La tâche en indique la raison.
- Vous avez posé plusieurs questions ? Chacune a ses propres choix ou un champ court, parfois prérempli avec votre réponse précédente. **Répondre** les envoie toutes en même temps.
- Il manque une information que vous seul avez ? Elle vous la demande et ne rédige que ce qui peut être envoyé sans cette information, par exemple une réponse pour confirmer une date. Elle ne rédige pas une réponse qui dit simplement qu’elle arrive.
- **Réessayer** relance la tâche. **Demander des modifications** permet de demander autre chose. Pour une tâche bloquée, **Réessayer** apparaît en premier, et **Détails** affiche ce qu’elle a essayé.
- La tâche est bloquée parce que l’exécution a échoué ? Après la mise à jour de votre Machine, elle réessaie automatiquement cette tâche une fois.
- Pendant la préparation, la tâche indique en une phrase simple ce que fait votre Machine, par exemple « Lecture des e-mails », « Lecture du PDF » ou « Rédaction du brouillon ». Les étapes détaillées restent dans le chat de la tâche.
- Une tâche marquée **En préparation…** démarre en quelques secondes. Si elle doit attendre, elle indique pourquoi et à peu près combien de temps, par exemple « Démarre après la tâche en cours ».
- Un site vous demande de vous connecter : appuyez sur **Se connecter**, ou sur **Ouvrir le navigateur** pour vous connecter depuis celui-ci. Elle continue ensuite automatiquement. Sinon, appuyez sur **Continuer**.
- Un code envoyé sur votre téléphone ou une autorisation manquante l’arrête. La tâche indique ce dont elle a besoin, puis affiche **Continuer** ou **Réessayer**. Si une source n’est pas connectée, par exemple Slack, **Connecter Slack** apparaît dans la tâche. Elle continue automatiquement une fois Slack connecté.
