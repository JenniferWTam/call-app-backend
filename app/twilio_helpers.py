from twilio.rest import Client
import os

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

def make_twilio_call(user_phone_number, script):
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

        call = client.calls.create(
            twiml=f"<Response><Say>{script}</Say></Response>",
            to=user_phone_number,
            from_=TWILIO_PHONE_NUMBER
        )

        return True

    except Exception as e:
        print("Twilio call error:", str(e))
        return False
