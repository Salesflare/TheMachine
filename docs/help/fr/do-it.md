---
title: Faire et ce qui est envoyé
area: cards
summary: Faire prépare le travail. Rien n’est envoyé, payé ni modifié avant que vous approuviez l’étape concernée.
covers: do-it
code: dashboard.html, next_actions.py, assistant.py
order: 2
translated: c8a5478e8a9cdab1
---
## Ce que fait Faire

**Faire** demande à votre Machine de préparer la tâche : rédiger une réponse, faire des recherches, remplir un formulaire. Elle utilise vos comptes et son propre navigateur, comme vous le feriez.

Pendant qu’elle travaille dans son navigateur, la tâche et son chat affichent la page en direct, y compris entre les étapes, jusqu’à ce qu’elle ait terminé. Cliquez sur l’image pour ouvrir le navigateur. Dans la tâche, la page s’affiche en plus grand, avec **Arrêter** : une seule pression interrompt immédiatement cette exécution.

Avant un suivi ou un transfert, elle vérifie s’il y a de nouvelles réponses, y compris de la part d’un collègue. Si la tâche a déjà été traitée, elle l’indique. Si elle a modifié un document ou une page, la tâche contient un lien vers cet élément.

Lorsqu’une tâche complexe aboutit sur un site ou dans un workflow, votre Machine conserve les étapes sous forme de compétence, sans aucune information personnelle. Les tâches suivantes sur ce site les utilisent comme guide, jamais comme autorisation : l’envoi et le paiement restent soumis à votre accord. Ces compétences apparaissent dans **Paramètres > Compétences**, sous **Appris lors d’une tâche**.

## Rien n’est envoyé sans votre accord

- Une réponse est proposée sous forme de brouillon. **Vérifier et envoyer** l’ouvre pour que vous puissiez le modifier. Elle n’est envoyée que si vous appuyez sur **Envoyer maintenant**.
- Pour deux e-mails ou plus dans une même tâche, un bouton dans le chat permet de tous les vérifier. Ils s’affichent l’un après l’autre avec **Suivant**. La dernière étape les envoie tous. Chaque e-mail n’est indiqué comme envoyé qu’une fois qu’il l’a été.
- Un e-mail s’affiche tel qu’il apparaîtra, avec le texte en gras, les listes et les liens. Un message Slack ou un message de chat est en texte brut.
- **Demander des modifications** dans la même fenêtre : dites ce qu’il faut changer et votre Machine retravaille le brouillon.
- Une réponse répond au dernier e-mail du fil, et la source de la tâche ouvre cet e-mail.
- Une étape qui valide une action, comme envoyer un formulaire, payer ou réserver, attend votre confirmation ou votre demande dans le chat. Confirmer une étape laisse les autres en attente : la tâche ne se termine que lorsque toutes les étapes sont faites.
- La tâche et son chat indiquent ce qu’une telle étape enverra avant que vous appuyiez dessus. Une invitation de calendrier affiche son titre, l’heure, les invités et indique si un lien de réunion sera ajouté.
- Les agendas connectés sont pris en compte lorsqu’elle cherche un horaire : elle consulte vos réunions pour les jours concernés avant de proposer des horaires.
- Dans le chat d’une tâche, un brouillon n’est jamais envoyé dans le même message que celui qui l’a rédigé.
- Tant que vous ne l’avez pas approuvé, la tâche reste dans **Pour vous**, avec le statut **Préparée**. La liste précise une seule fois que rien ne sera envoyé avant votre approbation. **Préparée** signifie qu’un brouillon ou un résultat est prêt à être approuvé. Si le travail se termine sans résultat parce qu’elle a besoin de vous (pour une décision, une information manquante, une connexion ou un choix), la tâche affiche plutôt **Vous attend**, avec une ligne indiquant ce dont elle a besoin. C’est aussi le cas si elle s’est contentée de répondre ou d’expliquer (« Réponse apportée. Rien n’a encore été fait. »), avec **Faire** en premier. Il en va de même pour sa notification et le récap du matin. La tâche indique qu’un brouillon a été envoyé seulement une fois qu’il l’a été.
- Un long brouillon affiche ses 3 premières lignes. **Afficher plus**, ou un appui sur le texte, permet de voir la suite. **Vérifier et envoyer** affiche toujours le brouillon en entier.

