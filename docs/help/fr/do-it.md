---
title: Faire, et ce qui est envoyé
area: cards
summary: Faire prépare le travail. Rien n’est envoyé, payé ni modifié tant que vous n’avez pas approuvé cette étape.
covers: do-it
code: dashboard.html, next_actions.py, assistant.py
order: 2
translated: 19077049dc3db174
---
## Ce que fait Faire

**Faire** demande à votre Machine de préparer la tâche : rédiger une réponse, chercher des informations, remplir un formulaire. Elle utilise vos propres comptes et son propre navigateur, comme vous le feriez.

Pendant qu’elle travaille dans son navigateur, la tâche et son chat affichent cette page en direct, y compris entre les étapes, jusqu’à ce qu’elle ait terminé. Cliquez sur l’image pour ouvrir le navigateur. Dans la tâche, la page s’ouvre en grand, avec **Arrêter** : une seule pression met fin à cette exécution.

Avant un suivi ou un transfert, elle vérifie s’il y a de nouvelles réponses, y compris de la part d’un collègue. Si la tâche a déjà été traitée, elle vous le dit. Si elle a modifié un document ou une page, la tâche contient un lien vers celui-ci.

Quand une tâche complexe aboutit sur un site ou dans un workflow, votre Machine mémorise les étapes sous forme de compétence, sans aucune donnée personnelle. Les tâches suivantes sur ce site s’en servent comme guide, jamais comme autorisation : l’envoi ou le paiement attend toujours votre accord. Elles apparaissent dans **Paramètres > Skills** sous **Appris lors d’une tâche**.

Si les étapes d’une compétence ne fonctionnent plus pour trois tâches d’affilée, votre Machine la désactive. Elle la réactive uniquement si une tâche ultérieure montre ce qui fonctionne maintenant, ou si vous la réactivez vous-même.

## Rien n’est envoyé sans votre accord

- Une réponse revient sous forme de brouillon. **Vérifier et envoyer** l’ouvre pour que vous puissiez le modifier. Elle n’est envoyée que lorsque vous appuyez sur **Envoyer maintenant**.
- S’il y a au moins deux e-mails dans une tâche, un seul bouton dans son chat permet de tous les vérifier. Ils s’affichent l’un après l’autre avec **Suivant**, et la dernière étape les envoie tous. Chaque e-mail n’apparaît comme envoyé qu’une fois qu’il l’est.
- Un e-mail s’affiche tel qu’il sera envoyé, avec le texte en gras, les listes et les liens. Un message Slack ou un message de chat est en texte brut.
- **Demander des modifications** dans la même fenêtre : indiquez ce qu’il faut modifier et votre Machine prépare un nouveau brouillon.
- Une réponse répond au dernier e-mail du fil, et la source de la tâche ouvre cet e-mail.
- Une étape qui confirme une action, comme envoyer un formulaire, payer ou réserver, attend votre confirmation ou que vous le demandiez dans le chat. La confirmation d’une étape laisse les autres en attente : la tâche ne se ferme que lorsque toutes les étapes sont terminées.
- La tâche et son chat indiquent ce qu’une telle étape enverra avant que vous appuyiez dessus. Une invitation d’agenda affiche son titre, son horaire, ses invités et précise si un lien de réunion est ajouté.
- Les agendas connectés sont pris en compte lors de la recherche d’un créneau : votre Machine consulte vos réunions pour ces journées avant de vous proposer des horaires.
- Dans le chat d’une tâche, un brouillon n’est jamais envoyé dans le même message que celui qui l’a rédigé.
- Tant que vous n’avez pas approuvé le résultat, la tâche reste sous **Pour vous** avec le statut **Préparée**, et la liste indique une fois que rien ne sera envoyé avant votre approbation. **Préparée** signifie qu’un brouillon ou un résultat est prêt à être approuvé. Si le travail se termine sans résultat parce qu’elle a besoin de vous (pour une décision, une information manquante, une connexion ou un choix), la tâche affiche plutôt **Vous attend**, avec une ligne indiquant ce dont elle a besoin. C’est aussi le cas lorsqu’elle s’est contentée de répondre ou d’expliquer (« Réponse apportée. Rien n’a encore été fait. »), avec **Faire** en premier. Il en va de même pour sa notification et le récap du matin. Elle indique qu’un brouillon a été envoyé uniquement une fois qu’il l’a été.
- Un brouillon qui ne peut pas encore être utilisé, comme une proposition sans prix, affiche aussi **Vous attend** : la question apparaît sur la ligne et **Répondre** permet d’y accéder. Le brouillon reste dans la tâche, avec **Envoyer** sous **⋯** ou **Copier le brouillon** au-dessus des boutons. Ajoutez vous-même les informations manquantes et son statut repasse à **Préparée**.
- Une réponse d’attente, qui promet simplement que le travail sera fait (« Je vous enverrai le devis »), affiche **Vous attend** : « Réponse d’attente prête. À faire : envoyer le devis. » **Envoyer** reste en premier, et la tâche reste ouverte après l’envoi.
- Un brouillon qui peut être envoyé tel quel reste **Préparée**. Si un point peut encore être amélioré, une ligne le précise : « Le brouillon est prêt. Une question : … ».
- Un long brouillon affiche ses 3 premières lignes. **Afficher plus**, ou un appui sur le texte, affiche la suite. **Vérifier et envoyer** affiche toujours le texte en entier.

