<?php
include("../config/db.php");

header("Content-Type: application/vnd.ms-excel");
header("Content-Disposition: attachment; filename=payments_report.xls");

echo "Member\tAmount\tDate\n";

$query = mysqli_query($conn,"
    SELECT payments.*, members.name
    FROM payments
    JOIN members ON payments.member_id = members.id
");

while($row = mysqli_fetch_assoc($query)){
    echo $row['name'] . "\t";
    echo $row['amount'] . "\t";
    echo $row['payment_date'] . "\n";
}
exit();
?>