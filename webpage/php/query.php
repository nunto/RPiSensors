<?php

include 'db_config.php';

// Connecting to SQL server
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: Origin, Content-Type, Accept");
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
$query = $obj["query"];

$stmt = sqlsrv_query($conn, $query);

if ($stmt === false) {
    die(print_r(sqlsrv_errors(), true));
}

$data = array();

// Appending results into array
while ($row = sqlsrv_fetch_array($stmt, SQLSRV_FETCH_NUMERIC)) {
    $data[] = $row;
}

// Sending back data
$json = json_encode($data);
echo json_encode($json);