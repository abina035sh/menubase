from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from twilio.rest import Client
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import geocoder
import logging
from gtts import gTTS
from flask import Flask, request, jsonify, send_file
from gtts import gTTS
import io
from flask import Flask, request, jsonify
from flask import Flask, request, jsonify
from flask import Flask, request, jsonify
import os
import cv2
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from PIL import Image, ImageFilter, ImageDraw
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from werkzeug.utils import secure_filename
from flask_cors import CORS
import cv2
from werkzeug.utils import secure_filename
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder, StandardScaler




app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/send_text_sms', methods=['POST'])
def send_text_sms():
    data = request.json
    account_sid = data['account_sid']
    auth_token = data['auth_token']
    to = data['to']
    from_ = data['from']  # Add this line to get the sender's phone number
    body = data['body']

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=to,
        from_=from_,  # Use the input phone number here
        body=body
    )

    return jsonify({"status": "success", "message_sid": message.sid})

@app.route('/send_mail', methods=['POST'])
def send_mail():
    data = request.json
    sender_email = data['sender_email']
    sender_password = data['sender_password']
    recipient_email = data['recipient_email']
    subject = data['subject']
    message = data['message']

    logging.info("Email send request received")

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()

        logging.info("Email sent successfully")
        return jsonify({"status": "success", "message": "Email sent successfully"})

    except smtplib.SMTPAuthenticationError:
        logging.error("Failed to authenticate")
        return jsonify({"status": "error", "message": "Failed to authenticate. Check your email and password."})
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})
    
    






@app.route('/google_query', methods=['POST'])
def google_query():
    GOOGLE_API_KEY = 'YOUR API KEY'  # Replace with a secure method to load the API key
    CSE_ID = 'YOUR SEARCH ENGINE ID'  # Replace with a secure method to load the CSE ID

    data = request.json
    query = data.get('query')
    num_results = data.get('num_results', 5)

    if not query:
        return jsonify({"status": "error", "message": "Query parameter is required"}), 400

    try:
        # Construct the API request URL
        params = {
            'key': GOOGLE_API_KEY,
            'cx': CSE_ID,
            'q': query,
            'num': num_results
        }
        search_url = "https://www.googleapis.com/customsearch/v1"
        response = requests.get(search_url, params=params)

        if response.status_code != 200:
            error_message = response.json().get('error', {}).get('message', 'Unknown error')
            return jsonify({"status": "error", "message": f"Error from Google API: {error_message}"}), response.status_code

        search_results = response.json()
        items = search_results.get('items', [])
        result_links = [item.get('link', 'No link available') for item in items]

        return jsonify({"results": result_links})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
            
@app.route('/get_location', methods=['GET'])
def get_location():
    g = geocoder.ip('me')
    latitude, longitude = g.latlng
    location = f"{g.city}, {g.state}, {g.country}"
    return jsonify({
        "latitude": latitude,
        "longitude": longitude,
        "location": location,
        "formatted_location": f"City: {g.city}, State: {g.state}, Country: {g.country}"
    })





@app.route('/text_to_speech', methods=['POST'])
def text_to_speech():
    try:
        # Print the incoming JSON data for debugging
        print("Received data:", request.json)

        # Extract text from JSON request
        data = request.json
        text = data.get('text', '')

        if not text:
            return jsonify({"status": "error", "message": "Text input is required."}), 400

        # Convert text to speech
        tts = gTTS(text=text, lang='en')

        # Save the audio to a BytesIO object instead of a file
        audio_file = io.BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)

        # Return the audio file to the frontend
        return send_file(audio_file, mimetype='audio/mp3', as_attachment=True, download_name='output.mp3')

    except Exception as e:
        # Log the error on the server-side and return a 500 response
        print(f"Error occurred: {e}")
        return jsonify({"status": "error", "message": "Internal server error."}), 500
 
    
