<?php
session_start();
include '../connection.php';  // This now uses vagdo_rental database

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Get form data
    $name = $_POST['name'];
    $phone = $_POST['phone'];
    $email = $_POST['email'];
    $house_type = $_POST['house_type'];
    $preferred_location = $_POST['preferred_location'];
    $family_size = $_POST['family_size'];
    $move_in_date = $_POST['move_in_date'];
    $budget_range = $_POST['budget_range'];
    $requirements = $_POST['requirements'];

    // Insert into houseinquiry table
    $sql = "INSERT INTO houseinquiry (name, phone, email, house_type, preferred_location, family_size, move_in_date, budget_range, requirements) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)";
    
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("sssssssss", $name, $phone, $email, $house_type, $preferred_location, $family_size, $move_in_date, $budget_range, $requirements);
    
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
    <title>Your Dream Home Rental - Find Your Perfect Stay</title>
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

        .preference-options {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .preference-option {
            flex: 1;
            min-width: 120px;
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

        <h1>🏠 Welcome to Vagdo House Rentals 🏠</h1>
        <p class="slogan">"Find Your Perfect Stay - Comfortable, Affordable, and Hassle-Free!"</p>

        <div class="section">
            <h2>About Our Properties</h2>
            <p>
                Looking for a comfortable and well-maintained house for rent? Look no further! Vagdo House Rentals offers a variety of homes to suit your needs, whether you're searching for a cozy apartment or a spacious family house. We provide clean, secure, and affordable properties for your peace of mind.
            </p>
            <div class="features">
                <div class="feature-item">Fully Furnished Options</div>
                <div class="feature-item">Prime Locations</div>
                <div class="feature-item">Flexible Lease Terms</div>
                <div class="feature-item">24/7 Maintenance Support</div>
                <div class="feature-item">Pet-Friendly Homes</div>
                <div class="feature-item">Affordable Rent Packages</div>
            </div>
        </div>

        <div class="section">
            <h2>Contact Us Today!</h2>
            <p class="contact-info">
                📞 <strong>Call/WhatsApp</strong>: <a href="tel:+917990511230">+91 7990521230</a><br>
                💬 <strong>WhatsApp Link</strong>: <a href="https://chat.whatsapp.com/BkPraTtFeIj4LCxPZChHWc">Click Here to Chat on WhatsApp</a><br>
                📧 <strong>Email</strong>: <a href="mailto:vagdorentals8411@gmail.com">vagdorentals8411@gmail.com</a><br>
            </p>
        </div>

        <div class="section">
            <h2>Book Your Stay Now!</h2>
            <p>Fill out the form below to inquire about house availability and schedule a viewing.</p>
            
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
                    <label class="form-label">House Type *</label>
                    <select class="form-control" name="house_type" required>
                        <option value="">Select house type</option>
                        <option value="apartment">Apartment</option>
                        <option value="villa">Villa</option>
                        <option value="bungalow">Bungalow</option>
                        <option value="duplex">Duplex</option>
                        <option value="penthouse">Penthouse</option>
                        <option value="other">Other</option>
                    </select>
                </div>

                <div class="form-group">
                    <label class="form-label">Preferred Location *</label>
                    <input type="text" class="form-control" name="preferred_location" required placeholder="Enter preferred location">
                </div>

                <div class="form-group">
                    <label class="form-label">Family Size *</label>
                    <select class="form-control" name="family_size" required>
                        <option value="">Select family size</option>
                        <option value="1-2">1-2 members</option>
                        <option value="3-4">3-4 members</option>
                        <option value="5-6">5-6 members</option>
                        <option value="7+">7+ members</option>
                    </select>
                </div>

                <div class="form-group">
                    <label class="form-label">Preferred Move-in Date *</label>
                    <input type="date" class="form-control" name="move_in_date" required>
                </div>

                <div class="form-group">
                    <label class="form-label">Budget Range *</label>
                    <select class="form-control" name="budget_range" required>
                        <option value="">Select budget range</option>
                        <option value="5000-10000">₹5,000 - ₹10,000</option>
                        <option value="10000-15000">₹10,000 - ₹15,000</option>
                        <option value="15000-20000">₹15,000 - ₹20,000</option>
                        <option value="20000-30000">₹20,000 - ₹30,000</option>
                        <option value="30000+">₹30,000+</option>
                    </select>
                </div>

                <div class="form-group">
                    <label class="form-label">Additional Requirements</label>
                    <textarea class="form-control" name="requirements" rows="4" placeholder="Tell us about any specific requirements (parking, garden, etc.)"></textarea>
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
            <p>🏡 Your Comfort, Our Priority – Welcome Home! 🏡</p>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>