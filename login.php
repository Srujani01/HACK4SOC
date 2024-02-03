<?php
// Connect to database
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "mydatabase";

$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Retrieve POST data
$email = $_POST['email'];
$password = $_POST['password'];

// Check if user exists
$sql = "SELECT * FROM users WHERE email='$email' AND password='$password'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // User exists, login successful
    $response = array("success" => true);
} else {
    // User does not exist or password is incorrect
    $response = array("success" => false, "message" => "Invalid email or password");
}

// Return JSON response
header('Content-Type: application/json');
echo json_encode($response);

$conn->close();
?>
