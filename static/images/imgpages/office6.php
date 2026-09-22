<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <title>Premium Office Space - Vagdo Rentals</title>
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', Arial, sans-serif;
            min-height: 100vh;
            background-color: #f8f9fa;
            color: #333;
        }

        .main-container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1rem;
        }

        .office-card {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }

        .image-gallery {
            position: relative;
            height: 500px;
            overflow: hidden;
        }

        .main-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }

        .main-image:hover {
            transform: scale(1.05);
        }

        .office-details {
            padding: 2rem;
        }

        .office-title {
            font-size: 2.5rem;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 1rem;
        }

        .price-tag {
            font-size: 1.8rem;
            color: #2ecc71;
            font-weight: 600;
            margin-bottom: 1.5rem;
        }

        .feature-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }

        .feature-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 1.1rem;
            color: #555;
        }

        .feature-item i {
            color: #3498db;
            font-size: 1.2rem;
        }

        .location-info {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1.5rem 0;
        }

        .location-info h3 {
            color: #2c3e50;
            margin-bottom: 1rem;
        }

        .contact-section {
            margin-top: 2rem;
            text-align: center;
        }

        .contact-button {
            display: inline-block;
            padding: 1rem 2.5rem;
            font-size: 1.2rem;
            font-weight: 600;
            color: white;
            background: #3498db;
            border: none;
            border-radius: 50px;
            text-decoration: none;
            transition: all 0.3s ease;
            margin: 0 0.5rem;
        }

        .contact-button:hover {
            background: #2980b9;
            transform: translateY(-2px);
            color: white;
        }

        .whatsapp-button {
            background: #25d366;
        }

        .whatsapp-button:hover {
            background: #128c7e;
        }

        .amenities-section {
            margin: 2rem 0;
        }

        .amenities-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }

        .amenity-item {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
            transition: transform 0.2s ease;
        }

        .amenity-item:hover {
            transform: translateY(-5px);
        }

        .amenity-item i {
            font-size: 1.5rem;
            color: #3498db;
            margin-bottom: 0.5rem;
        }

        @media (max-width: 768px) {
            .image-gallery {
                height: 300px;
            }

            .office-title {
                font-size: 2rem;
            }

            .price-tag {
                font-size: 1.5rem;
            }

            .feature-list {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="main-container">
        <div class="office-card">
            <div class="image-gallery">
                <img src="perimg/o6.jpg" alt="Premium Office Space" class="main-image">
            </div>
            
            <div class="office-details">
                <h1 class="office-title">Luxury Executive Suite</h1>
                <div class="price-tag">₹45,000/month</div>
                
                <div class="feature-list">
                    <div class="feature-item">
                        <i class="fas fa-ruler-combined"></i>
                        <span>1800 sq.ft Area</span>
                    </div>
                    <div class="feature-item">
                        <i class="fas fa-building"></i>
                        <span>Premium Complex</span>
                    </div>
                    <div class="feature-item">
                        <i class="fas fa-car"></i>
                        <span>Reserved Parking</span>
                    </div>
                    <div class="feature-item">
                        <i class="fas fa-shield-alt"></i>
                        <span>24/7 Security</span>
                    </div>
                </div>

                <div class="location-info">
                    <h3><i class="fas fa-map-marker-alt"></i> Location Details</h3>
                    <p>Prime location in Bhavnagar's business district with panoramic city views and excellent accessibility.</p>
                </div>

                <div class="amenities-section">
                    <h3>Office Amenities</h3>
                    <div class="amenities-grid">
                        <div class="amenity-item">
                            <i class="fas fa-wifi"></i>
                            <p>High-Speed Internet</p>
                        </div>
                        <div class="amenity-item">
                            <i class="fas fa-snowflake"></i>
                            <p>Central AC</p>
                        </div>
                        <div class="amenity-item">
                            <i class="fas fa-plug"></i>
                            <p>Backup Power</p>
                        </div>
                        <div class="amenity-item">
                            <i class="fas fa-couch"></i>
                            <p>Luxury Furnishing</p>
                        </div>
                        <div class="amenity-item">
                            <i class="fas fa-coffee"></i>
                            <p>Executive Lounge</p>
                        </div>
                        <div class="amenity-item">
                            <i class="fas fa-door-closed"></i>
                            <p>Private Suite</p>
                        </div>
                    </div>
                </div>

                <div class="contact-section">
                    <a href="alloffice.php" class="contact-button">
                        <i class="fas fa-phone"></i> Contact Now
                    </a>
                    <a href="https://wa.me/+917990521230" class="contact-button whatsapp-button">
                        <i class="fab fa-whatsapp"></i> WhatsApp
                    </a>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