Selon la source, elle peut envoyer un e-mail, un message privé Slack, ou un message WhatsApp, Telegram, LinkedIn ou X. L’article de chaque connexion indique ce qu’elle peut envoyer.

## Modifier un e-mail

- Utilisez les boutons au-dessus du texte, ou `Ctrl B` pour le gras, `Ctrl I` pour l’italique et `Ctrl K` pour un lien (`⌘` sur Mac). Des boutons permettent aussi de créer une liste à puces ou numérotée.
- Un lien doit commencer par https://. Le texte collé est inséré en texte brut, sans ses couleurs ni ses images.
- Le formatage qui ne peut pas être conservé dans un e-mail est d’abord supprimé, et le message affiche le résultat final. Appuyez de nouveau sur **Envoyer maintenant** pour l’envoyer.
- L’e-mail est envoyé exactement comme il s’affiche, avec une copie en texte brut pour les applications de messagerie qui ne prennent pas en charge le formatage.

## Si elle ne peut pas le faire

- « Impossible d’envoyer ceci depuis ici. » signifie que vous devez copier le brouillon avec **Copier le brouillon** et l’envoyer vous-même.
- Si **Vous attend** s’affiche sans qu’il y ait encore quoi que ce soit à envoyer, ouvrir ou lire, la tâche commence par **Répondre** : indiquez ce dont elle a besoin pour qu’elle continue. Si seule vous pouvez effectuer une étape, comme un paiement dans votre banque, elle commence par **Marquer comme fait**.
- **Attend votre aide** signifie qu’elle a une question : **Répondre**. **Bloqué** signifie qu’elle s’est arrêtée sans question. La tâche vous en indique la raison.
- Vous avez posé plusieurs questions ? Chacune propose ses propres choix ou un champ court, parfois déjà rempli avec votre réponse précédente. **Répondre** les envoie toutes à la fois.
- Quelqu’un vous a demandé des informations ou des fichiers ? Elle prépare une réponse avec ce qu’elle a trouvé et ne vous demande que le reste.
- Il manque une information que vous seul possédez ? Elle vous la demande et ne rédige que ce qui peut être envoyé sans elle, comme une réponse confirmant une date. Elle ne rédige pas une réponse qui dit seulement que l’information suivra.
- **Réessayer** relance la tâche. **Demander des modifications** permet de demander autre chose. Pour une tâche bloquée, **Réessayer** apparaît en premier et **Détails** affiche ce qu’elle a tenté.
- La tâche est bloquée parce que l’exécution a échoué ? Après la mise à jour de votre Machine, elle réessaie cette tâche une fois automatiquement.
- Elle réessaie automatiquement une exécution en échec au maximum deux fois. Ensuite, elle attend quelque chose de nouveau, comme un nouveau message ou un message de votre part dans son chat, ou que vous appuyiez sur **Réessayer**.
- Pendant la préparation, la tâche indique en une phrase ce que fait votre Machine, comme « Lecture des e-mails », « Lecture du PDF » ou « Rédaction du brouillon ». Les étapes détaillées restent dans le chat de la tâche.
- Une tâche marquée **En préparation…** démarre en quelques secondes. Si elle doit attendre, elle en indique la raison et le délai approximatif, par exemple « Démarre après la tâche en cours ».
- Une tâche que votre Machine prépare avant que vous le lui demandiez peut attendre pendant qu’elle économise votre utilisation. **Faire** reste affiché : appuyez dessus pour la démarrer immédiatement, avant les autres. Rien n’est envoyé sans votre accord. Si la limite d’utilisation de votre forfait IA est atteinte, Faire vous l’indique et la tâche démarre une fois la limite réinitialisée.
- Un site vous demande de vous connecter : appuyez sur **Se connecter**, ou sur **Ouvrir le navigateur** et connectez-vous depuis celui-ci. Elle continue ensuite automatiquement. Si ce n’est pas le cas, appuyez sur **Continuer**.
- Un code envoyé sur votre téléphone ou une autorisation manquante l’arrête. La tâche vous indique ce dont elle a besoin, puis propose **Continuer** ou **Réessayer**. Si une source n’est pas connectée, comme Slack, **Connecter Slack** apparaît dans la tâche. Elle continue automatiquement une fois Slack connecté.