Selon la source, elle peut envoyer un e-mail, un message direct Slack ou un message WhatsApp, Telegram, LinkedIn ou X. L’article de chaque connexion indique ce qu’elle peut envoyer.

## Modifier un e-mail

- Utilisez les boutons au-dessus du texte, ou `Ctrl B` pour le gras, `Ctrl I` pour l’italique et `Ctrl K` pour un lien (`⌘` sur Mac). Des boutons permettent aussi de créer une liste à puces ou numérotée.
- Un lien doit commencer par https://. Le texte collé est inséré en texte brut, sans ses couleurs ni ses images.
- Les formats incompatibles avec l’e-mail sont supprimés, et le message affiche le résultat final. Appuyez de nouveau sur **Envoyer maintenant** pour l’envoyer.
- L’e-mail est envoyé exactement comme il apparaît, avec une copie en texte brut pour les applications de messagerie qui n’affichent pas la mise en forme.

## Quand elle ne peut pas

- « Impossible d’envoyer depuis ici. » signifie que vous devez copier le brouillon avec **Copier le brouillon**, puis l’envoyer vous-même.
- **Attend votre aide** signifie qu’elle a une question : **Répondre**. **Bloqué** signifie qu’elle s’est arrêtée sans poser de question. La tâche en indique la raison.
- Vous avez demandé plusieurs choses ? Chaque question a ses propres choix ou un champ de réponse court, parfois déjà rempli avec votre réponse précédente. **Répondre** envoie toutes vos réponses en même temps.
- Il manque une information que vous seul avez ? Elle vous la demande et ne rédige que ce qui peut être fait sans cette information, comme une réponse confirmant une date. Elle ne rédige pas une réponse qui dit seulement qu’elle arrive.
- **Réessayer** relance la tâche. **Demander des modifications** permet de demander autre chose. Pour une tâche bloquée, **Réessayer** apparaît en premier, et **Détails** indique ce qu’elle a tenté.
- La tâche est bloquée parce que l’exécution a échoué ? Après la mise à jour de votre Machine, elle réessaie automatiquement une fois.
- Elle réessaie automatiquement une exécution échouée au maximum deux fois. Ensuite, elle attend un nouvel élément, comme un nouveau message ou un message de votre part dans son chat, ou que vous appuyiez sur **Réessayer**.
- Pendant la préparation, la tâche indique en une phrase simple ce que fait votre Machine, par exemple « Lecture des e-mails », « Lecture du PDF » ou « Rédaction du brouillon ». Les étapes détaillées restent dans le chat de la tâche.
- Une tâche marquée **En préparation…** démarre en quelques secondes. Si elle doit attendre, elle en indique la raison et le délai approximatif, par exemple « Démarre après la tâche en cours ».
- Une tâche préparée par votre Machine avant que vous ne la demandiez peut attendre pour économiser votre utilisation. Elle affiche quand même **Faire** : appuyez dessus pour la lancer immédiatement, avant les autres. Rien n’est envoyé sans votre accord. Si la limite d’utilisation de votre forfait IA est atteinte, Faire vous l’indique et la tâche démarre une fois la limite réinitialisée.
- Un site vous demande de vous connecter : appuyez sur **Se connecter**, ou sur **Ouvrir le navigateur** pour vous connecter dans le navigateur. Elle reprend ensuite automatiquement. Si ce n’est pas le cas, appuyez sur **Continuer**.
- Un code envoyé sur votre téléphone ou une autorisation manquante l’interrompt. La tâche indique ce dont elle a besoin, puis propose **Continuer** ou **Réessayer**. Si une source n’est pas connectée, comme Slack, **Connecter Slack** apparaît dans la tâche. Elle reprend automatiquement une fois Slack connecté.
