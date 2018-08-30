<?php

include 'db_config.php';

//Connecting to SQL server
header('Content-Type: application/json');
$connectionInfo = array("Database"=>$DATABASE_NAME, "UID"=>$HOST_USER, "PWD"=>$HOST_PASSWORD);

error_log("Attempting to connect to DB" + $HOST);
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

$query = "SELECT Timestamp, Temperature, Humidity FROM MachineSensorData";
$stmt = sqlsrv_query($conn, $query);

if ($stmt === false) {
    die(print_r(sqlsrv_errors(), true));
}

$data = array();

while ($row = sqlsrv_fetch_array($stmt, SQLSRV_FETCH_NUMERIC)) {
    $data[] = $row;
}

print_r($data);

$json = json_encode($data);
print_r($json);
echo json_encode($json);