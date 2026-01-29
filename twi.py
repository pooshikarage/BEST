from twilio.rest import Client

# Twilio credentials
account_sid = "ACe1322f5e137fba1bab5d01d4e7859feb"
auth_token = "8327fad75b5cf9b2b9e00d60f7aa3d60"

client = Client(account_sid, auth_token)

message = client.messages.create(
    body="🚨 Detection Alert:Garbage Detected!",
    from_="+19146771225",   # Twilio number
    to="+919361319454"     # Your phone number
)

print("Message sent:", message.sid)
