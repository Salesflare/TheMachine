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
- **Revient plus tard** : mise en attente.
- **Semblent faites** : les tâches qui semblent déjà terminées. Repliées, juste au-dessus de **Fait / écarté**.
- **Fait / écarté** : toutes les tâches terminées, les plus récentes d’abord, 30 à la fois quand vous faites défiler.

Sous **Semblent faites**, chaque tâche tient en une ligne : son titre et ce qui montre qu’elle est faite, comme « PR #3451 fusionnée ». **Fait** en ferme une, **Tout marquer comme fait** les ferme toutes (avec **Annuler**), et **Pas fait** la remet comme tâche normale pour que votre Machine en tienne compte. Touchez une ligne pour voir toute la tâche. Elles ne sont jamais en retard et ne comptent pas comme en attente de vous. Rien ne se ferme sans vous.

Une tâche dont la dernière étape reste ouverte chez quelqu’un d’autre, comme une relecture, une fusion ou une réponse, affiche **En attente de :** cette étape et reste ouverte. Elle attend dans **En attente des autres**, repliée au-dessus de Revient plus tard, et ne compte pas comme prête pour vous. Un nouveau message à son sujet la ramène.

**Tout est à jour.** veut dire que rien n’a besoin de vous pour l’instant. La ligne en dessous indique quand votre Machine a regardé pour la dernière fois.

**Tout**, **Travail** et **Perso** au-dessus de la liste dans la barre latérale affichent toutes les tâches ou un seul type. Votre Machine garde ce choix, pour que votre téléphone et votre ordinateur affichent la même liste. Quand Travail ou Perso est actif, le haut de la liste l’indique, avec **Tout afficher** pour revenir.

Une tâche liée à un projet affiche le nom du projet sur la ligne sous son titre ; il ouvre le projet. **Changer de projet** dans **Plus** le change (sur une tâche terminée, dans **Détails**). Voir [les tâches d’un projet](graph.md#a-projects-to-dos).

## Les boutons

Une nouvelle tâche a **Faire**, **Marquer comme fait**, **Mettre en attente**, **Faire autrement** et **Pas nécessaire**. Seuls quelques-uns s’affichent à la fois ; les autres sont sous **Plus**, avec **Renommer**.

- **Faire** : votre Machine la prépare. Voir [Faire](do-it.md).
- **Marquer comme fait** : c’est réglé.
- **Mettre en attente** : la faire revenir plus tard. Voir [Mettre en attente](snooze.md).
- **Faire autrement** : dites en quelques mots ce que vous voulez à la place. Sur une tâche préparée, c’est **Demander des modifications** : dites ce qu’il faut changer dans le brouillon et elle le refait. **Vérifier et envoyer** reste à côté.
- **Pas nécessaire** : elle disparaît. Choisissez pourquoi, si vous voulez : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des leçons.

Une tâche fermée peut revenir avec **Rouvrir**. Elle revient aussi d’elle-même quand il se passe quelque chose de nouveau, comme un nouveau message de la personne. Votre propre réponse ne la fait pas revenir.

Une tâche qui ne comptait que jusqu’à un moment précis, comme une confirmation avant une réunion, se ferme d’elle-même une fois ce moment passé. Elle passe dans les tâches terminées avec « Plus nécessaire » et la date. **Annuler** la fait revenir pendant un jour.

Sur vos premières tâches, une courte ligne sous les boutons montre l’essentiel : **Faire autrement** (ou **Demander des modifications**) et **Pas nécessaire** quand une tâche ne convient pas tout à fait, et sur votre premier brouillon prêt, que rien ne part avant que vous appuyiez sur **Envoyer**. Une astuce disparaît pour de bon dès que vous utilisez son bouton ou appuyez sur ×, sur tous vos appareils.

Chaque tâche commence par son titre. La ligne en dessous indique la personne concernée, son organisation, le projet, Travail ou Perso (sous **Tout**) et quand elle est arrivée, ainsi que son état quand son groupe ne le dit pas déjà. Appuyez sur un nom pour ouvrir sa page dans le Graph.

Parfois, une ligne discrète sous le texte dit ce qui n'est pas connu, comme « Dernier contact il y a 12 jours par e-mail ; rien depuis. » Elle n'apparaît que si le dernier échange est ancien ou toujours sans réponse, et nomme les canaux non connectés où une réponse a pu arriver, comme WhatsApp. Votre Machine prépare avec les mêmes faits : elle dit ce qu'elle ne sait pas au lieu de deviner.

Un titre dit ce qu'il faut faire. Il ne change que quand cela change, par exemple pour une nouvelle demande. Une tâche faite garde son titre, avec en dessous comment elle s'est terminée, par exemple ce qui est parti ou "Fait : Sam a signé mardi".

**Détails** montre le message d’origine (appuyez dessus pour lire le fil), votre dernière note et le résultat d’un agent de code. **Chat ›** au bout de cette ligne ouvre le chat. Une tâche terminée reste courte : son titre, une ligne et ce qui est parti.

Une tâche « En attente de » (quelqu’un vous a promis quelque chose) renvoie vers votre dernier message à cette personne, celui auquel vous attendez une réponse : « E-mail à Pat · mar. ».

## En créer une vous-même

**Nouvelle tâche** (sous **Trouver une tâche** sur ordinateur) ajoute une tâche pour n’importe quoi. La créer n’envoie rien.

- **Échéance** : tapez un jour ou une heure, comme « demain », « ven. prochain », « 3 nov. », « 15:00 », « dans 2 heures » ou « demain 14h ». L’anglais marche aussi (« in 2 hours », « tomorrow 9 »). L’icône du calendrier propose des choix rapides, comme pour la mise en attente, et **Choisir une date**.
- **E-mail** : joignez l’e-mail concerné. La recherche porte uniquement sur vos e-mails, par objet ou par expéditeur.
- **Fichiers** : touchez le trombone dans le champ, collez une capture d’écran ou déposez des fichiers sur le formulaire. Sur un téléphone, vous pouvez aussi prendre une photo. Jusqu’à 5 fichiers, des mêmes types et tailles que dans le chat (voir [Ajouter des fichiers](card-chat.md#add-files)). × en retire un.

Les fichiers restent avec la tâche : ils s’affichent sur la tâche et dans son chat, et The Machine les lit en travaillant dessus.
