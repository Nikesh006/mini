<?php
include("../config/db.php");
include("../layout/header.php");

$id = $_GET['id'];

$attendance = mysqli_query($conn,"
    SELECT *
    FROM attendance
    WHERE member_id='$id'
    ORDER BY attendance_date DESC
");
?>

<div class="glass-card">
    <h2>Attendance History</h2>

    <table class="glass-table">
        <thead>
            <tr>
                <th>Date</th>
                <th>Check In</th>
                <th>Check Out</th>
                <th>Duration</th>
            </tr>
        </thead>

        <tbody>
        <?php while($row = mysqli_fetch_assoc($attendance)){

            $duration = "-";

            if($row['check_in'] && $row['check_out']){
                $start = strtotime($row['check_in']);
                $end = strtotime($row['check_out']);
                $diff = $end - $start;
                $duration = gmdate("H:i:s",$diff);
            }
        ?>
            <tr>
                <td><?php echo $row['attendance_date']; ?></td>
                <td><?php echo $row['check_in'] ?? "-"; ?></td>
                <td><?php echo $row['check_out'] ?? "-"; ?></td>
                <td><?php echo $duration; ?></td>
            </tr>
        <?php } ?>
        </tbody>
    </table>
</div>

<?php include("../layout/footer.php"); ?>