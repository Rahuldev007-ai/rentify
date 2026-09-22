<?php
session_start();
include '../connection.php';  // This now uses vagdo_rental database

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Get form data
    $name = $_POST['name'];
    $phone = $_POST['phone'];
    $email = $_POST['email'];
    $business_type = $_POST['business_type'];
    $preferred_location = $_POST['preferred_location'];
    $employees_count = $_POST['employees_count'];
    $move_in_date = $_POST['move_in_date'];
    $requirements = $_POST['requirements'];

    // Insert into officeinquiry table
    $sql = "INSERT INTO officeinquiry (name, phone, email, business_type, preferred_location, employees_count, move_in_date, requirements) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
    
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ssssssss", $name, $phone, $email, $business_type, $preferred_location, $employees_count, $move_in_date, $requirements);
    
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
    <title>Office Rentals - Vagdo Rental</title>
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
        .inquiry-section {
            max-width: 800px;
            margin: 3rem auto;
            padding: 2rem;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }

        .section-title {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 2rem;
            font-size: 2.5rem;
            font-weight: 600;
        }

        .form-label {
            font-weight: 500;
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }

        .form-control {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 0.75rem;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }

        .form-control:focus {
            border-color: #3498db;
            box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
        }

        .submit-btn {
            background: #3498db;
            color: white;
            padding: 1rem 2rem;
            border: none;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 600;
            width: 100%;
            transition: all 0.3s ease;
            margin-top: 1rem;
        }

        .submit-btn:hover {
            background: #2980b9;
            transform: translateY(-2px);
        }

        .office-preference {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
        }

        .office-preference label {
            margin-right: 1rem;
            cursor: pointer;
        }

        .required-field {
            color: #e74c3c;
        }

        .form-text {
            color: #7f8c8d;
            font-size: 0.9rem;
            margin-top: 0.25rem;
        }

        .success-message {
            display: none;
            background: #2ecc71;
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin-top: 1rem;
            text-align: center;
        }

        .contact-info {
            text-align: center;
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 1px solid #e0e0e0;
        }

        .contact-info i {
            color: #3498db;
            margin-right: 0.5rem;
        }

        .whatsapp-btn {
            background: #25d366;
            color: white;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 50px;
            text-decoration: none;
            display: inline-block;
            margin-top: 1rem;
            transition: all 0.3s ease;
        }

        .whatsapp-btn:hover {
            background: #128c7e;
            color: white;
            transform: translateY(-2px);
        }
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
        .inquiry-form {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background: #fff;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-label {
            font-weight: 600;
            margin-bottom: 8px;
        }
        .btn-submit {
            background: #ff6f61;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 5px;
            font-weight: 600;
            transition: all 0.3s;
        }
        .btn-submit:hover {
            background: #ff5546;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
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

        <h1>🏢 Welcome to Vagdo Office Rent 🏢</h1>
        <p class="slogan">"The Perfect Space to Grow Your Business!"</p>

        <div class="section">
            <h2>About Our Office Spaces</h2>
            <p>
                Looking for the perfect office space to enhance productivity? Look no further! We offer spacious, fully-equipped, and professional office spaces tailored to meet your business needs. Whether you're a startup, a freelancer, or a corporate team, we provide the ideal workspace for you.
            </p>
            <div class="features">
                <div class="feature-item">Fully Furnished Offices</div>
                <div class="feature-item">High-Speed Internet</div>
                <div class="feature-item">Conference Rooms</div>
                <div class="feature-item">24/7 Security</div>
                <div class="feature-item">Parking Facility</div>
                <div class="feature-item">Flexible Lease Options</div>
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

        <div class="container">
            <div class="inquiry-section">
                <h1 class="section-title">Inquire Now</h1>
                
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
                        <label class="form-label">Business Type *</label>
                        <select class="form-control" name="business_type" required>
                            <option value="">Select business type</option>
                            <option value="technology">Technology/IT</option>
                            <option value="consulting">Consulting</option>
                            <option value="retail">Retail</option>
                            <option value="healthcare">Healthcare</option>
                            <option value="education">Education</option>
                            <option value="other">Other</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Preferred Location *</label>
                        <input type="text" class="form-control" name="preferred_location" required placeholder="Enter preferred location">
                    </div>

                    <div class="form-group">
                        <label class="form-label">Number of Employees *</label>
                        <select class="form-control" name="employees_count" required>
                            <option value="">Select employee count</option>
                            <option value="1-5">1-5 employees</option>
                            <option value="6-15">6-15 employees</option>
                            <option value="16-30">16-30 employees</option>
                            <option value="31-50">31-50 employees</option>
                            <option value="50+">50+ employees</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Preferred Move-in Date *</label>
                        <input type="date" class="form-control" name="move_in_date" required>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Additional Requirements</label>
                        <textarea class="form-control" name="requirements" rows="4" placeholder="Tell us about any specific requirements (parking, meeting rooms, etc.)"></textarea>
                    </div>

                    <div class="form-group text-center">
                        <button type="submit" class="btn-submit">Submit Inquiry</button>
                    </div>
                </form>
            </div>
        </div>

        <div class="social-links">
            <h2>Follow Us on Social Media</h2>
            <a href="#">📷 Instagram</a>
            <a href="#">👍 Facebook</a>
            <a href="#">🐦 Twitter</a>
        </div>

        <div class="footer">
            <p>🏢 Your Business, Our Space – Let's Grow Together! 🏢</p>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.getElementById('officeInquiryForm').addEventListener('submit', function(e) {
            e.preventDefault();
            // Form submission logic here
            document.getElementById('successMessage').style.display = 'block';
            this.reset();
            setTimeout(function() {
                document.getElementById('successMessage').style.display = 'none';
            }, 5000);
        });
    </script>
</body>
</html>
