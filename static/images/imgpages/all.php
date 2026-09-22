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

    // Insert into hallinquiry table
    $sql = "INSERT INTO hallinquiry (name, phone, email, event_type, event_date, guest_count, requirements) 
            VALUES (?, ?, ?, ?, ?, ?, ?)";
    
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("sssssss", $name, $phone, $email, $event_type, $event_date, $guest_count, $requirements);
    
    if ($stmt->execute()) {
        $_SESSION['success_message'] = "Thank you for your inquiry! We will contact you soon.";
        header("Location: " . $_SERVER['PHP_SELF']);
        exit();
    } else {
        $_SESSION['error_message'] = "Error submitting form. Please try again.";
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Hall Name - Perfect Venue for Events</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
          font-family: 'Arial', sans-serif;
          margin: 0;
          padding: 0;
          background-color: #f9f9f9;
          color: #333;
        }

        .container {
          max-width: 1200px;
          margin: 0 auto;
          padding: 20px;
          text-align: center;
        }

        h1 {
          font-size: 3rem;
          color: #ff6f61;
          margin-bottom: 10px;
        }

        .slogan {
          font-size: 1.5rem;
          color: #555;
          margin-bottom: 30px;
        }

        .section {
          background-color: #fff;
          padding: 20px;
          border-radius: 10px;
          box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
          margin-bottom: 20px;
        }

        .section h2 {
          font-size: 2rem;
          color: #333;
          margin-bottom: 15px;
        }

        .section p {
          font-size: 1.1rem;
          line-height: 1.6;
          color: #555;
        }

        .features {
          display: flex;
          flex-wrap: wrap;
          justify-content: center;
          gap: 20px;
          margin-top: 20px;
        }

        .feature-item {
          background-color: #ff6f61;
          color: #fff;
          padding: 15px;
          border-radius: 10px;
          width: 200px;
          text-align: center;
        }

        .contact-info {
          font-size: 1.2rem;
          margin-top: 20px;
        }

        .contact-info a {
          color: #ff6f61;
          text-decoration: none;
          font-weight: bold;
        }

        .contact-info a:hover {
          text-decoration: underline;
        }

        .social-links {
          margin-top: 30px;
        }

        .social-links a {
          margin: 0 10px;
          text-decoration: none;
          color: #ff6f61;
          font-size: 1.2rem;
        }

        .social-links a:hover {
          color: #333;
        }

        .footer {
          margin-top: 40px;
          font-size: 1rem;
          color: #777;
        }

        /* Form Styles */
        .inquiry-form {
          max-width: 600px;
          margin: 0 auto;
          text-align: left;
        }

        .form-group {
          margin-bottom: 1.5rem;
        }

        .form-label {
          font-weight: 600;
          color: #333;
          margin-bottom: 0.5rem;
        }

        .form-control {
          border: 1px solid #ddd;
          border-radius: 8px;
          padding: 0.75rem;
          transition: border-color 0.3s ease;
        }

        .form-control:focus {
          border-color: #ff6f61;
          box-shadow: 0 0 0 0.2rem rgba(255, 111, 97, 0.25);
        }

        .btn-submit {
          background-color: #ff6f61;
          color: white;
          padding: 12px 30px;
          border: none;
          border-radius: 8px;
          font-size: 1.1rem;
          font-weight: 600;
          transition: all 0.3s ease;
        }

        .btn-submit:hover {
          background-color: #ff5546;
          transform: translateY(-2px);
        }

        /* Add new styles for messages */
        .alert {
          padding: 15px;
          margin: 20px 0;
          border-radius: 8px;
          text-align: center;
          font-size: 18px;
          animation: fadeIn 0.5s;
        }

        .alert-success {
          background-color: rgba(46, 204, 113, 0.2);
          color: #27ae60;
          border: 2px solid #27ae60;
        }

        .alert-error {
          background-color: rgba(231, 76, 60, 0.2);
          color: #c0392b;
          border: 2px solid #c0392b;
        }

        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(-10px); }
          to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎉 Welcome to Vagdo Hall Rent🎉</h1>
        <p class="slogan">"Where Memories Are Made and Celebrations Come to Life!"</p>

        <?php
        // Display success message if set
        if (isset($_SESSION['success_message'])) {
            echo '<div class="alert alert-success">' . $_SESSION['success_message'] . '</div>';
            unset($_SESSION['success_message']);
        }
        // Display error message if set
        if (isset($_SESSION['error_message'])) {
            echo '<div class="alert alert-error">' . $_SESSION['error_message'] . '</div>';
            unset($_SESSION['error_message']);
        }
        ?>

        <div class="section">
          <h2>About Our Hall</h2>
          <p>
            Looking for the perfect venue for your next event? Look no further! offers a spacious, elegant, and fully-equipped hall to make your special occasion unforgettable. Whether it's a wedding, birthday party, corporate event, or family gathering, we provide the perfect setting for your celebration.
          </p>
          <div class="features">
            <div class="feature-item">Spacious and Air-Conditioned</div>
            <div class="feature-item">Modern Sound & Lighting</div>
            <div class="feature-item">Flexible Seating</div>
            <div class="feature-item">On-Site Parking</div>
            <div class="feature-item">Catering Services</div>
            <div class="feature-item">Affordable Packages</div>
          </div>
        </div>

       
        <div class="section">
          <h2>Contact Us Today!</h2>
          <p class="contact-info">
            📞 <strong>Call/WhatsApp</strong>: <a href="tel:+917990511230">+91 7990521230</a><br>
            💬 <strong>WhatsApp Link</strong>: <a href="https://chat.whatsapp.com/BkPraTtFeIj4LCxPZChHWc">Click Here to Chat on WhatsApp</a><br>
            📧 <strong>Email</strong>: <a href="mailto:vagdorentals8411.com">vagdorentals8411@gmail.com</a><br>
          </p>
        </div>

        <div class="section">
          <h2>Book Your Date Now!</h2>
          <p>Fill out the form below to inquire about hall availability and pricing.</p>
          
          <form class="inquiry-form" method="POST" action="">
            <div class="form-group">
              <label class="form-label">Full Name *</label>
              <input type="text" class="form-control" name="name" required placeholder="Enter your full name">
            </div>

            <div class="form-group">
              <label class="form-label">Phone Number *</label>
              <input type="tel" class="form-control" name="phone" required placeholder="Enter your phone number">
            </div>

            <div class="form-group">
              <label class="form-label">Email Address</label>
              <input type="email" class="form-control" name="email" placeholder="Enter your email address">
            </div>

            <div class="form-group">
              <label class="form-label">Event Type *</label>
              <select class="form-control" name="event_type" required>
                <option value="">Select event type</option>
                <option value="wedding">Wedding</option>
                <option value="birthday">Birthday Party</option>
                <option value="corporate">Corporate Event</option>
                <option value="reception">Reception</option>
                <option value="other">Other</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Preferred Date *</label>
              <input type="date" class="form-control" name="event_date" required>
            </div>

            <div class="form-group">
              <label class="form-label">Number of Guests *</label>
              <select class="form-control" name="guest_count" required>
                <option value="">Select guest count</option>
                <option value="1-50">1-50 guests</option>
                <option value="51-100">51-100 guests</option>
                <option value="101-200">101-200 guests</option>
                <option value="201-300">201-300 guests</option>
                <option value="300+">300+ guests</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Additional Requirements</label>
              <textarea class="form-control" name="requirements" rows="4" placeholder="Tell us about any specific requirements (catering, decoration, etc.)"></textarea>
            </div>

            <div class="form-group text-center">
              <button type="submit" class="btn-submit">Submit Inquiry</button>
            </div>
          </form>
        </div>

        <div class="social-links">
          <h2>Follow Us on Social Media</h2>
          <a href="#">📷 Instagram</a>
          <a href="#">👍 Facebook</a>
          <a href="#">🐦 Twitter</a>
        </div>

        <div class="footer">
          <p>🎉 Your Event, Our Passion – Let's Celebrate Together! 🎉</p>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>