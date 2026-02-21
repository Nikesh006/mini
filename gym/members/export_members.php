<?php
include("../config/db.php");

header("Content-Type: application/vnd.ms-excel");
header("Content-Disposition: attachment; filename=members.xls");

$result=mysqli_query($conn,"SELECT * FROM members");

echo "Name\tPhone\tEmail\tPlan\tExpiry\n";
while($row=mysqli_fetch_assoc($result)){
echo $row['name']."\t".$row['phone']."\t".$row['email']."\t".$row['plan']."\t".$row['expiry_date']."\n";
}
?>