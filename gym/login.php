<?php
session_start();
include("config/db.php");

$error="";
$success="";

/* LOGIN */
if(isset($_POST['login'])){
    $username=$_POST['username'];
    $password=md5($_POST['password']);

    $check=mysqli_query($conn,"SELECT * FROM admins WHERE username='$username' AND password='$password'");
    if(mysqli_num_rows($check)>0){
        $_SESSION['admin']=$username;
        header("Location: dashboard.php");
        exit();
    } else {
        $error="Invalid username or password";
    }
}

/* REGISTER */
if(isset($_POST['register'])){
    $username=$_POST['reg_username'];
    $email=$_POST['reg_email'];
    $password=md5($_POST['reg_password']);

    $exists=mysqli_query($conn,"SELECT * FROM admins WHERE username='$username'");
    if(mysqli_num_rows($exists)>0){
        $error="Username already exists";
    } else {
        mysqli_query($conn,"INSERT INTO admins(username,email,password)
        VALUES('$username','$email','$password')");
        $success="Registration successful! Please login.";
    }
}
?>

<!DOCTYPE html>
<html>
<head>
<title>NAMMUDE GYM</title>
<link rel="stylesheet" href="assets/css/login.css">

<script>
function toggleForm(){
    document.getElementById("loginForm").classList.toggle("hidden");
    document.getElementById("registerForm").classList.toggle("hidden");
}

function togglePassword(id){
    const pass=document.getElementById(id);
    pass.type=pass.type==="password"?"text":"password";
}
</script>

</head>
<body>

<div id="tsparticles"></div>

<div class="container">

<div class="left">
    <h1 class="logo">🏋NAMMUDE GYM</h1>
    <p>Manage your fitness business like a pro with modern SaaS tools.</p>
</div>

<div class="right">

<div class="card">

<?php if($error!=""){ ?>
<div class="error"><?php echo $error; ?></div>
<?php } ?>

<?php if($success!=""){ ?>
<div class="success"><?php echo $success; ?></div>
<?php } ?>

<!-- LOGIN -->
<form method="POST" id="loginForm">
<h2>Login</h2>

<input type="text" name="username" placeholder="Username" required>

<div class="password-box">
<input type="password" id="loginPass" name="password" placeholder="Password" required>
<span onclick="togglePassword('loginPass')">👁</span>
</div>

<button name="login">Login</button>
<p class="switch" onclick="toggleForm()">Don't have account? Register</p>
</form>

<!-- REGISTER -->
<form method="POST" id="registerForm" class="hidden">
<h2>Register</h2>

<input type="text" name="reg_username" placeholder="Username" required>
<input type="email" name="reg_email" placeholder="Email" required>

<div class="password-box">
<input type="password" id="regPass" name="reg_password" placeholder="Password" required>
<span onclick="togglePassword('regPass')">👁</span>
</div>

<button name="register">Register</button>
<p class="switch" onclick="toggleForm()">Already have account? Login</p>
</form>

</div>
</div>
</div>

<!-- PARTICLES -->
<script src="https://cdn.jsdelivr.net/npm/tsparticles@2/tsparticles.bundle.min.js"></script>
<script>
tsParticles.load("tsparticles", {
  background: { color: "transparent" },
  fpsLimit: 60,
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