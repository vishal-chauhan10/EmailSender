import pandas as pd
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders

# SMTP server configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'chauhan.vishal4943@gmail.com'
smtp_password = 'ntvu skod dibv cabm'

def attach_file(msg, filepath):
    """Attach a file to the email message"""
    try:
        with open(filepath, 'rb') as f:
            # Determine the file type and create appropriate MIME part
            file_name = os.path.basename(filepath)
            part = MIMEBase('application', "octet-stream")
            part.set_payload(f.read())
            
            # Encode the attachment
            encoders.encode_base64(part)
            
            # Add header
            part.add_header(
                'Content-Disposition',
                'attachment',
                filename=file_name
            )
            msg.attach(part)
            return True
    except Exception as e:
        print(f"Error attaching file {filepath}: {str(e)}")
        return False

try:
    # Read CSV file with email, subject, body, and attachment paths
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
            # Create message container
            msg = MIMEMultipart()
            msg['Subject'] = row['Subject']
            msg['From'] = smtp_user
            msg['To'] = row['Email']
            
            # Add body
            msg.attach(MIMEText(row['Body'], 'plain'))
            
            # Add attachments if specified
            if 'Attachments' in row and pd.notna(row['Attachments']):
                # Handle multiple attachments separated by semicolons
                attachment_paths = row['Attachments'].split(';')
                for filepath in attachment_paths:
                    filepath = filepath.strip()
                    if os.path.exists(filepath):
                        attach_file(msg, filepath)
                    else:
                        print(f"Warning: Attachment not found: {filepath}")

            server.sendmail(smtp_user, row['Email'], msg.as_string())
            print(f"Email sent to: {row['Email']}")
            
        print("All emails have been sent.")

except Exception as e:
    print(f"An error occurred: {str(e)}")