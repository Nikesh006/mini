<?php
session_start();
include("config/db.php");

if(!isset($_SESSION['admin'])){
    header("Location: login.php");
    exit();
}

/* COUNTS */
$totalMembers = mysqli_num_rows(mysqli_query($conn,"SELECT * FROM members"));
$totalAttendance = mysqli_num_rows(mysqli_query($conn,"SELECT * FROM attendance"));
$totalRevenue = mysqli_fetch_assoc(mysqli_query($conn,"
    SELECT SUM(amount) as total FROM payments
"))['total'];

$today = date("Y-m-d");
$todayAttendance = mysqli_num_rows(mysqli_query($conn,"
    SELECT * FROM attendance WHERE date='$today'
"));
?>

<!DOCTYPE html>
<html>
<head>
<title>Dashboard</title>
<link rel="stylesheet" href="/gym/assets/css/style.css">
</head>
<body>

<div class="sidebar">
    <h2>🏋 NAMMUDE GYM</h2>
    <a href="/gym/dashboard.php">Dashboard</a>
    <a href="/gym/attendance/mark_attendance.php">Mark Attendance</a>
    <a href="/gym/auth/logout.php">Logout</a>
</div>

<div class="main">

<div class="topbar">
    <h3>Welcome, <?php echo $_SESSION['admin']; ?></h3>
</div>

<div class="cards">

<div class="card">
    <h3>Total Members</h3>
    <h1><?php echo $totalMembers; ?></h1>
</div>

<div class="card">
    <h3>Total Attendance</h3>
    <h1><?php echo $totalAttendance; ?></h1>
</div>

<div class="card">
    <h3>Today's Attendance</h3>
    <h1><?php echo $todayAttendance; ?></h1>
</div>

<div class="card">
    <h3>Total Revenue</h3>
    <h1>₹ <?php echo $totalRevenue ? $totalRevenue : 0; ?></h1>
</div>

</div>

</div>
</body>
</html>