from flask import Flask, request, jsonify
from dotenv import load_dotenv
from app import app
import requests
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
import os
from datetime import datetime
import requests

load_dotenv()

app = Flask(__name__)

@app.route('/make_reservation', methods=['POST'])
def make_reservation():
    try:
        data = request.get_json()

        # Extract user details from the frontend request
        user_name = data['userName']
        user_phone_number = data['userPhoneNumber']
        party_size = data['partySize']
        restaurant_name = data['restaurantName']
        reservation_time_str = data['reservationTime']
        
        # Parse the date string into a datetime object
        reservation_time_str = data['reservationTime']
        reservation_time = datetime.strptime(reservation_time_str, '%m-%d-%YT%H:%M:%S')


        # Generate prompt using OpenAI
        prompt = f"Hello, {user_name} would like to make a reservation for {party_size} at {reservation_time.strftime('%Y-%m-%d %H:%M')}. Press one if that is available, press two if you're not available, press three if you would like some more time."

        # Rest of your backend code remains unchanged...
        
        # Call OpenAI to get the reservation conversation
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json={
            "model": "gpt-3.5-turbo",  # Include the model parameter
            "messages": [{"role": "user", "content": prompt}]
        })

        if response.status_code != 200:
            print(response.json())  # Add this line to print the response content
            return jsonify({"status": "error", "message": "Failed to get response from OpenAI"}), 500

        data = response.json()

        if "choices" not in data or len(data["choices"]) == 0 or "text" not in data["choices"][0]:
            return jsonify({"status": "error", "message": "Invalid response from OpenAI"}), 500

        reply = data["choices"][0]["text"].strip()

        conversation = []

        # Initiate the conversation with the initial prompt
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json={
            "model": "gpt-3.5-turbo",  # Include the model parameter
            "messages": [{"role": "user", "content": prompt}]
        })

        conversation.extend(response.json()["choices"][0]["message"]["content"].split("\n"))

        # Iterate through the conversation with the restaurant until a reservation is made
        while True:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": conversation[-1]}]
            })

            reply = response.json()["choices"][0]["message"]["content"].strip()
            conversation.append(reply)

            # Check if the conversation indicates a reservation is made
            if "reservation confirmed" in reply.lower():
                break

        # Initiate the Twilio call to the restaurant
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

        # Replace this with the restaurant's phone number on file
        restaurant_phone_number = "2489461263"

        call = client.calls.create(
            twiml=f"<Response><Say>{reply}</Say></Response>",
            to=restaurant_phone_number,
            from_=TWILIO_PHONE_NUMBER
        )
        # Send an SMS back to the user
        client.messages.create(
            body=f"Your reservation at {restaurant_name} is confirmed.",
            to=user_phone_number,
            from_=TWILIO_PHONE_NUMBER
        )

        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)