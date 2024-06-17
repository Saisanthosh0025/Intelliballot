import pandas as pd
import plotly.express as px
from flask import Flask, render_template, request, redirect, url_for
import random
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

def generate_random_credentials():
    """Generate random username and password."""
    characters = "abcdef@#123456789"
    username = ''.join(random.choices(characters, k=10))
    password = ''.join(random.choices(characters, k=10))
    return username, password

def send_credentials_email(username, password, recipient_email):
    """Send credentials to the specified email address."""
    sender_email = "intelliballot.voting@outlook.com"
    sender_password = "Sai1799@"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Your Randomly Generated Credentials"

    body = f"Username: {username}\nPassword: {password}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email sent successfully")
    except smtplib.SMTPAuthenticationError as e:
        print("Authentication error:", e)
    except smtplib.SMTPException as e:
        print("SMTP error:", e)
    except Exception as e:
        print("An error occurred:", e)

# Dummy user credentials
USER_CREDENTIALS = {}

def get_votes():
    """Read voting data from CSV and return the vote counts for each party."""
    try:
        # Read voting data from CSV file
        voting_data = pd.read_csv('merged_votes.csv')
        
        # Group by party and sum the votes
        vote_counts = voting_data.groupby('Party')['Votes'].sum()
        
        return vote_counts.to_dict()  # Convert to dictionary for easier access in template
    except FileNotFoundError:
        return None

def get_winner_and_margin():
    """Read voting data from CSV and determine the winner and margin of victory."""
    try:
        # Read voting data from CSV file
        voting_data = pd.read_csv('merged_votes.csv')
        
        # Calculate total votes for each party
        vote_counts = voting_data.groupby('Party')['Votes'].sum()
        
        # Determine the winner and the runner-up
        winner_party = vote_counts.idxmax()
        winner_votes = vote_counts.max()
        margin = winner_votes - vote_counts.drop(winner_party).max()
        
        return winner_party, margin, vote_counts
    except FileNotFoundError:
        return None, None, None

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_check():
    username = request.form['username']
    password = request.form['password']
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        return redirect(url_for('index', username=username))
    else:
        error_message = "Incorrect username or password. Please try again."
        return render_template('login.html', error_message=error_message)

@app.route('/index/<username>')
def index(username):
    winner_party, margin, vote_counts = get_winner_and_margin()
    if vote_counts is not None:
        # Generate horizontal bar chart with swapped axes
        fig = px.bar(y=vote_counts.values, x=vote_counts.index, orientation='v', labels={'y': 'Votes', 'x': 'Party'}, 
                     title='Votes for Each Party', color=vote_counts.index)
        graph_json = fig.to_json()

        return render_template('index.html', username=username, winner=winner_party, margin=margin, graph_json=graph_json)
    else:
        return render_template('index.html', username=username, winner=None, margin=None, graph_json=None)

if __name__ == '__main__':
    # Generate random credentials and send them via email
    new_username, new_password = generate_random_credentials()
    USER_CREDENTIALS[new_username] = new_password
    send_credentials_email(new_username, new_password, "pichikasaisantosh2003@gmail.com")

    app.run(debug=True)
