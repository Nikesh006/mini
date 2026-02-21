<?php
if(session_status() === PHP_SESSION_NONE){
    session_start();
}
if(!isset($_SESSION['admin'])){
    header("Location: /gym/login.php");
    exit();
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>NAMMUDE GYM</title>
    <link rel="stylesheet" href="/gym/assets/css/dashboard.css">
</head>
<body>

<div id="tsparticles"></div>

<div class="wrapper">

<div class="sidebar">
    <h2>🏋 NAMMUDE GYM</h2>
    <a href="/gym/dashboard.php">Dashboard</a>
    <a href="/gym/members/view_members.php">Members</a>
    <a href="/gym/attendance/mark_attendance.php">Attendance</a>
    <a href="/gym/payments/view_payments.php">Payments</a>
    <a href="/gym/auth/logout.php">Logout</a>
</div>

<div class="main">

<div class="topbar">
    <h3>Welcome, <?php echo htmlspecialchars($_SESSION['admin']); ?></h3>
</div>