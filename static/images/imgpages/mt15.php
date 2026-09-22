<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Royal Enfield Bullet - Premium Bike Rental</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
    <style>
        :root {
            --primary: #003399;
            --secondary: #00ff00;
            --dark: #1a1a1a;
            --light: #f8f9fa;
            --accent: #ff3366;
        }

        body {
            font-family: 'Poppins', sans-serif;
            background: var(--light);
            min-height: 100vh;
            display: flex;
            align-items: center;
            padding: 20px;
            background: linear-gradient(135deg, #f6f8fd 0%, #ffffff 100%);
        }

        .bike-container {
            max-width: 1200px;
            margin: auto;
            padding: 20px;
        }

        .bike-card {
            background: white;
            border-radius: 25px;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            position: relative;
        }

        .image-gallery {
            position: relative;
            height: 450px;
            overflow: hidden;
        }

        .image-gallery img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s ease;
        }

        .image-gallery:hover img {
            transform: scale(1.05);
        }

        .bike-status {
            position: absolute;
            top: 20px;
            right: 20px;
            background: var(--accent);
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            font-weight: 500;
            box-shadow: 0 5px 15px rgba(255, 51, 102, 0.3);
        }

        .specs-section {
            padding: 40px;
            background: linear-gradient(to bottom, #ffffff, #f8f9fa);
        }

        .bike-title {
            font-size: 2.8rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 20px;
            letter-spacing: -1px;
        }

        .price-display {
            font-size: 2rem;
            color: var(--accent);
            font-weight: 600;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .price-display i {
            font-size: 1.5rem;
        }

        .specs-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .spec-item {
            background: var(--light);
            padding: 15px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 15px;
            transition: all 0.3s ease;
        }

        .spec-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.05);
            background: white;
        }

        .spec-item i {
            font-size: 1.5rem;
            color: var(--primary);
        }

        .rental-options {
            background: white;
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        }

        .time-select {
            padding: 12px;
            border-radius: 10px;
            border: 2px solid #e1e1e1;
            width: 100%;
            max-width: 250px;
            font-size: 1rem;
            margin-top: 10px;
            background: white;
            transition: all 0.3s ease;
        }

        .time-select:focus {
            border-color: var(--primary);
            outline: none;
            box-shadow: 0 0 0 3px rgba(0, 51, 153, 0.1);
        }

        .location-group {
            display: flex;
            gap: 20px;
            margin-top: 20px;
        }

        .location-option {
            flex: 1;
            padding: 15px;
            background: var(--light);
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
        }

        .location-option:hover {
            background: white;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        }

        .location-option input[type="radio"] {
            margin-right: 8px;
        }

        .book-button {
            display: inline-block;
            width: 100%;
            padding: 18px;
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.2rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 20px;
        }

        .book-button:hover {
            background: #002266;
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0, 51, 153, 0.2);
        }

        @media (max-width: 768px) {
            .image-gallery {
                height: 300px;
            }

            .bike-title {
                font-size: 2rem;
            }

            .specs-section {
                padding: 20px;
            }

            .location-group {
                flex-direction: column;
            }

            .price-display {
                font-size: 1.5rem;
            }
        }
          /* Booking Form Styles */
          .booking-form-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 1000;
            justify-content: center;
            align-items: center;
            padding: 20px;
            overflow-y: auto;
        }

        .booking-form {
            background: white;
            padding: 30px;
            border-radius: 15px;
            width: 100%;
            max-width: 500px;
            position: relative;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            margin: 20px auto;
            max-height: 90vh;
            overflow-y: auto;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: var(--dark);
        }

        .form-group input,
        .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e1e1e1;
            border-radius: 8px;
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        .form-group input:focus,
        .form-group textarea:focus {
            border-color: var(--primary);
            outline: none;
            box-shadow: 0 0 0 3px rgba(0, 51, 153, 0.1);
        }

        .close-form {
            position: absolute;
            top: 15px;
            right: 15px;
            font-size: 24px;
            cursor: pointer;
            color: var(--dark);
            transition: color 0.3s ease;
        } 

        .close-form:hover {
            color: var(--accent);
        }

        @media (max-width: 768px) {
            .image-gallery {
                height: 300px;
            }

            .bike-title {
                font-size: 2rem;
            }

            .specs-section {
                padding: 20px;
            }

            .location-group {
                flex-direction: column;
            }

            .price-display {
                font-size: 1.5rem;
            }

            .booking-form {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="bike-container">
        <div class="bike-card">
            <div class="image-gallery">
                <img src="perimg/mt15.jpg" alt="Royal Enfield Bullet">
                <span class="bike-status">Premium Bike</span>
            </div>
            
            <div class="specs-section">
                <h1 class="bike-title">YAMAHA MT - 15</h1>
                <div class="price-display">
                    <i class="fas fa-tag"></i>
                    ₹2,200 <span style="font-size: 1rem; color: var(--dark);">/per day</span>
                </div>

                <div class="specs-grid">
                    <div class="spec-item">
                        <i class="fas fa-tachometer-alt"></i>
                        <div>
                            <h4>155cc</h4>
                            <small>Engine</small>
                        </div>
                    </div>
                    <div class="spec-item">
                        <i class="fas fa-horse"></i>
                        <div>
                            <h4>18.4 PS</h4>
                            <small>Power</small>
                        </div>
                    </div>
                    <div class="spec-item">
                        <i class="fas fa-gas-pump"></i>
                        <div>
                            <h4>56.87 kmpl</h4>
                            <small>Mileage</small>
                        </div>
                    </div>
                </div>

                <button class="book-button" onclick="showBookingForm()">
                    <i class="fas fa-motorcycle me-2"></i> Book Now
                </button>
            </div>
        </div>
    </div>
    <!-- Booking Form Overlay -->
    <div class="booking-form-overlay" id="bookingFormOverlay">
        <div class="booking-form">
            <span class="close-form" onclick="hideBookingForm()">&times;</span>
            <h2 style="margin-bottom: 20px; color: var(--primary);">Book Your Ride</h2>
            <form id="bikeBookingForm">
                <div class="form-group">
                    <label for="firstName">First Name</label>
                    <input type="text" id="firstName" name="firstName" required>
                </div>
                <div class="form-group">
                    <label for="lastName">Last Name</label>
                    <input type="text" id="lastName" name="lastName" required>
                </div>
                <div class="form-group">
                    <label for="phone">Phone Number</label>
                    <input type="tel" id="phone" name="phone" required>
                </div>
                <div class="form-group">
                    <label for="pickupDateTime">Pick Up Date & Time</label>
                    <input type="datetime-local" id="pickupDateTime" name="pickupDateTime" required>
                </div>
                <div class="form-group">
                    <label for="returnDateTime">Return Date & Time</label>
                    <input type="datetime-local" id="returnDateTime" name="returnDateTime" required>
                </div>
                <div class="form-group">
                    <label for="specialRequest">Special Request</label>
                    <textarea id="specialRequest" name="specialRequest" rows="3"></textarea>
                </div>
                <button type="submit" class="book-button">Confirm Booking</button>
            </form>
        </div>
    </div>

    <script>
        function showBookingForm() {
            document.getElementById('bookingFormOverlay').style.display = 'flex';
        }

        function hideBookingForm() {
            document.getElementById('bookingFormOverlay').style.display = 'none';
        }

        document.getElementById('bikeBookingForm').addEventListener('submit', function(e) {
            e.preventDefault();
            // Here you can add code to handle the form submission
            alert('Booking request submitted successfully!');
            hideBookingForm();
        });
    </script>
</body>
</html>
