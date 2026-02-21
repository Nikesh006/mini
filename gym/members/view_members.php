<?php
include("../config/db.php");
include("../layout/header.php");

$members = mysqli_query($conn,"SELECT * FROM members ORDER BY id DESC");
?>

<div class="glass-card">

    <div class="members-header">
        <h2>All Members</h2>

        <a href="add_member.php" class="btn-add">
            <span>+ Add Member</span>
        </a>
    </div>

    <table class="glass-table">
        <thead>
            <tr>
                <th>Name</th>
                <th>Phone</th>
                <th>Join Date</th>
                <th>Actions</th>
            </tr>
        </thead>

        <tbody>
        <?php while($row = mysqli_fetch_assoc($members)) { ?>
            <tr>
                <td><?php echo $row['name']; ?></td>
                <td><?php echo $row['phone']; ?></td>
                <td><?php echo $row['join_date']; ?></td>
                <td class="action-buttons">

                    <a href="delete_member.php?id=<?php echo $row['id']; ?>" 
                       class="btn danger"
                       onclick="return confirm('Are you sure you want to delete this member?')">
                        Delete
                    </a>

                    <a href="../attendance/member_attendance.php?id=<?php echo $row['id']; ?>" 
                       class="btn success">
                        View Attendance
                    </a>

                </td>
            </tr>
        <?php } ?>
        </tbody>

    </table>

</div>

<?php include("../layout/footer.php"); ?>