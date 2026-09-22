<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mercedes-Benz - Car Details</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root {
            --primary-color: #1a237e;
            --secondary-color: #ff3d00;
            --text-color: #333;
            --light-bg: #f8f9fa;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--light-bg);
            color: var(--text-color);
            min-height: 100vh;
            padding-top: 2rem;
        }

        .car-details-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            background: white;
            border-radius: 20px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }

        .car-gallery {
            position: relative;
            border-radius: 15px;
            overflow: hidden;
            margin-bottom: 2rem;
        }

        .car-gallery img {
            width: 100%;
            height: 500px;
            object-fit: cover;
            border-radius: 15px;
            transition: transform 0.3s ease;
        }

        .car-gallery img:hover {
            transform: scale(1.02);
        }

        .car-info {
            padding: 2rem;
            background: var(--light-bg);
            border-radius: 15px;
        }

        .car-title {
            font-size: 2.5rem;
            color: var(--primary-color);
            margin-bottom: 1rem;
            font-weight: 700;
        }

        .price-tag {
            background: var(--secondary-color);
            color: white;
            padding: 0.5rem 1.5rem;
            border-radius: 50px;
            display: inline-block;
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
        }

        .feature-list {
            list-style: none;
            padding: 0;
            margin-bottom: 2rem;
        }

        .feature-item {
            padding: 1rem;
            margin-bottom: 1rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
            display: flex;
            align-items: center;
            transition: transform 0.2s ease;
        }

        .feature-item:hover {
            transform: translateX(5px);
        }

        .feature-item i {
            color: var(--primary-color);
            font-size: 1.5rem;
            margin-right: 1rem;
            width: 30px;
        }

        .rental-form {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        .form-label {
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }

        .form-select, .form-control {
            border: 2px solid #eee;
            border-radius: 8px;
            padding: 0.8rem;
            width: 100%;
            transition: all 0.3s ease;
        }

        .form-select:focus, .form-control:focus {
            border-color: var(--primary-color);
            box-shadow: none;
        }

        .location-options {
            display: flex;
            gap: 2rem;
            margin-top: 0.5rem;
        }

        .location-option {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .btn-rent {
            background: var(--secondary-color);
            color: white;
            padding: 1rem 2rem;
            border: none;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 600;
            width: 100%;
            transition: all 0.3s ease;
        }

        .btn-rent:hover {
            background: #f44336;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }

        @media (max-width: 768px) {
            .car-gallery img {
                height: 300px;
            }

            .car-details-container {
                padding: 1rem;
            }

            .car-title {
                font-size: 2rem;
            }

            .location-options {
                flex-direction: column;
                gap: 1rem;
            }
        }
        /* Modal Styles */
        .booking-modal .modal-content {
            border-radius: 20px;
            border: none;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }

        .booking-modal .modal-header {
            background: var(--primary-color);
            color: white;
            border-radius: 20px 20px 0 0;
            padding: 1.5rem;
        }

        .booking-modal .modal-body {
            padding: 2rem;
        }

        .booking-modal .form-control {
            padding: 0.8rem;
            border-radius: 8px;
            border: 2px solid #eee;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }

        .booking-modal .form-control:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 0.2rem rgba(26, 35, 126, 0.1);
        }

        .booking-modal .btn-book {
            background: var(--secondary-color);
            color: white;
            padding: 1rem 2rem;
            border: none;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 600;
            width: 100%;
            margin-top: 1rem;
            transition: all 0.3s ease;
        }

        .booking-modal .btn-book:hover {
            background: #f44336;
            transform: translateY(-2px);
        }

        @media (max-width: 768px) {
            .car-gallery img {
                height: 300px;
            }

            .car-details-container {
                padding: 1rem;
            }

            .car-title {
                font-size: 2rem;
            }

            .location-options {
                flex-direction: column;
                gap: 1rem;
            }
        }
    </style>
</head>
<body>
    <div class="car-details-container">
        <div class="row">
            <div class="col-lg-7">
                <div class="car-gallery">
                    <img src="perimg/mercedes.jpg" alt="Mercedes-Benz" class="img-fluid">
                </div>
            </div>
            <div class="col-lg-5">
                <div class="car-info">
                    <h1 class="car-title">Mercedes-Benz</h1>
                    <div class="price-tag">₹12,000 / day</div>
                    
                    <ul class="feature-list">
                        <li class="feature-item">
                            <i class="fas fa-car"></i>
                            <span>5 Seater Luxury Sedan</span>
                        </li>
                        <li class="feature-item">
                            <i class="fas fa-gas-pump"></i>
                            <span>Petrol - 14.8 kmpl</span>
                        </li>
                        <li class="feature-item">
                            <i class="fas fa-cog"></i>
                            <span>9G-TRONIC Automatic</span>
                        </li>
                        <li class="feature-item">
                            <i class="fas fa-star"></i>
                            <span>Premium Leather Interior</span>
                        </li>
                        <li class="feature-item">
                            <i class="fas fa-music"></i>
                            <span>Burmester® Sound System</span>
                        </li>
                        <li class="feature-item">
                            <i class="fas fa-shield-alt"></i>
                            <span>PRE-SAFE® Protection</span>
                        </li>
                    </ul>

                    <div class="rental-form">
                        <div class="form-group">
                            <label class="form-label">Rental Duration</label>
                            <select class="form-select">
                                <option value="24">24 Hours</option>
                                <option value="12">12 Hours</option>
                                <option value="48">2 Days</option>
                                <option value="72">3 Days</option>
                                <option value="96">4 Days</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label class="form-label">Pickup Location</label>
                            <div class="location-options">
                                <div class="location-option">
                                    <input type="radio" id="bhavnagar" name="location" value="bhavnagar">
                                    <label for="bhavnagar">Bhavnagar</label>
                                </div>
                                <div class="location-option">
                                    <input type="radio" id="ahmedabad" name="location" value="ahmedabad">
                                    <label for="ahmedabad">Ahmedabad</label>
                                </div>
                            </div>
                        </div>

                        <button class="btn btn-rent" data-bs-toggle="modal" data-bs-target="#bookingModal">
                            <i class="fas fa-car-side me-2"></i>
                            Rent Now
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
     <!-- Booking Modal -->
     <div class="modal fade booking-modal" id="bookingModal" tabindex="-1" aria-labelledby="bookingModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="bookingModalLabel">Complete Your Booking</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="bookingForm">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label class="form-label">First Name</label>
                                    <input type="text" class="form-control" name="firstName" required>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label class="form-label">Last Name</label>
                                    <input type="text" class="form-control" name="lastName" required>
                                </div>
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Email</label>
                            <input type="email" class="form-control" name="email" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Phone</label>
                            <input type="tel" class="form-control" name="phone" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Pickup Date & Time</label>
                            <input type="datetime-local" class="form-control" name="pickupDateTime" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Return Date & Time</label>
                            <input type="datetime-local" class="form-control" name="returnDateTime" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Special Requests</label>
                            <textarea class="form-control" name="specialRequests" rows="3"></textarea>
                        </div>
                        <button type="submit" class="btn btn-book">
                            <i class="fas fa-check me-2"></i>
                            Confirm Booking
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11.0.19/dist/sweetalert2.all.min.js"></script>
    <script>
        document.getElementById('bookingForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = {
                firstName: formData.get('firstName'),
                lastName: formData.get('lastName'),
                email: formData.get('email'),
                phone: formData.get('phone'),
                pickupDateTime: formData.get('pickupDateTime'),
                specialRequests: formData.get('specialRequests'),
                carModel: 'Maruti Swift'
            };

            // Hide booking modal
            const bookingModal = bootstrap.Modal.getInstance(document.getElementById('bookingModal'));
            bookingModal.hide();

            // Show loading state
            Swal.fire({
                title: 'Processing Your Booking',
                html: 'Please wait...',
                allowOutsideClick: false,
                didOpen: () => {
                    Swal.showLoading();
                }
            });

            // Send booking data to server
            fetch('../process_booking.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(result => {
                if (result.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Booking Confirmed!',
                        text: result.message,
                        confirmButtonColor: '#1a237e'
                    });
                    this.reset();
                } else {
                    throw new Error(result.message || 'Failed to process booking');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                Swal.fire({
                    icon: 'error',
                    title: 'Booking Failed',
                    text: error.message || 'Something went wrong. Please try again.',
                    confirmButtonColor: '#1a237e'
                });
            });
        });
    </script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
