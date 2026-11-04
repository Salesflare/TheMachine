---
title: Tâches
area: cards
summary: Une tâche par chose qui a besoin de vous, prête pour votre accord. Ce que veulent dire les parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
---
Votre Machine lit tout ce qui est nouveau et ne crée une tâche que si quelque chose a besoin de vous. Une tâche par sujet, peu importe le nombre de messages.

## Où sont les tâches

La page **Tâches** les regroupe :

- **Prêt pour vous** : préparée et en attente de votre accord.
- **Attend votre décision** : quelque chose que vous seul pouvez décider.
- **En préparation** : votre Machine y travaille. Une tâche à laquelle vous venez de dire **Faire** reste à sa place pendant la préparation, puis passe dans **Prêt pour vous**.
- **Tout juste fait** : une dernière étape que tu as confirmée, comme envoyer un formulaire ou créer un ticket, a réussi pendant ton absence. Elle montre ce qui s'est passé jusqu'à ce que tu touches **Compris**, un jour au plus, et ton téléphone l'apprend aussi. Ensuite, elle n'est plus que dans Fait.
- **Revient plus tard** : mise en attente.
- **Promesses** : ce que vous avez promis et ce que d’autres vous ont promis. Voir [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, les plus récentes d’abord, 30 à la fois quand vous faites défiler. Les tâches qui semblent déjà terminées viennent en premier, avec l’étiquette **Semble fait**.

Une tâche marquée **Semble fait** s’affiche comme une tâche faite, avec ce qui montre qu’elle est faite, comme « PR #3451 fusionnée ». Elle n’est pas encore fermée : **Rouvrir** la remet dans votre liste, et votre Machine en tient compte. Elles ne sont jamais en retard et ne comptent pas comme en attente de vous.

Une tâche dont la dernière étape reste ouverte chez quelqu’un d’autre, comme une relecture, une fusion ou une réponse, affiche **En attente de :** cette étape et reste ouverte. Elle attend dans **En attente des autres**, repliée au-dessus de Revient plus tard, et ne compte pas comme prête pour vous. Un nouveau message à son sujet la ramène.

**Tout est à jour.** veut dire que rien n’a besoin de vous pour l’instant. La ligne en dessous indique quand votre Machine a regardé pour la dernière fois.

**Tout**, **Travail** et **Perso** au-dessus de la liste dans la barre latérale affichent toutes les tâches ou un seul type. Votre Machine garde ce choix, pour que votre téléphone et votre ordinateur affichent la même liste. Quand Travail ou Perso est actif, le haut de la liste l’indique, avec **Tout afficher** pour revenir.

Une tâche liée à un projet affiche le nom du projet sur la ligne sous son titre ; il ouvre le projet. **Projet** sous **Détails** le change ou le retire. Voir [les tâches d’un projet](graph.md#a-projects-to-dos).

**Domaine** sous **Détails** déplace la tâche vers votre autre espace, comme une tâche perso qui doit partir de votre adresse pro. Ce qu’elle peut lire et d’où elle peut envoyer suit le déplacement ; les messages d’où elle vient restent où ils sont. **Annuler** dans le message qui suit la remet en place.

Quand une tâche a besoin d’un autre espace pour avancer, elle le demande avec un bouton **Déplacer vers Travail**. Rien ne bouge avant que vous appuyiez ; ensuite, elle continue toute seule.

Quand vous lancez une tâche, elle peut toujours lire les messages d’où elle vient, même dans la boîte d’une autre entreprise. Si elle a besoin d’autres messages d’un autre espace, elle le demande avec **Utiliser cet e-mail pour cette tâche** ; un appui les ajoute et elle continue. Le courrier pour une autre de vos entreprises va dès le départ dans les tâches de cette entreprise.

## Les boutons

Une tâche affiche son étape suivante, comme **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Voir [Faire](do-it.md) et [Mettre en attente](snooze.md).

Pas encore préparée, elle a **Changer d’approche** (dites comment faire autrement) ; prête, **Demander des modifications** (dites ce qu’il faut changer dans le brouillon). Quand la rangée est pleine sur un téléphone, **Mettre en attente** passe dans **…**. **Marquer comme fait** (c’est réglé) est là aussi : visible sans brouillon, sinon en haut de **…**.

Pour la faire autrement, dites-le dans son **Chat**.

Sous **…** (sur un téléphone, ce menu s’ouvre depuis le bas de l’écran) :

- **Transférer…** : la confier à un coéquipier, à [Claude Code ou Codex](hand-to-agent.md) (ceux que vous avez configurés) ou [demander une relecture à quelqu’un](ask-to-review.md).
- **Répéter…** : elle [revient à un rythme régulier](recurring.md).
- **Pas nécessaire** : elle disparaît. Choisissez pourquoi, si vous voulez : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des leçons.

Appuyez sur le titre, ou sur **Nom** sous **Détails**, pour la renommer. Votre titre reste, même quand la tâche change.

Une tâche fermée peut revenir avec **Rouvrir**. Elle revient aussi d’elle-même quand il se passe quelque chose de nouveau, comme un nouveau message de la personne. Votre propre réponse ne la fait pas revenir.

Une tâche qui ne comptait que jusqu’à un moment précis, comme une confirmation avant une réunion, se ferme d’elle-même une fois ce moment passé. Elle passe dans les tâches terminées avec « Plus nécessaire » et la date. **Annuler** la fait revenir pendant un jour.

Sur vos premières tâches, une courte ligne sous les boutons montre l’essentiel : **Changer d’approche** (ou **Demander des modifications**) et **Pas nécessaire** quand une tâche ne convient pas tout à fait, et sur votre premier brouillon prêt, que rien ne part avant que vous appuyiez sur **Envoyer**. Une astuce disparaît pour de bon dès que vous utilisez son bouton ou appuyez sur ×, sur tous vos appareils.

Le premier jour, le haut des Tâches vous salue par votre prénom et indique qui attend votre réponse depuis le plus longtemps. The Machine rédige cette réponse en premier, pour qu’elle soit prête à votre arrivée. Rien ne part avant que vous l’envoyiez. La ligne disparaît après votre premier jour ou votre première tâche décidée.

Chaque tâche commence par son titre. La ligne en dessous indique la personne concernée, son organisation, le projet, Travail ou Perso (sous **Tout**) et quand elle est arrivée, ainsi que son état quand son groupe ne le dit pas déjà. Appuyez sur un nom pour ouvrir sa page dans le Graph.

Parfois, une ligne discrète sous le texte dit ce qui n'est pas connu, comme « Dernier contact il y a 12 jours par e-mail ; rien depuis. » Elle n'apparaît que si le dernier échange est ancien ou toujours sans réponse, et nomme les canaux non connectés où une réponse a pu arriver, comme WhatsApp. Votre Machine prépare avec les mêmes faits : elle dit ce qu'elle ne sait pas au lieu de deviner.

Un titre dit ce qu'il faut faire. Il ne change que quand cela change, par exemple pour une nouvelle demande. Une tâche faite garde son titre, avec en dessous comment elle s'est terminée, par exemple ce qui est parti ou "Fait : Sam a signé mardi".

**Détails** montre son nom, son projet et son espace (appuyez sur l’un d’eux pour le changer), le message d’origine (appuyez dessus pour lire le fil), votre dernière note et le résultat d’un agent de code. **Chat ›** au bout de cette ligne ouvre le chat. Une tâche terminée reste courte : son titre, une ligne et ce qui est parti.

Une tâche « En attente de » (quelqu’un vous a promis quelque chose) renvoie vers votre dernier message à cette personne, celui auquel vous attendez une réponse : « E-mail à Pat · mar. ».

## En créer une vous-même

**Nouvelle tâche** (sous **Rechercher** sur ordinateur) ajoute une tâche pour n’importe quoi. La créer n’envoie rien.

- **Échéance** : tapez un jour ou une heure, comme « demain », « ven. prochain », « 3 nov. », « 15:00 », « dans 2 heures » ou « demain 14h ». L’anglais marche aussi (« in 2 hours », « tomorrow 9 »). L’icône du calendrier propose des choix rapides, comme pour la mise en attente, et **Choisir une date**.
- **E-mail** : joignez l’e-mail concerné. La recherche porte uniquement sur vos e-mails, par objet ou par expéditeur.
- **Fichiers** : touchez le trombone dans le champ, collez une capture d’écran ou déposez des fichiers sur le formulaire. Sur un téléphone, vous pouvez aussi prendre une photo. Jusqu’à 5 fichiers, des mêmes types et tailles que dans le chat (voir [Ajouter des fichiers](card-chat.md#add-files)). × en retire un.

Les fichiers restent avec la tâche : ils s’affichent sur la tâche et dans son chat, et The Machine les lit en travaillant dessus.
