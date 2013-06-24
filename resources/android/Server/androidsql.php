<?php
//These variables are sent from the users phone.
// Format is:
// $php_variable = $_POST["python_variable"];

// INPUTS WILL NEED TO BE SANITIZED
// CURRENT SETUP IS VULNERABLE

$subject_number = $_POST["subject_number"];
$trial = $_POST["trial"];
$type = $_POST["type"];
$question = $_POST["question"];
$response = $_POST["response"];
$probe = $_POST["probe"];
$colour = $_POST["colour"];
$response = $_POST["response"];
$rt = $_POST["rt"];
$xList = $_POST["xList"];
$yList = $_POST["yList"];
$tList = $_POST["tList"];

// Replace the following with the details of your own SQL database.
$host = "HOSTNAME.COM";
// e.g. $host = "cogsci.nl";
$database = "DATABASE_NAME";
$username = "USERNAME";
$password = "PASSWORD";

$con = mysql_connect($host, $username,$password);
mysql_select_db($database, $con) or die( "Unable to select database");


//Format:

// mysql_query("INSERT INTO table_name (column_name1, column_name2, ..., column_nameN)
// VALUES ('$php_variable1', '$php_variable2', ..., '$php_variableN')");
 
mysql_query("INSERT INTO OS_Android_Test1 (subject_number, trial,  trial_type,  question,  response,
				probe,  colour,  rt,  xList,  yList,  tList)
VALUES ('$subject_number', '$trial', '$type', '$question', '$response',
			'$probe', '$colour', '$rt', '$xList', '$yList', '$tList')");

mysql_close($con);


?>
