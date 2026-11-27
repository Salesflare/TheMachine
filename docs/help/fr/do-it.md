---
title: Faire et ce qui est envoyé
area: cards
summary: Faire prépare le travail. Rien n’est envoyé, payé ou modifié avant que vous validiez cette étape.
covers: do-it
code: dashboard.html, next_actions.py, assistant.py
order: 2
translated: 4b4bf05b5035c218
---
## Ce que fait **Faire**

**Faire** demande à votre Machine de préparer la tâche : rédiger une réponse, faire des recherches, remplir un formulaire. Elle utilise vos comptes et son propre navigateur, comme vous le feriez.

Pendant qu’elle travaille dans son navigateur, la tâche et son chat affichent la page en direct, y compris entre les étapes, jusqu’à ce qu’elle ait terminé. Cliquez sur l’image pour ouvrir le navigateur. Dans la tâche, elle s’affiche en plus grand, avec **Arrêter** : un seul clic arrête immédiatement cette exécution.

Avant une relance ou un transfert, elle vérifie s’il y a de nouvelles réponses, y compris de la part d’un collègue. Si la tâche a déjà été traitée, elle vous le dit. Si elle a modifié un document ou une page, la tâche contient un lien vers cet élément.

Quand votre Machine réussit une tâche complexe sur un site ou dans un flux de travail, elle conserve les étapes sous forme de compétence, sans aucune donnée personnelle. Les tâches suivantes sur ce site s’en servent comme guide, jamais comme autorisation : l’envoi ou le paiement attend toujours votre accord. Ces compétences s’affichent dans **Paramètres > Compétences**, sous **Appris lors d’une tâche**.

Si les étapes d’une compétence ne fonctionnent plus pour trois tâches consécutives, votre Machine la désactive. Elle le fait jusqu’à ce qu’une tâche ultérieure montre ce qui fonctionne maintenant ou que vous la réactiviez.

## Rien n’est envoyé sans votre accord

- Une réponse est préparée sous forme de brouillon. **Vérifier et envoyer** l’ouvre, prête à être modifiée. Elle n’est envoyée que lorsque vous appuyez sur **Envoyer maintenant**.
- S’il y a au moins deux e-mails dans une tâche, un bouton dans son chat permet de les vérifier tous. Ils s’affichent l’un après l’autre avec **Suivant**. La dernière étape les envoie tous. Chacun n’est indiqué comme envoyé qu’une fois qu’il l’a été.
- Un e-mail s’affiche tel qu’il sera envoyé, avec le texte en gras, les listes et les liens. Un message Slack ou un message de chat s’affiche en texte brut.
- **Demander des modifications** dans la même fenêtre : indiquez ce qu’il faut changer et votre Machine refait le brouillon.
- Une réponse est envoyée en réponse au dernier e-mail du fil. La source de la tâche ouvre cet e-mail.
- Une étape qui valide une action, comme envoyer un formulaire, payer ou réserver, attend votre confirmation ou votre demande dans le chat. La validation d’une étape ne lance pas les autres : la tâche ne se termine que lorsque toutes les étapes sont faites.
- La tâche et son chat montrent ce qu’une telle étape enverra avant que vous appuyiez dessus. Une invitation d’agenda indique son titre, l’heure, les invités et si un lien de réunion est ajouté.
- Les agendas connectés sont pris en compte lors de la recherche d’un créneau : votre Machine consulte vos réunions pour ces jours-là avant de vous proposer des horaires.
- Dans le chat d’une tâche, un brouillon n’est jamais envoyé dans le même message que celui qui l’a rédigé.
- Tant que vous ne l’avez pas approuvé, la tâche attend dans **Pour vous**, sous **Préparée**. La liste indique aussi une seule fois que rien ne sera envoyé avant votre accord. **Préparée** signifie qu’un brouillon ou un résultat est prêt à être approuvé. Si le travail se termine sans brouillon ni résultat parce que votre intervention est nécessaire, par exemple pour prendre une décision, fournir une information manquante ou vous connecter, la tâche affiche plutôt **Vous attend**, avec une ligne indiquant ce dont elle a besoin. C’est aussi le cas si elle s’est contentée de répondre ou d’expliquer (« Réponse donnée. Rien n’a encore été fait. ») : **Faire** s’affiche en premier. Il en va de même pour sa notification et le récap du matin. Elle indique qu’un brouillon a été envoyé uniquement après son envoi.
- Un brouillon qui ne peut pas encore être utilisé, par exemple une proposition sans prix, affiche aussi **Vous attend** : la question apparaît dans la description et **Répondre** permet d’y accéder. Le brouillon reste dans la tâche, avec **Envoyer** sous **⋯** ou **Copier le brouillon** au-dessus des boutons. Ajoutez vous-même l’information manquante pour que la tâche affiche de nouveau **Préparée**.
- Une réponse d’attente, qui promet seulement que le travail sera fait (« Je vous enverrai le devis »), affiche **Vous attend** : « Réponse d’attente prête. Il reste à envoyer le devis. » **Envoyer** reste le premier bouton, et la tâche reste ouverte après l’envoi.
- Un brouillon qui peut être envoyé tel quel reste **Préparée**. Si un point peut encore être amélioré, la description le précise : « Le brouillon est prêt. Une question : … ».
- Un long brouillon affiche ses 3 premières lignes. **Afficher plus**, ou un appui sur le texte, affiche la suite. **Vérifier et envoyer** affiche toujours le texte en entier.

