<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <title>Responsive Car Info Page</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f4f4f4;
        }

        .container {
            display: flex;
            flex-direction: column;
            max-width: 800px;
            width: 100%;
            background: #fff;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            overflow: hidden;
        }

        .image-section {
            width: 100%;
            height: 400px;
            background: url(perimg/avalon.jpg) center/cover no-repeat;
        }

        .info-section {
            padding: 20px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .info-section h1 {
            margin: 0 0 10px;
            font-size: 24px;
        }

        .info-section p {
            margin: 5px 0;
            font-size: 16px;
            color: #555;
        }

        .info-section button {
            margin-top: 20px;
            padding: 10px 20px;
            font-size: 16px;
            color: #fff;
            background: #007bff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s ease;
        }

        .info-section button:hover {
            background: #0056b3;
        }

        @media (max-width: 768px) {
            .image-section {
                height: 200px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="image-section"></div>
        <div class="info-section">
            <h1>Avalon-Hall</h1>
            <p><strong>Price:</strong> ₹ 15000</p>
            <p><strong>Time:</strong>
                <select name="dpl">
                    <option value="time">24 - Hours</option>
                    <option value="time">12 - Hours</option>
                    <option value="time">2 - Days</option>
                    <option value="time">3 - Days</option>
                    <option value="time">4 - Days</option>
            </select>
            </p>
            <p><strong>capacity:</strong>
                150 People
                </p>
                <p><strong>Amenities:</strong>
                    Stage , Lighting , Parking
                    </p>
            <p><strong>Location:</strong>
                Ahemdabad
                </p>
            <button><a href="all.php">Contact Now</button>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
</body>
</html>
