import pandas as pd
import smtplib
from email.mime.text import MIMEText

# SMTP server configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'chauhan.vishal4943@gmail.com'
smtp_password = 'ntvu skod dibv cabm'

try:
    # Read CSV file with email, subject, and body
    df = pd.read_csv('emails.csv')
    print("\nCSV file contents:")
    print(df.head())
    
    # Verify required columns exist
    required_columns = ['Email', 'Subject', 'Body']
    if not all(col in df.columns for col in required_columns):
        raise Exception(f"CSV must contain these columns: {required_columns}")
    
    # Clean the email addresses
    df['Email'] = df['Email'].astype(str).str.strip()
    
    # Remove any rows with invalid emails
    df = df[df['Email'].str.contains('@')]
    
    if len(df) == 0:
        raise Exception("No valid email addresses found in the file")
    
    print("\nValid emails found:")
    print(df['Email'].tolist())
    
    # Send emails
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        
        for _, row in df.iterrows():
            msg = MIMEText(row['Body'])
            msg['Subject'] = row['Subject']
            msg['From'] = smtp_user
            msg['To'] = row['Email']

            server.sendmail(smtp_user, row['Email'], msg.as_string())
            print(f"Email sent to: {row['Email']}")
            
        print("All emails have been sent.")

except Exception as e:
    print(f"An error occurred: {str(e)}")