<?php
include("../config/db.php");
include("../layout/header.php");

$payments = mysqli_query($conn,"
    SELECT payments.*, members.name
    FROM payments
    JOIN members ON payments.member_id = members.id
    ORDER BY payments.id DESC
");

$totalQuery = mysqli_query($conn,"SELECT SUM(amount) as total FROM payments");
$totalData = mysqli_fetch_assoc($totalQuery);
$totalRevenue = $totalData['total'] ?? 0;
?>

<div class="glass-card">

    <div class="payments-header">
        <h2>All Payments</h2>

        <div style="display:flex; gap:10px;">
            <a href="export_payments.php" class="btn-add">
                📊 Export Excel
            </a>

            <a href="add_payment.php" class="btn-add">
                💰 Add Payment
            </a>
        </div>
    </div>

    <div class="glass-card" style="text-align:center; margin-bottom:20px;">
        <h4>Total Revenue</h4>
        <h1>₹ <?php echo number_format($totalRevenue,2); ?></h1>
    </div>

    <table>
        <table class="glass-table">
        <thead>
            <tr>
                <th>Member</th>
                <th>Amount</th>
                <th>Date</th>
                <th>Invoice</th>
            </tr>
        </thead>
        <tbody>
        <?php while($row = mysqli_fetch_assoc($payments)){ ?>
            <tr>
                <td><?php echo $row['name']; ?></td>
                <td class="amount">₹ <?php echo number_format($row['amount'],2); ?></td>
                <td><?php echo $row['payment_date']; ?></td>
                <td>
                    <a href="invoice.php?id=<?php echo $row['id']; ?>" class="btn-success">
                        🧾 Invoice
                    </a>
                </td>
            </tr>
        <?php } ?>
        </tbody>
    </table>

</div>

<?php include("../layout/footer.php"); ?>