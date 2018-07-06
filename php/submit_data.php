<?php

include 'db_config.php';

// Connecting to SQL server
header('Content-Type: application/json');
$connectionInfo = array("Database"=>$DATABASE_NAME, "UID"=>$HOST_USER, "PWD"=>$HOST_PASSWORD);

error_log("Attempting to connect to DB");
$conn = sqlsrv_connect($HOST, $connectionInfo);

// Log errors in the case of a failed connection
if ($conn === false) {
    echo json_encode("Could not connect to sqlsrv");
    if (($errors = sqlsrv_errors()) != null) {
        foreach($errors as $error) {
            error_log("SQLSTATE: ".$error[ 'SQLSTATE']."<br />");
            error_log("code: ".$error[ 'code']."<br />");
            error_log("message: ".$error[ 'message']."<br />");
        }
    }
    die();
} 
else {
    // Success log messages
    error_log("Connection successful");
}

// Retrieving the JSON contents sent from the Scanner
$json = file_get_contents("php://input");

$obj = json_decode($json, true);

// Unpacking JSON info
$temp = $obj["temp"];

$humidity = $obj["humidity"];

// Query retrieved data into the db
$query = "INSERT INTO TempHumidity(Temperature, Humidity) values ('$temp', '$humidity')";
$insert = sqlsrv_query($conn, $query);

// Log errors in the case of a failed query
// Return a JSON response to the application which initialized this
if ($insert === false) {
    echo json_encode("Query failed.");
    if (($errors = sqlsrv_errors()) != null) {
        foreach($errors as $error) {
            error_log("SQLSTATE: ".$error[ 'SQLSTATE']."<br />");
            error_log("code: ".$error[ 'code']."<br />");
            error_log("message: ".$error[ 'message']."<br />");
        }
    }
} else {
    echo json_encode("Query Successful!");
}

// Close connection to SQL Server
sqlsrv_close($conn);
?>