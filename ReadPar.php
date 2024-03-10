<?php
$myfile = fopen("Parameters.txt", "r") or die("Unable to open file!");
while ($line = fgets($myfile)) {
  // <... Do your work with the line ...>
   echo($line);
}
fclose($myfile);
?>