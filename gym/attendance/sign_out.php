<?php
include("../config/db.php");

$member_id = $_GET['id'];

mysqli_query($conn,"
    UPDATE attendance 
    SET sign_out=NOW() 
    WHERE member_id='$member_id' 
    AND sign_out IS NULL
");

header("Location: view_attendance.php");
?>