Selon la source, votre Machine peut envoyer un e-mail, un message privé Slack ou un message WhatsApp, Telegram, LinkedIn ou X. L’article de chaque connexion indique ce qu’elle peut envoyer.

## Modifier un e-mail

- Utilisez les boutons au-dessus du texte ou `Ctrl B` pour le gras, `Ctrl I` pour l’italique et `Ctrl K` pour un lien (`⌘` sur Mac). Des boutons permettent aussi de créer une liste à puces ou numérotée.
- Un lien doit commencer par https://. Le texte collé est ajouté sans mise en forme, couleurs ni images.
- Les mises en forme qui ne sont pas prises en charge dans un e-mail sont d’abord supprimées. Le message affiche alors son apparence finale. Appuyez de nouveau sur **Envoyer maintenant** pour l’envoyer.
- L’e-mail est envoyé exactement comme affiché, avec une copie en texte brut pour les applications de messagerie qui n’affichent pas la mise en forme.

## Si l’envoi est impossible

- « Impossible d’envoyer depuis ici. » signifie que vous devez copier le brouillon avec **Copier le brouillon** et l’envoyer vous-même.
- Si une tâche affiche **Vous attend** sans rien qui puisse encore être envoyé, ouvert ou consulté, elle affiche d’abord **Répondre** : indiquez ce dont elle a besoin et elle reprendra. Si une étape ne peut être faite que par vous, comme un paiement dans votre banque, elle affiche **Marquer comme fait**.
- **Attend votre aide** signifie qu’elle a une question : **Répondre**. **Bloqué** signifie qu’elle s’est arrêtée sans poser de question. La tâche vous en indique la raison.
- Elle vous a posé plusieurs questions ? Chacune propose ses propres choix ou un champ court, parfois prérempli avec votre dernière réponse. **Répondre** les envoie toutes ensemble.
- Quelqu’un vous a demandé des informations ou des fichiers ? Votre Machine prépare une réponse avec les éléments qu’elle a trouvés et ne vous demande que le reste.
- Il manque une information que vous seul pouvez fournir ? Elle vous la demande et ne rédige que ce qui peut être envoyé sans elle, par exemple une réponse qui confirme une date. Elle ne rédige pas de réponse qui se contente de dire que l’information suivra.
- **Réessayer** relance la tâche. **Demander des modifications** permet de demander autre chose. Pour une tâche bloquée, **Réessayer** s’affiche en premier et **Détails** montre ce que votre Machine a essayé.
- La tâche est bloquée parce que l’exécution a échoué ? Après une mise à jour de votre Machine, elle réessaie cette tâche une fois automatiquement.
- Elle réessaie automatiquement une exécution en échec deux fois au maximum. Ensuite, elle attend un nouvel élément, comme un nouveau message ou un message de votre part dans son chat, ou que vous appuyiez sur **Réessayer**.
- Pendant la préparation, la tâche indique en une phrase simple ce que fait votre Machine, par exemple « Lecture de l’e-mail », « Lecture du PDF » ou « Rédaction du brouillon ». Les étapes détaillées restent dans le chat de la tâche.
- Une tâche marquée **En préparation…** démarre en quelques secondes. Si elle doit attendre, elle en indique la raison et le délai approximatif, par exemple « Démarrera après la tâche en cours ».
- Une tâche que votre Machine prépare avant que vous le lui demandiez peut attendre pour économiser de l’utilisation. Elle affiche tout de même **Faire** : appuyez dessus pour la lancer immédiatement, avant les autres. Rien n’est envoyé sans votre accord. Si la limite d’utilisation de votre forfait IA est atteinte, Faire vous l’indique et la tâche démarre une fois la limite réinitialisée.
- Un site vous demande de vous connecter ? Appuyez sur **Se connecter**, ou sur **Ouvrir le navigateur** et connectez-vous dans celui-ci. Votre Machine reprend ensuite automatiquement. Si elle ne le fait pas, appuyez sur **Continuer** : elle vérifie d’abord à nouveau son navigateur. Si le site affiche toujours la page de connexion, elle vous le signale au lieu de recommencer.
- Un code envoyé sur votre téléphone ou une autorisation manquante l’arrête. La tâche indique ce dont elle a besoin, puis affiche **Continuer** ou **Réessayer**. Si une source n’est pas connectée, comme Slack, **Connecter Slack** s’affiche dans la tâche. Votre Machine reprend automatiquement une fois Slack connecté.
