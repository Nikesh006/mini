<?php
session_start();
include("../config/db.php");
include("../layout/header.php");

$today = date("Y-m-d");

/* ================= CHECK IN ================= */
if(isset($_POST['checkin'])){

    $member_id = $_POST['member_id'];

    // Check if member currently inside (no checkout yet)
    $check = mysqli_query($conn,"
        SELECT * FROM attendance
        WHERE member_id='$member_id'
        AND attendance_date='$today'
        AND check_out IS NULL
    ");

    if(mysqli_num_rows($check) == 0){

        // Allow new check-in
        mysqli_query($conn,"
            INSERT INTO attendance(member_id, attendance_date, check_in)
            VALUES('$member_id','$today', CURTIME())
        ");

        $_SESSION['msg'] = "Check-In Successful!";
        $_SESSION['type'] = "success";

    } else {

        $_SESSION['msg'] = "Member already inside gym!";
        $_SESSION['type'] = "error";
    }

    header("Location: mark_attendance.php");
    exit();
}


/* ================= CHECK OUT ================= */
if(isset($_POST['checkout'])){

    $member_id = $_POST['member_id'];

    // Find latest active session
    $check = mysqli_query($conn,"
        SELECT * FROM attendance
        WHERE member_id='$member_id'
        AND attendance_date='$today'
        AND check_out IS NULL
        ORDER BY id DESC
        LIMIT 1
    ");

    if(mysqli_num_rows($check) == 0){

        $_SESSION['msg'] = "Member not inside!";
        $_SESSION['type'] = "warning";

    } else {

        $row = mysqli_fetch_assoc($check);

        mysqli_query($conn,"
            UPDATE attendance
            SET check_out = CURTIME()
            WHERE id='".$row['id']."'
        ");

        $_SESSION['msg'] = "Check-Out Successful!";
        $_SESSION['type'] = "success";
    }

    header("Location: mark_attendance.php");
    exit();
}


/* ================= MEMBERS INSIDE ================= */
$inside = mysqli_query($conn,"
    SELECT members.name, attendance.check_in
    FROM attendance
    JOIN members ON attendance.member_id = members.id
    WHERE attendance.attendance_date='$today'
    AND attendance.check_out IS NULL
");

/* ================= ALL MEMBERS ================= */
$members = mysqli_query($conn,"SELECT * FROM members");
?>

<!-- ================= TOAST MESSAGE ================= -->
<?php if(isset($_SESSION['msg'])){ ?>
<div class="toast <?php echo $_SESSION['type']; ?>">
    <?php echo $_SESSION['msg']; ?>
</div>
<?php 
unset($_SESSION['msg']);
unset($_SESSION['type']);
} ?>

<div class="glass-card">
    <h2>Attendance System</h2>

    <form method="POST">
        <select name="member_id" required>
            <?php while($m = mysqli_fetch_assoc($members)){ ?>
                <option value="<?php echo $m['id']; ?>">
                    <?php echo $m['name']; ?>
                </option>
            <?php } ?>
        </select>

        <button type="submit" name="checkin" class="btn-success">
            ✅ Check In
        </button>

        <button type="submit" name="checkout" class="btn-danger">
            ⏹ Check Out
        </button>
    </form>
</div>


<!-- ================= MEMBERS INSIDE SECTION ================= -->

<div class="glass-card" style="margin-top:30px;">
    <h2>🏋 Members Inside Gym</h2>

    <table class="glass-table">
        <thead>
            <tr>
                <th>Member</th>
                <th>Check In Time</th>
            </tr>
        </thead>

        <tbody>
        <?php while($row = mysqli_fetch_assoc($inside)){ ?>
            <tr>
                <td><?php echo $row['name']; ?></td>
                <td><?php echo $row['check_in']; ?></td>
            </tr>
        <?php } ?>
        </tbody>
    </table>
</div>

<?php include("../layout/footer.php"); ?>