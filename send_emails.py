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

def read_template(template_path):
    """Read the template file"""
    with open(template_path, 'r', encoding='utf-8') as file:
        return file.read().strip()  # Add strip() to remove extra whitespace

def fill_template(template, **kwargs):
    """Fill the template with provided values"""
    try:
        # Default values
        defaults = {
            'title': 'Cricket Tournament Sponsorship',
            'main_content': 'We are excited to invite you to sponsor our upcoming cricket tournament. Your support would mean a lot to us!',
            'footer_text': '© 2024 Cricket Tournament. All rights reserved.',
        }
        
        # Update defaults with provided values
        defaults.update(kwargs)
        
        # Fill template
        return template.format(**defaults)
    except KeyError as e:
        print(f"Missing template variable: {e}")
        raise
    except Exception as e:
        print(f"Error filling template: {e}")
        raise

def attach_file(msg, filepath):
    """Attach a file to the email message"""
    try:
        with open(filepath, 'rb') as f:
            file_name = os.path.basename(filepath)
            part = MIMEBase('application', "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
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
    # Read the email template
    template = read_template('templates/email_template.html')
    
    # Read CSV file
    df = pd.read_csv('emails.csv')
    print("\nCSV file contents:")
    print(df.head())
    print("\nColumns in DataFrame:", list(df.columns))  # Add this line for debugging
    
    # Verify required columns exist
    required_columns = ['Email', 'Subject']
    if not all(col in df.columns for col in required_columns):
        raise Exception(f"CSV must contain these columns: {required_columns}")
    
    # Clean the email addresses
    df['Email'] = df['Email'].astype(str).str.strip()
    df = df[df['Email'].str.contains('@')]
    
    if len(df) == 0:
        raise Exception("No valid email addresses found in the file")
    
    # Send emails
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        
        for _, row in df.iterrows():
            try:
                # Create message container
                msg = MIMEMultipart('alternative')
                msg['Subject'] = row['Subject']
                msg['From'] = smtp_user
                msg['To'] = row['Email']
                
                # Fill template with row data
                template_data = row.to_dict()  # Convert row to dictionary
                html_content = fill_template(template, **template_data)
                
                # Attach HTML content
                msg.attach(MIMEText(html_content, 'html'))
                
                # Add attachments if specified
                if 'Attachments' in row and pd.notna(row['Attachments']):
                    for filepath in row['Attachments'].split(';'):
                        filepath = filepath.strip()
                        if os.path.exists(filepath):
                            attach_file(msg, filepath)
                        else:
                            print(f"Warning: Attachment not found: {filepath}")

                server.sendmail(smtp_user, row['Email'], msg.as_string())
                print(f"Email sent to: {row['Email']}")
            
            except Exception as e:
                print(f"Error sending email to {row['Email']}: {str(e)}")
                continue
            
        print("All emails have been sent.")

except Exception as e:
    print(f"An error occurred: {str(e)}")