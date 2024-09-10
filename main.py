import poplib
from email.parser import BytesParser
from email.policy import default
import re

# Email account credentials
username = input("Nhap Email: ")
password = input("Nhap Password: ")
print("Chon loai code de lay:")
print("1: Lay ma Verify (verify@x.com)")
print("2: Lay ma Login (info@x.com)")
option = int(input("Lua chon: "))
target_senders = {
    1: "verify@x.com",   # Option 1: Login code from verify@x.com
    2: "Your X confirmation code is"     # Option 2: Verification code from info@x.com
}
if option in target_senders:
    target_sender = target_senders[option]
else:
    print("Lua chon khong hop le.")
    exit()

# Custom mail server details
pop3_server = 'mail.mcrdev.tech'
pop3_port = 995  # Standard port for POP3 with SSL

# Define target email subject prefix


try:
    # Connect to the mail server
    server = poplib.POP3_SSL(pop3_server, pop3_port)
    
    # Log in to your account
    server.user(username)
    server.pass_(password)
    
    # Get the number of messages
    message_count, total_size = server.stat()
    print(f"Total messages: {message_count}")
    
    # Iterate over all messages (starting from the newest)
    for i in range(message_count, 0, -1):
        # Fetch the email
        response, lines, octets = server.retr(i)
        
        # Join the lines to get the full message
        message_bytes = b'\n'.join(lines)
        
        # Parse the email content
        parser = BytesParser(policy=default)
        message = parser.parsebytes(message_bytes)
        if target_sender == 'Your X confirmation code is':
            # Check if the email subject starts with "Your X confirmation code is"
            if message['subject'] and target_sender.lower() in message['subject'].lower():

                
                # Use regex to extract the alphanumeric confirmation code from the subject
                code_match = re.search(r'\b[a-zA-Z0-9]{8}\b', message['subject'])
                if code_match:
                    confirmation_code = code_match.group(0)
                    print(f"Confirmation code: {confirmation_code}")
                else:
                    print("No confirmation code found in the subject.")
                
                # Stop after processing the newest matching email
                break
        else:
            if message['from'] and target_sender in message['from'].lower():
                # Extract the plain text content of the email
                email_body = ""
                if message.is_multipart():
                    for part in message.iter_parts():
                        if part.get_content_type() == 'text/plain':
                            email_body = part.get_payload(decode=True).decode()
                            break
                else:
                    email_body = message.get_payload(decode=True).decode()
                    
                # Use regex to extract the 6-digit verification code
                code_match = re.search(r'\b\d{6}\b', email_body)
                if code_match:
                    verification_code = code_match.group(0)
                    print(f"Verification code: {verification_code}")
                else:
                    print("No verification code found.")
                
                # Stop after processing the newest matching email
                break
    
    # Close the connection
    server.quit()

except Exception as e:
    print(f"Error: {str(e)}")
