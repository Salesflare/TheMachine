---
title: Faire et ce qui est envoyé
area: cards
summary: Faire prépare le travail. Rien n’est envoyé, payé ni modifié avant que vous approuviez cette étape.
covers: do-it
code: dashboard.html, next_actions.py, assistant.py
order: 2
translated: 9e0936e0d9712ce3
---
## Ce que fait Faire

**Faire** demande à votre Machine de préparer la tâche : rédiger une réponse, faire des recherches ou remplir un formulaire. Elle utilise vos comptes et son propre navigateur, comme vous le feriez.

Pendant qu’elle travaille dans son navigateur, la tâche et son chat affichent cette page en direct, y compris entre les étapes, jusqu’à ce que la tâche soit terminée. Cliquez sur l’image pour ouvrir le navigateur. Dans la tâche, elle s’affiche en plus grand, avec **Arrêter** : une pression met immédiatement fin à cette exécution.

Avant un suivi ou un transfert, elle vérifie s’il y a de nouvelles réponses, y compris celles d’un collègue. Si la demande a déjà été traitée, la tâche l’indique. Si elle a modifié un document ou une page, la tâche fournit un lien vers celui-ci.

Quand une tâche complexe aboutit sur un site ou dans un processus, votre Machine enregistre les étapes sous forme de compétence, sans aucune donnée personnelle. Les tâches ultérieures sur ce site les utilisent comme guide, jamais comme autorisation : l’envoi ou le paiement attend toujours votre accord. Elles apparaissent dans **Paramètres > Compétences**, sous **Appris lors d’une tâche**.

Si les étapes d’une compétence ne fonctionnent plus pendant trois tâches consécutives, votre Machine la désactive. Elle le restera jusqu’à ce qu’une tâche ultérieure montre ce qui fonctionne maintenant ou que vous la réactiviez.

## Rien n’est envoyé sans votre accord

- Une réponse est préparée sous forme de brouillon. **Vérifier et envoyer** permet de le modifier avant l’envoi. Le message part uniquement lorsque vous appuyez sur **Envoyer maintenant**.
- S’il y a au moins deux e-mails dans une même tâche, un bouton dans son chat permet de les vérifier tous. Ils s’affichent l’un après l’autre avec **Suivant**. La dernière étape les envoie tous. Chacun est indiqué comme envoyé uniquement après son envoi.
- Un e-mail s’affiche tel qu’il sera envoyé, avec le texte en gras, les listes et les liens. Un message Slack ou un message de chat est en texte brut.
- **Demander des modifications** dans la même fenêtre : indiquez ce qui doit changer et votre Machine refait le brouillon.
- Une réponse répond au dernier e-mail du fil, et la source de la tâche ouvre cet e-mail.
- Une étape qui valide une action, comme envoyer un formulaire, payer ou réserver, attend votre confirmation ou votre demande dans le chat. La confirmation d’une étape ne débloque pas les autres : la tâche se ferme uniquement lorsque toutes les étapes sont terminées.
- La tâche et son chat indiquent ce qu’une telle étape enverra avant que vous la validiez. Une invitation d’agenda affiche son titre, l’heure, les invités et précise si un lien de réunion est ajouté.
- Les agendas connectés sont pris en compte lors de la recherche d’un créneau : votre Machine consulte vos réunions des jours concernés avant de vous proposer des horaires.
- Dans le chat d’une tâche, un brouillon n’est jamais envoyé dans le même message que celui qui l’a rédigé.
- Tant que vous n’avez pas donné votre accord, la tâche attend dans **Pour vous**, avec le statut **Préparée**. La liste indique une seule fois que rien ne sera envoyé avant votre accord. **Préparée** signifie qu’un brouillon ou un résultat est prêt à être approuvé. Si le travail se termine sans brouillon ni résultat parce que la tâche a besoin de vous (pour une décision, une information manquante, une connexion ou un choix), elle affiche plutôt **Vous attend**, avec une ligne qui indique ce dont elle a besoin. C’est aussi le cas si elle a seulement répondu ou fourni une explication ("Réponse apportée. Rien n’a encore été fait."), avec **Faire** en premier. Il en va de même pour la notification et le récap du matin. La tâche indique qu’un brouillon a été envoyé uniquement après son envoi.
- Un brouillon inutilisable en l’état, par exemple une proposition sans prix, affiche aussi **Vous attend** : la question apparaît sur sa ligne et **Répondre** permet d’y répondre. Le brouillon reste dans la tâche, avec **Envoyer** sous **⋯** ou **Copier le brouillon** au-dessus des boutons. Ajoutez vous-même l’information manquante pour que le statut redevienne **Préparée**.
- Un brouillon qui peut être envoyé tel quel reste **Préparée**. Si un point peut encore être amélioré, la tâche l’indique sur sa ligne : "Le brouillon est prêt. Une question : …".
- Les trois premières lignes d’un long brouillon s’affichent. **Afficher plus**, ou un appui sur le texte, affiche le reste. **Vérifier et envoyer** affiche toujours le brouillon en entier.

