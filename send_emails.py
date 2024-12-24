import pandas as pd
import smtplib
from email.mime.text import MIMEText

# Email configuration
subject = "Sponsorship Opportunity for Our Cricket Tournament"
body = """Dear Businessman,

We are excited to invite you to sponsor our upcoming cricket tournament. Your support would mean a lot to us!

Best Regards,
[Your Name]
[Your Contact Information]
"""

# SMTP server configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'chauhan.vishal4943@gmail.com'
smtp_password = 'ntvu skod dibv cabm'

try:
    # Try to read the file first as text to inspect its contents
    with open('emails.csv', 'r') as file:
        print("First few lines of the CSV file:")
        for i, line in enumerate(file):
            if i < 5:  # Print first 5 lines
                print(f"Line {i+1}: {line.strip()}")
            else:
                break
        print("-------------------")
    
    # Try reading with different parameters
    try:
        # First attempt: standard reading
        df = pd.read_csv('emails.csv')
    except:
        try:
            # Second attempt: no header
            df = pd.read_csv('emails.csv', header=None, names=['Email'])
        except:
            try:
                # Third attempt: different separator
                df = pd.read_csv('emails.csv', sep=';')
            except:
                # Final attempt: most flexible reading
                df = pd.read_csv('emails.csv', sep=None, engine='python')

    print("\nCSV file contents:")
    print(df.head())
    print("\nColumns in the DataFrame:", list(df.columns))
    
    # If we have multiple columns, try to identify the email column
    if len(df.columns) > 1:
        # Try to find a column that looks like it contains emails
        email_col = None
        for col in df.columns:
            if df[col].astype(str).str.contains('@').any():
                email_col = col
                break
        
        if email_col:
            df['Email'] = df[email_col]
        else:
            raise Exception("Could not find a column containing email addresses")
    
    # Ensure we have an Email column
    if 'Email' not in df.columns:
        df.columns = ['Email']
    
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
        
        for email in df['Email']:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = smtp_user
            msg['To'] = email

            server.sendmail(smtp_user, email, msg.as_string())
            print(f"Email sent to: {email}")
            
        print("All emails have been sent.")

except Exception as e:
    print(f"An error occurred: {str(e)}")