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
    GOOGLE_API_KEY = 'google api key'  # Replace with a secure method to load the API key
    CSE_ID = 'custom search engine id'  # Replace with a secure method to load the CSE ID

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


if __name__ == '__main__':
    app.run(debug=True)
