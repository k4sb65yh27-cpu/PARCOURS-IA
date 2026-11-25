<?php
// Réglages de la synchronisation du Parcours IA. Seul fichier à adapter.
return [
    // Dossier des données (base SQLite). De préférence HORS de la racine web.
    'data_dir' => __DIR__ . '/data',

    // 'local' : comptes créés dans l'application (courriel professionnel + mot de passe).
    // 'remote_user' : identité fournie par le serveur web (SSO, LDAP, authentification HTTP) via REMOTE_USER ; aucun mot de passe géré ici.
    'auth_mode' => 'local',

    // Domaines de courriel autorisés à créer un compte (mode local). Vide = tous.
    'allowed_domains' => ['sattse.com'],

    // Création de compte ouverte (true) ou réservée à l'administrateur en ligne de commande (false).
    'open_registration' => true,

    // Durée de validité d'une connexion, en jours.
    'token_days' => 180,

    // Taille maximale d'une sauvegarde, en octets.
    'max_bytes' => 2 * 1024 * 1024,
];
