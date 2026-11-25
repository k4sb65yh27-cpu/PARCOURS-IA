<?php
/*
 * Parcours IA : synchronisation de la progression par compte.
 * Un seul fichier, PHP 8.1 ou plus avec pdo_sqlite. Aucune dépendance.
 *
 * Web (JSON, même origine que l'application) :
 *   POST sync.php?a=register  {email, password}      -> {token, email}
 *   POST sync.php?a=login     {email, password}      -> {token, email}
 *   POST sync.php?a=logout                           -> {ok}
 *   GET  sync.php?a=me                               -> {email, mode}
 *   GET  sync.php?a=pull                             -> {data, updatedAt}
 *   PUT  sync.php?a=push      {data, updatedAt}      -> {ok, updatedAt}
 *   Jeton : en-tête « Authorization: Bearer <jeton> » (mode local).
 *
 * Ligne de commande (administrateur) :
 *   php sync.php list
 *   php sync.php add <courriel> <mot de passe>
 *   php sync.php passwd <courriel> <mot de passe>
 *   php sync.php delete <courriel>
 *   php sync.php selftest
 */
declare(strict_types=1);

$C = require __DIR__ . '/config.php';

function db(array $C): PDO {
    static $pdo = null;
    if ($pdo) return $pdo;
    if (!is_dir($C['data_dir']) && !mkdir($C['data_dir'], 0700, true)) throw new RuntimeException('data_dir');
    $pdo = new PDO('sqlite:' . $C['data_dir'] . '/parcours.sqlite', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
    $pdo->exec('PRAGMA journal_mode=WAL; PRAGMA busy_timeout=3000;');
    $pdo->exec('CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, hash TEXT, created INTEGER, fails INTEGER DEFAULT 0, fail_at INTEGER DEFAULT 0)');
    $pdo->exec('CREATE TABLE IF NOT EXISTS tokens (hash TEXT PRIMARY KEY, email TEXT, expires INTEGER)');
    $pdo->exec('CREATE TABLE IF NOT EXISTS saves (email TEXT PRIMARY KEY, data TEXT, updated INTEGER, saved_at INTEGER)');
    return $pdo;
}

function norm_email(string $e): string { return strtolower(trim($e)); }

function valid_email(array $C, string $e): bool {
    if (!filter_var($e, FILTER_VALIDATE_EMAIL)) return false;
    if (!$C['allowed_domains']) return true;
    $dom = substr(strrchr($e, '@'), 1);
    return in_array($dom, $C['allowed_domains'], true);
}

function set_password(array $C, string $email, string $pw): void {
    $st = db($C)->prepare('INSERT INTO users(email, hash, created) VALUES(?, ?, ?) ON CONFLICT(email) DO UPDATE SET hash = excluded.hash, fails = 0');
    $st->execute([$email, password_hash($pw, PASSWORD_DEFAULT), time()]);
}

function new_token(array $C, string $email): string {
    $t = bin2hex(random_bytes(32));
    db($C)->prepare('INSERT INTO tokens VALUES(?, ?, ?)')->execute([hash('sha256', $t), $email, time() + 86400 * $C['token_days']]);
    db($C)->prepare('DELETE FROM tokens WHERE expires < ?')->execute([time()]);
    return $t;
}

/* ---------- Ligne de commande ---------- */
if (PHP_SAPI === 'cli') {
    [$cmd, $a, $b] = array_pad(array_slice($argv, 1), 3, '');
    $email = norm_email($a);
    switch ($cmd) {
        case 'list':
            foreach (db($C)->query('SELECT u.email, s.saved_at FROM users u LEFT JOIN saves s ON s.email = u.email ORDER BY u.email') as $r)
                echo $r['email'], "\t", $r['saved_at'] ? date('Y-m-d H:i', (int)$r['saved_at']) : 'jamais synchronisé', "\n";
            break;
        case 'add':
        case 'passwd':
            if (!$email || strlen($b) < 10) exit("Courriel et mot de passe de 10 caractères minimum.\n");
            set_password($C, $email, $b);
            db($C)->prepare('DELETE FROM tokens WHERE email = ?')->execute([$email]);
            echo "OK\n";
            break;
        case 'delete':
            foreach (['users', 'tokens', 'saves'] as $t) db($C)->prepare("DELETE FROM $t WHERE email = ?")->execute([$email]);
            echo "Supprimé (compte, connexions et progression).\n";
            break;
        case 'selftest':
            $C['data_dir'] = sys_get_temp_dir() . '/parcours-selftest-' . getmypid();
            set_password($C, 'test@sattse.com', 'motdepasse-test');
            $u = db($C)->query("SELECT hash FROM users WHERE email = 'test@sattse.com'")->fetch();
            assert(password_verify('motdepasse-test', $u['hash']));
            assert(valid_email($C, 'a@sattse.com') && !valid_email($C, 'a@gmail.com'));
            $t = new_token($C, 'test@sattse.com');
            assert(strlen($t) === 64);
            echo "selftest OK\n";
            break;
        default:
            echo "Commandes : list | add <courriel> <mdp> | passwd <courriel> <mdp> | delete <courriel> | selftest\n";
    }
    exit;
}

/* ---------- Web ---------- */
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');

function out(int $code, array $body): never { http_response_code($code); echo json_encode($body, JSON_UNESCAPED_UNICODE); exit; }
function body(array $C): array {
    $raw = file_get_contents('php://input', false, null, 0, $C['max_bytes'] + 1);
    if (strlen((string)$raw) > $C['max_bytes']) out(413, ['error' => 'Sauvegarde trop volumineuse.']);
    $j = json_decode((string)$raw, true);
    return is_array($j) ? $j : [];
}
function who(array $C): string {
    if ($C['auth_mode'] === 'remote_user') {
        $u = $_SERVER['REMOTE_USER'] ?? $_SERVER['REDIRECT_REMOTE_USER'] ?? '';
        if ($u === '') out(401, ['error' => 'Authentification du serveur absente.']);
        return norm_email($u);
    }
    $h = $_SERVER['HTTP_AUTHORIZATION'] ?? $_SERVER['REDIRECT_HTTP_AUTHORIZATION'] ?? '';
    if (!preg_match('/^Bearer\s+([a-f0-9]{64})$/', $h, $m)) out(401, ['error' => 'Connexion requise.']);
    $st = db($C)->prepare('SELECT email FROM tokens WHERE hash = ? AND expires > ?');
    $st->execute([hash('sha256', $m[1]), time()]);
    $e = $st->fetchColumn();
    if (!$e) out(401, ['error' => 'Connexion expirée.']);
    return (string)$e;
}

$a = $_GET['a'] ?? '';
$m = $_SERVER['REQUEST_METHOD'];
try {
    if ($a === 'register' && $m === 'POST') {
        if ($C['auth_mode'] !== 'local' || !$C['open_registration']) out(403, ['error' => 'Création de compte fermée : demandez un compte à votre administrateur.']);
        $j = body($C); $email = norm_email((string)($j['email'] ?? '')); $pw = (string)($j['password'] ?? '');
        if (!valid_email($C, $email)) out(400, ['error' => 'Utilisez votre adresse professionnelle.']);
        if (strlen($pw) < 10) out(400, ['error' => 'Mot de passe de 10 caractères minimum.']);
        $st = db($C)->prepare('SELECT 1 FROM users WHERE email = ?'); $st->execute([$email]);
        if ($st->fetchColumn()) out(409, ['error' => 'Ce compte existe déjà : connectez-vous.']);
        set_password($C, $email, $pw);
        out(200, ['token' => new_token($C, $email), 'email' => $email]);
    }
    if ($a === 'login' && $m === 'POST') {
        if ($C['auth_mode'] !== 'local') out(400, ['error' => 'Connexion gérée par le serveur.']);
        $j = body($C); $email = norm_email((string)($j['email'] ?? '')); $pw = (string)($j['password'] ?? '');
        $st = db($C)->prepare('SELECT hash, fails, fail_at FROM users WHERE email = ?'); $st->execute([$email]);
        $u = $st->fetch(PDO::FETCH_ASSOC);
        // Verrou après 10 échecs, levé au bout de 15 minutes.
        if ($u && $u['fails'] >= 10 && time() - (int)$u['fail_at'] < 900) out(429, ['error' => 'Trop d\'essais. Réessayez dans 15 minutes.']);
        if (!$u || !password_verify($pw, $u['hash'])) {
            if ($u) db($C)->prepare('UPDATE users SET fails = fails + 1, fail_at = ? WHERE email = ?')->execute([time(), $email]);
            usleep(400000);
            out(401, ['error' => 'Courriel ou mot de passe incorrect.']);
        }
        db($C)->prepare('UPDATE users SET fails = 0 WHERE email = ?')->execute([$email]);
        out(200, ['token' => new_token($C, $email), 'email' => $email]);
    }
    if ($a === 'logout' && $m === 'POST') {
        $h = $_SERVER['HTTP_AUTHORIZATION'] ?? $_SERVER['REDIRECT_HTTP_AUTHORIZATION'] ?? '';
        if (preg_match('/^Bearer\s+([a-f0-9]{64})$/', $h, $mm)) db($C)->prepare('DELETE FROM tokens WHERE hash = ?')->execute([hash('sha256', $mm[1])]);
        out(200, ['ok' => true]);
    }
    if ($a === 'me' && $m === 'GET') out(200, ['email' => who($C), 'mode' => $C['auth_mode']]);
    if ($a === 'pull' && $m === 'GET') {
        $st = db($C)->prepare('SELECT data, updated FROM saves WHERE email = ?'); $st->execute([who($C)]);
        $r = $st->fetch(PDO::FETCH_ASSOC);
        out(200, ['data' => $r ? json_decode($r['data'], true) : null, 'updatedAt' => $r ? (int)$r['updated'] : 0]);
    }
    if ($a === 'push' && $m === 'PUT') {
        $email = who($C); $j = body($C);
        if (!isset($j['data']['state']) || !is_array($j['data']['state'])) out(400, ['error' => 'Sauvegarde invalide.']);
        $upd = (int)($j['updatedAt'] ?? 0);
        db($C)->prepare('INSERT INTO saves VALUES(?, ?, ?, ?) ON CONFLICT(email) DO UPDATE SET data = excluded.data, updated = excluded.updated, saved_at = excluded.saved_at')
            ->execute([$email, json_encode($j['data'], JSON_UNESCAPED_UNICODE), $upd, time()]);
        out(200, ['ok' => true, 'updatedAt' => $upd]);
    }
    out(404, ['error' => 'Action inconnue.']);
} catch (Throwable $e) {
    error_log('parcours sync: ' . $e->getMessage());
    out(500, ['error' => 'Erreur du serveur de synchronisation.']);
}
