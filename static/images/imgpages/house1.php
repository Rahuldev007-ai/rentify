<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>House Details | Vagdo Rentals</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root {
            --primary-color: #2c3e50;
            --accent-color: #e74c3c;
            --text-color: #34495e;
            --light-bg: #f8f9fa;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--light-bg);
            color: var(--text-color);
            line-height: 1.6;
        }

        .property-container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1rem;
        }

        .property-card {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
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

        .property-details {
            padding: 2rem;
        }

        .property-title {
            font-size: 2.5rem;
            color: var(--primary-color);
            margin-bottom: 1rem;
            font-weight: 600;
        }

        .price-tag {
            background: var(--accent-color);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            display: inline-block;
            font-size: 1.25rem;
            margin-bottom: 1.5rem;
        }

        .location-info {
            display: flex;
            align-items: center;
            margin-bottom: 1.5rem;
            color: var(--text-color);
        }

        .location-info i {
            color: var(--accent-color);
            margin-right: 0.5rem;
            font-size: 1.25rem;
        }

        .features-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }

        .feature-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .feature-item i {
            color: var(--accent-color);
            font-size: 1.25rem;
        }

        .contact-section {
            background: var(--primary-color);
            padding: 2rem;
            border-radius: 10px;
            color: white;
            margin-top: 2rem;
        }

        .contact-btn {
            background: var(--accent-color);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 25px;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            margin-top: 1rem;
        }

        .contact-btn:hover {
            background: #c0392b;
            transform: translateY(-2px);
            color: white;
        }

        .back-btn {
            position: fixed;
            top: 20px;
            left: 20px;
            background: var(--primary-color);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            z-index: 1000;
            transition: all 0.3s ease;
        }

        .back-btn:hover {
            background: var(--accent-color);
            color: white;
        }

        @media (max-width: 768px) {
            .property-container {
                margin: 1rem auto;
            }

            .image-gallery {
                height: 300px;
            }

            .property-title {
                font-size: 2rem;
            }

            .features-list {
                grid-template-columns: 1fr;
                gap: 1rem;
            }

            .contact-section {
                padding: 1.5rem;
            }
        }
    </style>
</head>
<body>
    <a href="allhouse.html" class="back-btn">
        <i class="fas fa-arrow-left"></i> Back
    </a>

    <div class="property-container">
        <div class="property-card">
            <div class="image-gallery">
                <img src="perimg/i1.jpg" alt="House View" class="main-image">
            </div>

            <div class="property-details">
                <h1 class="property-title">House-1</h1>
                <div class="price-tag">₹5,000/month</div>

                <div class="location-info">
                    <i class="fas fa-map-marker-alt"></i>
                    <span>Bhavnagar</span>
                </div>

                <div class="features-list">
                    <div class="feature-item">
                        <i class="fas fa-bed"></i>
                        <span>2 Bedrooms</span>
                    </div>
                    <div class="feature-item">
                        <i class="fas fa-bath"></i>
                        <span>1 Bathroom</span>
                    </div>
                    <div class="feature-item">
                        <i class="fas fa-vector-square"></i>
                        <span>1200 sq ft</span>
                    </div>
                    <div class="feature-item">
                        <i class="fas fa-car"></i>
                        <span>1 Parking</span>
                    </div>
                </div>

                <div class="contact-section">
                    <h3>Interested in this property?</h3>
                    <p>Contact our team for more information or to schedule a viewing.</p>
                    <a href="allhouse.php" class="contact-btn">
                        <i class="fas fa-phone"></i> Contact Now
                    </a>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
