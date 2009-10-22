<?php
///////////////////////////////////////////////////////////////////////////////
// Act like the webserver
//
// WARNING: only use this tool if you know what you are doing. Leaving this
// script unattended on a public webserver can cause serious problems.
// You should at the very least change the secret (password) below.
//
// Act like the webserver is a lightweight (aka quick and dirty) tool to
// execute commands with the same permissions as the webserver.
// This can be usefull to fix permission issues on certain hosting setups where
// you have limited permissions. E.g. a web application created files (owned
// by the webserver user consequently) and you can't manipulate them through
// FTP or SSH because that involves a different user.
// With this script you can invoke the appropriate remove/delete commands
// executed by the webserver user.
///////////////////////////////////////////////////////////////////////////////


// SETTINGS ///////////////////////////////////////////////////////////////////
// Do not forget to change the secret.
$secret = 'bar';
// Allow command through HTTP POSTs?
$allow_post = TRUE;
// Allow commands through HTTP GETS?
$allow_get = FALSE;


function handle_post_request($data) {
    global $allow_post;
    if (!$allow_post) {
        print 'Get off my lawn, you poster!';
        exit();
    }
    handle_data($data);
}

function handle_get_request($data) {
    global $allow_get;
    if (!$allow_get) {
        print 'Get off my lawn, you getter!';
        exit();
    }
    handle_data($data);
}

function handle_data($data) {
    header("Content-Type: text/plain");

    global $secret;
    $password = isset($data['secret']) ? $data['secret'] : NULL;
    if ($password != $secret) {
        print 'Get off my lawn, you trespasser!';
        exit();
    }

    if (isset($data['command'])) {
        $command = $data['command'];
        system($command);
    }

}


function show_form() {
    print '<html>';
    print '<head><title>Act like you\'re the webserver!</title></head>';
    print '<body>';
    print '<form action="'. $_SELF .'" method="post">';
    print '<div><label for="command">Command</label><input type="text" title="Command" value="echo hello world" maxlength="60" size="60" name="command" /></div>';
    print '<div><label for="secret">Secret</label><input type="text" title="Secret" value="" maxlength="20" size="20" name="secret" /></div>';
    print '<div><input type="submit" value="Do it!" name="submit" /></div>';
    print '</form>';
    print '</body>';
    print '</html>';
}


// ENTRY POINT ////////////////////////////////////////////////////////////////
if (count($_POST) > 0) {
    handle_post_request($_POST);
}
else if (count($_GET) > 0) {
    handle_get_request($_GET);
}
else {
    show_form();
}

