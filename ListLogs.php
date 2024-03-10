<!DOCTYPE HTML>
<html>
<head>
  <title>Usage log</title>
  <link rel="stylesheet" type="text/css" href="home.css">
  <meta charset="UTF-8">
</head>
<body>
  <main>
<?php
$directory = "/var/www/html/admin/myserver";
$htmlFiles = glob("$directory/*.{html,htm}", GLOB_BRACE);
foreach($htmlFiles as $phpfile)
{
    echo '<a href="'.basename($phpfile).'">'.$phpfile.'</a><br>';
}
echo("
  </main>
</body>
</html>");
?>