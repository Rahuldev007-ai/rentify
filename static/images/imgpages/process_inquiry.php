<?php
session_start();
include '../connection.php';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Get form data
    $name = $_POST['name'];
    $phone = $_POST['phone'];
    $email = $_POST['email'];
    $event_type = $_POST['event_type'];
    $event_date = $_POST['event_date'];
    $guest_count = $_POST['guest_count'];
    $requirements = $_POST['requirements'];

    // Insert into your existing contact or inquiries table
    $sql = "INSERT INTO contact (name, phone, email, message, created_at) 
            VALUES (?, ?, ?, ?, NOW())";
    
    $message = "Event Type: " . $event_type . "\n";
    $message .= "Event Date: " . $event_date . "\n";
    $message .= "Guest Count: " . $guest_count . "\n";
    $message .= "Requirements: " . $requirements;
    
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ssss", $name, $phone, $email, $message);
    
    if ($stmt->execute()) {
        // Prepare email content
        $to = "mohitdhandhukiya1353@gmail.com";
        $subject = "New Hall Booking Inquiry from " . $name;
        
        $email_message = "New Hall Booking Inquiry:\n\n";
        $email_message .= "Name: " . $name . "\n";
        $email_message .= "Phone: " . $phone . "\n";
        $email_message .= "Email: " . $email . "\n";
        $email_message .= "Event Type: " . $event_type . "\n";
        $email_message .= "Event Date: " . $event_date . "\n";
        $email_message .= "Guest Count: " . $guest_count . "\n";
        $email_message .= "Requirements: " . $requirements . "\n";
        
        $headers = "From: " . $email . "\r\n";
        
        // Send email
        mail($to, $subject, $email_message, $headers);
        
        echo json_encode(['status' => 'success', 'message' => 'Thank you for your inquiry! We will contact you soon.']);
    } else {
        echo json_encode(['status' => 'error', 'message' => 'Error submitting inquiry. Please try again.']);
    }
} else {
    echo json_encode(['status' => 'error', 'message' => 'Invalid request method.']);
}
?>