@app.route('/send_sms', methods=['POST'])
def send_sms():
    data = request.json
    api_secret = data['api_secret']
    device_id = data['device_id']
    phone = data['phone']
    message_text = data['message']

    message = {
        "secret": api_secret,
        "mode": "devices",
        "device": device_id,
        "sim": 1,
        "priority": 1,
        "phone": phone,
        "message": message_text
    }

    response = requests.post("https://www.cloud.smschef.com/api/send/sms", params=message)
    
    if response.status_code == 200:
        result = response.json()
        return jsonify({"status": "success", "result": result})
    else:
        return jsonify({"status": "error", "status_code": response.status_code, "response": response.text})

@app.route('/send_bulk_mail', methods=['POST'])
def send_bulk_email():
    data = request.json
    sender_email = data['sender_email']
    sender_password = data['sender_password']
    recipient_list = data['recipient_list']
    subject = data['subject']
    body = data['body']

    if 'recipient_list' not in data:
        return jsonify({"status": "error", "message": "'recipient_list' key is missing"}), 400

    # Ensure recipient_list is a list of emails
    if not isinstance(recipient_list, list) or not recipient_list:
        return jsonify({"status": "error", "message": "Recipient list is empty or not a list"}), 400

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Prepare the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ", ".join(recipient_list)  # Join recipients into a single string
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))  # Adjust MIMEText if you want to use HTML

        # Send the email to all recipients at once
        server.sendmail(sender_email, recipient_list, msg.as_string())

        server.quit()
        return jsonify({"status": "success", "message": "Bulk emails sent successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Task 1: Dataset Processing and Model Creation

def process_dataset():
    # Load Employee Dataset from CSV
    data_path = r'C:/abinash/employee_data.csv'
    df = pd.read_csv(data_path)
    
    # Check for missing values and handle them (dropping for simplicity)
    df.dropna(inplace=True)
    
    # Let's assume the dataset has 'Experience', 'location', 'Salary' columns
    # Preprocess the dataset for ML (Label Encoding 'location')
    label_encoder = LabelEncoder()
    df['location'] = label_encoder.fit_transform(df['location'])
    
    # Features: Experience and location; Target: Salary (Binary: High or Low)
    X = df[['Experience', 'location']]  # Features
    y = (df['Salary'] > 50000).astype(int)  # Target: 1 if salary > 50000, else 0
    
    # Scale the features for better performance
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    # Train a Logistic Regression model
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    
    # Predict and calculate accuracy
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    return accuracy# Task 2: Upload and Integrate Model in Web App (Uses pre-trained model)


@app.route('/predict', methods=['POST'])
def predict():
    accuracy=process_dataset()    
    if accuracy >= 80:
        jsonify({
            "message": "Dataset processed and model trained successfully",
            "accuracy": accuracy
        })
    else:
        jsonify({
            "message": "Dataset processed and model not trained successfully",
            "accuracy": accuracy
        })
            
    try:
        data = request.json['data']  # User will provide input data for prediction
        prediction = model.predict([data])  # Predict based on input data
        return jsonify({"prediction": prediction[0]})
    except:
        return jsonify({"error": "Invalid input data"})

# Other image processing and filter application routes (tasks 3-6) remain the same


# Task 3: Click and Crop Image (Simulated Upload for Web)
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image part"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    img_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(img_path)

    # Process and crop face using OpenCV
    cropped_face_path = crop_face(img_path)

    return jsonify({"message": "Image uploaded and face cropped", "cropped_face_path": cropped_face_path})

def crop_face(image_path):
    # Load image
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use pre-trained face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return "No face detected"

    # Crop the first detected face
    for (x, y, w, h) in faces:
        face_img = img[y:y+h, x:x+w]
        cropped_face_path = os.path.join(UPLOAD_FOLDER, 'cropped_face.jpg')
        cv2.imwrite(cropped_face_path, face_img)
        return cropped_face_path

# Task 4: Apply Filters to an Image                                                                                                      done
@app.route('/apply_filter', methods=['POST','GET'])
def apply_filter():
    if 'image' not in request.files:
        return jsonify({"error": "No image part"}), 400
    file = request.files['image']
    img_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(img_path)

    pil_img = Image.open(img_path)

    # Apply a filter (e.g., BLUR)
    filtered_img = pil_img.filter(ImageFilter.GaussianBlur(radius=100))
    filtered_img_path = os.path.join(UPLOAD_FOLDER, 'filtered_image.jpg')
    filtered_img.save(filtered_img_path)

    return jsonify({"message": "Filter applied", "filtered_image_path": filtered_img_path})

# Task 5: Create Custom Image using NumPy                                                                                             done
@app.route('/create_custom_image', methods=['POST','GET'])
def create_custom_image():
    # Create a blank 200x200 image with RGB channels
    data = np.zeros((200, 200, 3), dtype=np.uint8)
    
    # Convert NumPy array to an image using PIL
    custom_image = Image.fromarray(data, 'RGB')
    
    # Create a draw object
    draw = ImageDraw.Draw(custom_image)
    
    # Background color (sky blue)
    draw.rectangle([0, 0, 200, 200], fill=(135, 206, 235))
    
    # Draw the eagle shape
    # Head of the eagle (white circle)
    draw.ellipse((80, 40, 120, 80), fill=(255, 255, 255), outline=(0, 0, 0), width=2)  # Head (white)
    
    # Eye of the eagle
    draw.ellipse((105, 55, 110, 60), fill=(0, 0, 0))  # Eye
    
    # Beak (yellow triangle)
    draw.polygon([(120, 60), (135, 65), (120, 70)], fill=(255, 223, 0), outline=(0, 0, 0), width=1)
    
    # Body of the eagle (brown oval)
    draw.ellipse((70, 80, 130, 150), fill=(139, 69, 19), outline=(0, 0, 0), width=2)
    
    # Wings (brown arcs)
    draw.polygon([(40, 90), (70, 120), (30, 160), (70, 110)], fill=(139, 69, 19), outline=(0, 0, 0), width=2)  # Left wing
    draw.polygon([(130, 110), (170, 160), (130, 120), (160, 90)], fill=(139, 69, 19), outline=(0, 0, 0), width=2)  # Right wing
    
    # Tail (white triangle)
    draw.polygon([(90, 150), (110, 150), (100, 180)], fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    
    # Feet (yellow lines)
    draw.line((95, 150, 95, 170), fill=(255, 223, 0), width=3)  # Left foot
    draw.line((105, 150, 105, 170), fill=(255, 223, 0), width=3)  # Right foot
    
    # Optional: Add clouds or other background elements for better scenery
    
    # Save the custom image with the eagle shape
    custom_img_path = os.path.join(UPLOAD_FOLDER, 'custom_eagle_image.png')
    custom_image.save(custom_img_path)

    return jsonify({"message": "Detailed eagle image created", "custom_image_path": custom_img_path})

# Task 6: Apply Cool Filters (Sunglasses, Stars) on an Image                                                                        done
@app.route('/apply_cool_filters', methods=['POST'])
def apply_cool_filters():
    if 'image' not in request.files:
        return jsonify({"error": "No image part"}), 400
    
    file = request.files['image']
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(img_path)

    # Read the image with OpenCV
    img_cv2 = cv2.imread(img_path)
    gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return jsonify({"error": "No face detected"}), 400

    for (x, y, w, h) in faces:
        # Draw rectangle around face (optional, or use it to align sunglasses)
        # cv2.rectangle(img_cv2, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Detect eyes within the face region
        face_region = gray[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(face_region)

        for (ex, ey, ew, eh) in eyes:
            # Draw sunglasses (rectangle or overlay an actual image of sunglasses)
            # Here we draw a black rectangle over the eyes (you can modify the coordinates as needed)
            cv2.rectangle(img_cv2, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (0, 0, 0), -1)

    # Save the modified image
    filtered_img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'cool_filtered_image.jpg')
    cv2.imwrite(filtered_img_path, img_cv2)

    return jsonify({"message": "Cool filters applied", "filtered_image_path": filtered_img_path})


if __name__ == '__main__':
    # Load Employee dataset when app starts
    df = pd.read_csv(r'C:/abinash/uploads/employee_data.csv')
    label_encoder = LabelEncoder()
    df['location'] = label_encoder.fit_transform(df['location'])
    X = df[['Experience', 'location']]
    y = (df['Salary'] > 50000).astype(int)
    
    # Train model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    
    # Start Flask app
    app.run(debug=True)
