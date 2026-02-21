<?php
include("../config/db.php");
include("../layout/header.php");

if(isset($_POST['add'])){

    $name = $_POST['name'];
    $phone = $_POST['phone'];
    $join_date = $_POST['join_date'];

    mysqli_query($conn,"
        INSERT INTO members (name, phone, join_date)
        VALUES ('$name','$phone','$join_date')
    ");

    echo "<script>window.location='view_members.php'</script>";
}
?>

<div class="glass-card">
    <h2>Add New Member</h2>

    <form method="POST" class="glass-form">
        <input type="text" name="name" placeholder="Member Name" required>
        <input type="text" name="phone" placeholder="Phone Number" required>
        <input type="date" name="join_date" required>

        <button type="submit" name="add" class="btn success">
            Add Member
        </button>
    </form>
</div>

<?php include("../layout/footer.php"); ?>