<?php
$allowed_hours = $_POST['get_minutes'];
$fname ="Parameters.txt";
file_put_contents($fname, $allowed_hours);
//echo $allowed_hours;
$message = '';
if(isset($_POST['get_minutes'])){
	$message = urlencode("$allowed_hours minutes saved to memory");
	$url = $_SERVER[HTTP_REFERER];
	$url = strtok($url, "?");
	header("Location:".$url."?message=".$message);
	die;
}
?>