import smtplib
import pandas as pd
import os
from email.message import EmailMessage

# ------------------------------
# CONFIGURATION — CHANGE THESE
# ------------------------------
EMAIL_ADDRESS = "email"
EMAIL_PASSWORD = "apppPassword"     # Use Gmail App Password
ATTACHMENT_FOLDER = "attachments"

# Load CSV
data = pd.read_csv("data.csv")

# Email server login
server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

for index, row in data.iterrows():
    msg = EmailMessage()
    msg["Subject"] = f"Hello {row['name']} — Your Document"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = row["email"]

    # Email body
    msg.set_content(f"""
Hi {row['name']},

Please find your attached file.

Regards,
Your Company
""")

    # Attachment Handling
    attachment_path = os.path.join(ATTACHMENT_FOLDER, row["attachment"])

    if os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
            msg.add_attachment(
                file_data,
                maintype="application",
                subtype="octet-stream",
                filename=file_name
            )
        print(f"Attached: {file_name} → {row['email']}")
    else:
        print(f"❌ Attachment not found for {row['email']}")
        continue

    # Send email
    server.send_message(msg)
    print(f"✔ Email sent to {row['email']}")

server.quit()
print("\nAll emails sent successfully!")
