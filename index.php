<!DOCTYPE HTML>
<html>
<?php
$linetest=2;

$line = file_get_contents( "Parameters.txt" ); 
//}
echo("
<body>
<form method='POST' action='WritePar.php'>
	<table>

		<tr>
			<td>Ani allowed time (min):</td>
			<td><input type='text' id='Mins' value='$line' name='get_minutes'></input></td>
			<td><button onclick=''>Save</button></td>

		</tr>
	</table>
</form>");
if(isset($_GET['message'])){
  echo $_GET['message'];
}

echo("
</body>
</html>");
?>