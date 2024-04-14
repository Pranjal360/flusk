# from flask import Flask, request, jsonify
# import joblib
# import numpy as np

# app = Flask(__name__)
# # Load the pickled model
# model = joblib.load('train_model.sav')


# @app.route('/predict', methods=['POST'])
# def predict():
#     # Get input features from request
#     features = request.json['features']

#     input_data_as_numpy_array = np.asarray(features)

#     # reshape the array as we are predicting for one instance
#     input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
#     prediction = model.predict(input_data_reshaped)

#     # Return prediction as JSON response
#     return jsonify({'prediction': prediction.tolist()})


# if __name__ == '__main__':
#     app.run(debug=False, host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()

    sender_email = "noreplytohealdivine8283392@gmail.com"
    sender_name = data.get('name')
    recipient_email = "admin@healdivinebiologicals.in"
    fromEmail = data.get('from')
    subject = data.get('subject')
    message = data.get('body')
    body = f'Hi this message is from {fromEmail}. Here is the message {message}'

    if not all([recipient_email, subject, message]):
        return jsonify({'error': 'Missing required fields'}), 400

    # Connect to SMTP server
    smtp_server = "smtp.elasticemail.com"
    smtp_port = 2525  # Elastic Email SMTP port
    smtp_username = "admin@healdivinebiologicals.in"  # Your Elastic Email username
    smtp_password = "0B3F967257FF559117785C48A0ACF9B7A67E"  # Your Elastic Email password

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Construct email message
        msg = MIMEMultipart()
        msg['From'] = f"{sender_name} <{sender_email}>"
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()

        return jsonify({'message': 'Email sent successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)