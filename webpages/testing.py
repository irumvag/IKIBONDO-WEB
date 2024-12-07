import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('djanaclet@gmail.com', 'pily zqke qnme pfvv')  # Use your app password
    print("Login successful")
except Exception as e:
    print(f"An error occurred: {e}")

