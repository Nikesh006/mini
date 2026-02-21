<?php
session_start();
include("config/db.php");

/* If not logged in redirect */
if(!isset($_SESSION['admin'])){
    header("Location: login.php");
    exit();
}

/* Safe default values */
$totalMembers = 0;
$totalAttendance = 0;
$totalRevenue = 0;

/* Fetch Members Count */
$membersQuery = mysqli_query($conn, "SELECT * FROM members");
if($membersQuery){
    $totalMembers = mysqli_num_rows($membersQuery);
}

/* Fetch Attendance Count */
$attendanceQuery = mysqli_query($conn, "SELECT * FROM attendance");
if($attendanceQuery){
    $totalAttendance = mysqli_num_rows($attendanceQuery);
}

/* Fetch Revenue */
$revenueQuery = mysqli_query($conn, "SELECT SUM(amount) as total FROM payments");
if($revenueQuery){
    $revData = mysqli_fetch_assoc($revenueQuery);
    if($revData && $revData['total'] != null){
        $totalRevenue = $revData['total'];
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
    <link rel="stylesheet" href="assets/css/dashboard.css">
</head>

<body>

<div id="tsparticles"></div>

<div class="wrapper">

    <!-- Sidebar -->
    <div class="sidebar">
        <h2>🏋 NAMMUDE GYM</h2>
        <a href="dashboard.php" class="active">Dashboard</a>
        <a href="members/view_members.php">Members</a>
        <a href="attendance/mark_attendance.php">Attendance</a>
        <a href="payments/view_payments.php">Payments</a>
        <a href="auth/logout.php">Logout</a>
    </div>

    <!-- Main -->
    <div class="main">

        <div class="topbar">
            <h3>Welcome, <?php echo htmlspecialchars($_SESSION['admin']); ?></h3>
        </div>

        <div class="cards">

            <div class="card">
                <h4>Total Members</h4>
                <h1><?php echo $totalMembers; ?></h1>
            </div>

            <div class="card">
                <h4>Total Attendance</h4>
                <h1><?php echo $totalAttendance; ?></h1>
            </div>

            <div class="card">
                <h4>Total Revenue</h4>
                <h1>₹ <?php echo number_format($totalRevenue,2); ?></h1>
            </div>

        </div>

    </div>

</div>

<!-- Particle Background -->
<script src="https://cdn.jsdelivr.net/npm/tsparticles@2/tsparticles.bundle.min.js"></script>
<script>
tsParticles.load("tsparticles", {
  background: { color: "transparent" },
  particles: {
    number: { value: 60 },
    color: { value: "#ffffff" },
    links: {
      enable: true,
      distance: 150,
      color: "#ffffff",
      opacity: 0.2,
      width: 1
    },
    move: { enable: true, speed: 1 },
    opacity: { value: 0.3 },
    size: { value: 2 }
  }
});
</script>

</body>
</html>