Selon la source, elle peut envoyer un e-mail, un message privé Slack ou un message WhatsApp, Telegram, LinkedIn ou X. L’article de chaque connexion indique ce qu’elle peut envoyer.

## Modifier un e-mail

- Utilisez les boutons au-dessus du texte, ou `Ctrl B` pour le gras, `Ctrl I` pour l’italique et `Ctrl K` pour un lien (`⌘` sur Mac). Des boutons permettent aussi de créer des listes à puces et numérotées.
- Un lien doit commencer par https://. Le texte collé est inséré en texte brut, sans couleurs ni images.
- Les mises en forme incompatibles avec l’envoi d’un e-mail sont supprimées. Le message affiche ensuite le résultat final. Appuyez de nouveau sur **Envoyer maintenant** pour l’envoyer.
- L’e-mail est envoyé exactement comme il s’affiche, avec une copie en texte brut pour les applications de messagerie qui ne prennent pas en charge la mise en forme.

## Si l’envoi est impossible

- "Cet élément ne peut pas être envoyé ici." signifie que vous devez copier le brouillon avec **Copier le brouillon** et l’envoyer vous-même.
- Si **Vous attend** s’affiche et qu’aucun élément ne peut encore être envoyé, ouvert ou lu, la tâche propose **Répondre** : indiquez ce dont elle a besoin pour qu’elle puisse continuer. Si seule vous pouvez effectuer une étape, comme un paiement dans votre banque, la tâche propose **Marquer comme fait**.
- **Attend votre aide** signifie que la tâche a une question : **Répondre**. **Bloqué** signifie qu’elle s’est arrêtée sans poser de question ; la tâche en indique la raison.
- Vous avez reçu plusieurs questions ? Chacune propose ses propres choix ou un champ court, parfois prérempli avec votre réponse précédente. **Répondre** les envoie toutes en même temps.
- Quelqu’un vous a demandé des informations ou des fichiers ? La tâche rédige une réponse avec ce qu’elle a trouvé et ne vous demande que le reste.
- Il manque une information que vous seul connaissez ? La tâche vous la demande et ne rédige que les éléments qui peuvent s’en passer, comme une réponse confirmant une date. Elle ne rédige pas une réponse qui dit simplement que l’information suivra.
- **Réessayer** relance la tâche. **Demander des modifications** permet de demander autre chose. Pour une tâche bloquée, **Réessayer** apparaît en premier et **Détails** affiche ce qu’elle a essayé.
- Si la tâche est bloquée parce que l’exécution a échoué, votre Machine la réessaie automatiquement une fois après sa mise à jour.
- Elle réessaie automatiquement une exécution échouée au maximum deux fois. Ensuite, elle attend un nouvel élément, comme un nouveau message ou un message de votre part dans son chat, ou que vous appuyiez sur **Réessayer**.
- Pendant la préparation, la tâche indique en une phrase ce que fait votre Machine, par exemple "Lecture de l’e-mail", "Lecture du PDF" ou "Rédaction du brouillon". Les étapes détaillées restent dans le chat de la tâche.
- Une tâche avec le statut **En préparation…** démarre en quelques secondes. Si elle doit attendre, elle en indique la raison et le délai approximatif, par exemple "Démarre après la tâche en cours".
- Une tâche que votre Machine prépare avant que vous le lui demandiez peut attendre pour économiser votre consommation. Le bouton **Faire** reste visible : appuyez dessus pour la lancer immédiatement, avant les autres tâches. Rien n’est envoyé sans votre accord. Si la limite d’utilisation de votre forfait IA est atteinte, Faire vous l’indique et la tâche démarre une fois la limite réinitialisée.
- Un site vous demande de vous connecter : appuyez sur **Se connecter**, ou sur **Ouvrir le navigateur** et connectez-vous dans le navigateur. La tâche reprend ensuite automatiquement. Si ce n’est pas le cas, appuyez sur **Continuer**.
- Un code envoyé sur votre téléphone ou une autorisation manquante arrête la tâche. Celle-ci indique ce dont elle a besoin, puis propose **Continuer** ou **Réessayer**. Si une source n’est pas connectée, comme Slack, **Connecter Slack** apparaît dans la tâche. Elle reprend automatiquement une fois Slack connecté.
