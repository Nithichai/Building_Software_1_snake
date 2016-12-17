<?php
$con = mysqli_connect('localhost', 'root', 'yourname', 'GAME_DB');  // Connect mysql and database
if(!$con) {
    die('Error');   // Not connect => show error
}
$sql = "SELECT * FROM `GAME_TB`";
$result = mysqli_query($con, $sql);     // Get data from GAME_TB

// Echo all data to pattern
foreach($result as $row) {
    foreach($row as $col) {
        echo $col . ",";
    }
    echo "/";
}
mysqli_close($con);     // Disconnect database and mysql
?>