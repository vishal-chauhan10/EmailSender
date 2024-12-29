import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage
import os

# SMTP server configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'chauhan.vishal4943@gmail.com'
smtp_password = 'ntvu skod dibv cabm'

def read_template(template_path):
    """Read the template file"""
    with open(template_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

def fill_template(template, **kwargs):
    """Fill the template with provided values"""
    try:
        return template.format(**kwargs)
    except KeyError as e:
        print(f"Missing template variable: {e}")
        raise
    except Exception as e:
        print(f"Error filling template: {e}")
        raise

def send_emails(csv_file):
    try:
        # Read the email template
        template = read_template('templates/email_template.html')
        
        # Read CSV file
        df = pd.read_csv(csv_file)
        print(f"Processing {len(df)} recipients...")

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
        successful_sends = 0
        failed_sends = 0
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            
            for _, row in df.iterrows():
                try:
                    # Create message container
                    msg = MIMEMultipart('related')
                    msg['Subject'] = row['Subject']
                    msg['From'] = smtp_user
                    msg['To'] = row['Email']
                    
                    # Create the HTML part
                    html_part = MIMEMultipart('alternative')
                    msg.attach(html_part)
                    
                    # Fill template with row data
                    template_data = row.to_dict()
                    html_content = fill_template(template, **template_data)
                    
                    # Attach HTML content
                    html_part.attach(MIMEText(html_content, 'html'))
                    
                    # Send the email
                    server.sendmail(smtp_user, row['Email'], msg.as_string())
                    print(f"✓ Email sent to: {row['Email']}")
                    successful_sends += 1
                
                except Exception as e:
                    print(f"✗ Error sending email to {row['Email']}: {str(e)}")
                    failed_sends += 1
                    continue
            
        print(f"\nEmail sending completed:")
        print(f"✓ Successful: {successful_sends}")
        print(f"✗ Failed: {failed_sends}")
        print(f"Total: {successful_sends + failed_sends}")
        
        return {
            'success': True,
            'message': f'Emails sent successfully ({successful_sends} sent, {failed_sends} failed)',
            'details': {
                'successful': successful_sends,
                'failed': failed_sends,
                'total': successful_sends + failed_sends
            }
        }

    except Exception as e:
        error_message = f"Error sending emails: {str(e)}"
        print(error_message)
        return {
            'success': False,
            'message': error_message
        }