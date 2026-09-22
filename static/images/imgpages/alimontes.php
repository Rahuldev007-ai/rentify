<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
    <title>Alimentos Hall - Premium Event Venue</title>
    <style>
        :root {
            --primary: #2c3e50;
            --secondary: #e74c3c;
            --dark: #1a1a1a;
            --light: #f8f9fa;
            --accent: #3498db;
        }

        body {
            font-family: 'Poppins', sans-serif;
            background: var(--light);
            min-height: 100vh;
            padding: 20px;
            background: linear-gradient(135deg, #f6f8fd 0%, #ffffff 100%);
        }

        .venue-container {
            max-width: 1200px;
            margin: 40px auto;
            background: white;
            border-radius: 25px;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }

        .image-gallery {
            position: relative;
            height: 500px;
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

        .venue-status {
            position: absolute;
            top: 20px;
            right: 20px;
            background: var(--secondary);
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            font-weight: 500;
            box-shadow: 0 5px 15px rgba(231, 76, 60, 0.3);
        }

        .details-section {
            padding: 40px;
            background: linear-gradient(to bottom, #ffffff, #f8f9fa);
        }

        .venue-title {
            font-size: 2.8rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 20px;
            letter-spacing: -1px;
        }

        .price-display {
            font-size: 2.5rem;
            color: var(--secondary);
            font-weight: 600;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .price-display i {
            font-size: 2rem;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin: 30px 0;
        }

        .feature-item {
            background: var(--light);
            padding: 20px;
            border-radius: 15px;
            display: flex;
            align-items: center;
            gap: 15px;
            transition: all 0.3s ease;
        }

        .feature-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.05);
            background: white;
        }

        .feature-item i {
            font-size: 1.8rem;
            color: var(--accent);
        }

        .feature-item .feature-details {
            flex: 1;
        }

        .feature-item h4 {
            margin: 0;
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--dark);
        }

        .feature-item p {
            margin: 5px 0 0;
            font-size: 0.9rem;
            color: #666;
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
            border-color: var(--accent);
            outline: none;
            box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
        }

        .contact-button {
            display: inline-block;
            width: 100%;
            padding: 18px;
            background: var(--secondary);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.2rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 30px;
            text-decoration: none;
            text-align: center;
        }

        .contact-button:hover {
            background: #c0392b;
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(231, 76, 60, 0.2);
            color: white;
        }

        @media (max-width: 768px) {
            .venue-container {
                margin: 20px auto;
            }

            .image-gallery {
                height: 300px;
            }

            .venue-title {
                font-size: 2rem;
            }

            .details-section {
                padding: 20px;
            }

            .price-display {
                font-size: 2rem;
            }

            .features-grid {
                grid-template-columns: 1fr;
                gap: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="venue-container">
        <div class="image-gallery">
            <img src="perimg/alimentos.jpg" alt="Alimentos Hall">
            <span class="venue-status">Premium Venue</span>
        </div>
        
        <div class="details-section">
            <h1 class="venue-title">Alimentos Hall</h1>
            <div class="price-display">
                <i class="fas fa-tag"></i>
                ₹20,000 <span style="font-size: 1rem; color: var(--dark);">/per day</span>
            </div>

            <div class="features-grid">
                <div class="feature-item">
                    <i class="fas fa-users"></i>
                    <div class="feature-details">
                        <h4>Capacity</h4>
                        <p>Up to 100 People</p>
                    </div>
                </div>
                <div class="feature-item">
                    <i class="fas fa-clock"></i>
                    <div class="feature-details">
                        <h4>Duration Options</h4>
                        <select class="time-select">
                            <option value="24">24 Hours</option>
                            <option value="12">12 Hours</option>
                            <option value="48">2 Days</option>
                            <option value="72">3 Days</option>
                            <option value="96">4 Days</option>
                        </select>
                    </div>
                </div>
                <div class="feature-item">
                    <i class="fas fa-map-marker-alt"></i>
                    <div class="feature-details">
                        <h4>Location</h4>
                        <p>Ahmedabad</p>
                    </div>
                </div>
            </div>

            <div class="features-grid">
                <div class="feature-item">
                    <i class="fas fa-theater-masks"></i>
                    <div class="feature-details">
                        <h4>Stage</h4>
                        <p>Professional stage setup</p>
                    </div>
                </div>
                <div class="feature-item">
                    <i class="fas fa-lightbulb"></i>
                    <div class="feature-details">
                        <h4>Lighting</h4>
                        <p>Modern lighting system</p>
                    </div>
                </div>
                <div class="feature-item">
                    <i class="fas fa-parking"></i>
                    <div class="feature-details">
                        <h4>Parking</h4>
                        <p>Ample parking space</p>
                    </div>
                </div>
            </div>

            <a href="all.php" class="contact-button">
                <i class="fas fa-phone-alt me-2"></i> Contact Now
            </a>
        </div>
    </div>
</body>
</html>
