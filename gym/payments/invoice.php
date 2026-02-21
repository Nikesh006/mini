<?php
include("../config/db.php");

$id = $_GET['id'];

$query = mysqli_query($conn,"
    SELECT payments.*, members.name
    FROM payments
    JOIN members ON payments.member_id = members.id
    WHERE payments.id='$id'
");

$data = mysqli_fetch_assoc($query);
?>

<!DOCTYPE html>
<html>
<head>
<title>Invoice</title>
<link rel="stylesheet" href="../assets/css/dashboard.css">
</head>
<body>

<div class="glass-card" style="max-width:600px;margin:40px auto;">

    <h2>🧾 Payment Invoice</h2>

    <p><strong>Member:</strong> <?php echo $data['name']; ?></p>
    <p><strong>Date:</strong> <?php echo $data['payment_date']; ?></p>
    <p><strong>Amount:</strong> ₹ <?php echo number_format($data['amount'],2); ?></p>

    <br>
    <button onclick="window.print()" class="btn-success">Print</button>

</div>

</body>
</html>