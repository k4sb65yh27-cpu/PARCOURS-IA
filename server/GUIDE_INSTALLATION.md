# Parcours IA : installation sur un serveur SATT

Version 1, 25/11/2026.

## Ce que c'est

Le Parcours IA est une application web de formation à l'usage des assistants d'IA (Claude, ChatGPT, Copilot, Le Chat). Elle se compose de fichiers statiques (HTML, JavaScript, CSS, images) et d'un script PHP de synchronisation.

- Sur PC, elle s'ouvre dans le navigateur. Edge et Chrome proposent aussi « Installer l'application ».
- Sur téléphone, on l'ajoute à l'écran d'accueil : Safari, Partager, puis « Sur l'écran d'accueil » sur iPhone ; Chrome, puis « Installer » sur Android.
- Elle fonctionne hors connexion une fois chargée.
- Avec un compte, la progression suit l'utilisateur d'un appareil à l'autre. Sans le script PHP, l'application marche quand même, mais la progression reste dans le navigateur.

Aucune ressource externe n'est chargée. L'application n'envoie aucune donnée ailleurs qu'au script de synchronisation du même serveur, et n'appelle aucun service d'IA.

## Prérequis

- Un serveur web en HTTPS. HTTPS est obligatoire pour l'installation sur téléphone et le fonctionnement hors ligne.
- PHP 8.1 ou plus, avec l'extension `pdo_sqlite`.
- Environ 3 Mo de disque pour l'application, plus quelques ko par utilisateur.

## Installation

1. Copier le dossier `parcours/` sous la racine web, par exemple pour obtenir `https://outils.sattse.com/parcours/`.
2. Vérifier que `parcours/config.json` contient `{"syncUrl": "api/sync.php"}`.
3. Ouvrir `parcours/api/config.php` et régler :
   - `data_dir` : le dossier de la base SQLite. Le placer de préférence hors de la racine web, par exemple `/var/lib/parcours-ia`. Le serveur web doit pouvoir y écrire.
   - `auth_mode` : `local` (comptes créés dans l'application) ou `remote_user` (identité fournie par le serveur, voir plus bas).
   - `allowed_domains` : les domaines autorisés à créer un compte, `sattse.com` par défaut.
   - `open_registration` : `false` pour réserver la création de comptes à l'administrateur.
4. Tester : `php parcours/api/sync.php selftest` doit afficher `selftest OK`.
5. Ouvrir l'adresse dans un navigateur, aller dans Profil : le bloc « Compte » apparaît.

### Apache

Les fichiers `.htaccess` fournis font deux choses : ils transmettent l'en-tête `Authorization` à PHP et ils interdisent l'accès web à `config.php` et au dossier `data/`. Il faut que `AllowOverride` les autorise. Sinon, reporter ces règles dans la configuration du site.

### Nginx

```nginx
location ~ ^/parcours/api/(data/|config\.php) { deny all; }
location ~ ^/parcours/api/sync\.php$ {
    include fastcgi_params;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    fastcgi_param HTTP_AUTHORIZATION $http_authorization;
    fastcgi_pass unix:/run/php/php-fpm.sock;
}
```

## Deux modes de compte

**Mode `local` (par défaut).** L'utilisateur crée son compte dans l'application avec son courriel professionnel et un mot de passe de 10 caractères minimum.
- Les mots de passe sont hachés avec `password_hash`.
- Les jetons de connexion (180 jours par défaut) sont stockés hachés.
- Un compte est verrouillé 15 minutes après 10 essais erronés.

**Mode `remote_user`.** Ce mode réutilise l'authentification existante (SSO, LDAP ou Active Directory, authentification HTTP).
- Le serveur web protège `parcours/api/sync.php` et transmet l'identifiant dans `REMOTE_USER`.
- L'application n'affiche alors aucun formulaire et ne gère aucun mot de passe.
- Le reste de `parcours/` peut rester public : le contenu est générique.

## Administration

```
php parcours/api/sync.php list                      # comptes et dernière synchronisation
php parcours/api/sync.php add <courriel> <mdp>      # créer un compte
php parcours/api/sync.php passwd <courriel> <mdp>   # nouveau mot de passe (déconnecte les appareils)
php parcours/api/sync.php delete <courriel>         # supprimer compte et progression
```

## Données conservées

Le fichier `parcours.sqlite` contient trois tables :
- `users` : courriel, empreinte du mot de passe, compteur d'échecs ;
- `tokens` : empreintes des jetons, échéance ;
- `saves` : la progression au format JSON. On y trouve l'XP, les étapes validées, les réponses aux questions, les défis relevés et les notes libres du carnet d'étape.

L'application demande de ne saisir aucune donnée de dossier dans le carnet. Ces données personnelles (courriel et progression de formation) relèvent du registre des traitements. Un utilisateur qui quitte la SATT se supprime avec la commande `delete`.

Sauvegarde : copier `parcours.sqlite`. Cette copie est sûre quand le serveur est arrêté, ou avec `sqlite3 parcours.sqlite ".backup copie.sqlite"`.

## Mises à jour

Le contenu de la formation est mis à jour chaque semaine. Pour une mise à jour, remplacer tout le dossier `parcours/` **sauf** trois éléments :
- `config.json` ;
- `api/config.php` ;
- le dossier de données.

Les navigateurs récupèrent la nouvelle version au prochain chargement, et la progression des utilisateurs est conservée.

## Comportement de la synchronisation

- L'application synchronise à l'ouverture, au retour du réseau, et 2,5 secondes après chaque progression.
- Elle récupère d'abord la sauvegarde du serveur, la fusionne avec celle de l'appareil, puis renvoie le résultat.
- La fusion ne retire rien : une étape validée, un exercice coché ou un défi relevé sur un appareil le reste partout.

## Désinstallation

Supprimer le dossier `parcours/` et le dossier de données.
