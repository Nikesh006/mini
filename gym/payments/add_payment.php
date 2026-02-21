<?php
include("../config/db.php");
include("../layout/header.php");

$members = mysqli_query($conn,"SELECT * FROM members");

if(isset($_POST['add'])){

    $member_id = $_POST['member_id'];
    $amount = $_POST['amount'];

    mysqli_query($conn,"
        INSERT INTO payments (member_id, amount, payment_date)
        VALUES ('$member_id','$amount', CURDATE())
    ");

    echo "<script>window.location='view_payments.php'</script>";
}
?>

<div class="glass-card">
    <h2>Add Payment</h2>

    <form method="POST">

        <label>Select Member</label>
        <select name="member_id" required>
            <?php while($m = mysqli_fetch_assoc($members)){ ?>
                <option value="<?php echo $m['id']; ?>">
                    <?php echo $m['name']; ?>
                </option>
            <?php } ?>
        </select>

        <label>Amount</label>
        <input type="number" name="amount" placeholder="Enter Amount" required>

        <button type="submit" name="add" class="btn-success">
            <span class="icon">💰</span> Add Payment
        </button>

    </form>
</div>

<?php include("../layout/footer.php"); ?>