import requests
import pdfkit
import smtplib
from email.mime.text import MIMEText

num_questions = 50

def fetch_questions(endpoint, num_questions):
    # Function to fetch the questions from the API endpoint
    response = requests.get(endpoint)
    data = response.json()
    questions = data["items"][:num_questions]
    return questions

def create_pdf(questions):
    # Function to create a PDF containing the questions
    html_content = "<html><head><style>img {max-width: 50%;}</style></head><body>"
    question_number = 1

    for question in questions:
        # Extract question details
        title = question["title"]
        views = question["view_count"]
        link = question["link"]

        # Check if the "imageURL" key exists in the dictionary
        if "imageURL" in question:
            image_url = question["imageURL"]
        else:
            image_url = ""

        # Generate HTML content for the question
        html_content += f"<h2>{question_number}. {title}</h2>"
        html_content += f"<p>Views: {views}</p>"
        html_content += f'<a href="{link}">{link}</a>'
        html_content += f'<img src="{image_url}"><br><br>'

        question_number += 1

    html_content += "</body></html>"

    # Configure PDFKit and generate the PDF
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdfkit.from_string(html_content, "questions.pdf", configuration=config)

def send_email(recipient, subject, text_content):
    # Function to send the extracted questions to the provided email address
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "mosesoleka@gmail.com"
    password = "waztyctkkrilyerc"

    # Create the email message
    message = MIMEText(text_content, "html")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient

    # Connect to the SMTP server, login, and send the message
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(message)

def main():
    # Main function to execute the program
    url = input("Enter the URL of the site: ")
    #url example = api.stackexchange.com/2.3/questions?site=stackoverflow&pagesize=50&sort=votes
    endpoint = f"https://{url}"
    name = input("Enter your name: ")
    email = input("Enter your email: ")

    # Fetch the questions from the API
    questions = fetch_questions(endpoint, num_questions)

    # Generate the HTML content for the email
    html_content = "<html><body>"
    html_content += f"<h2>Extracted Questions for {name}</h2>"
    html_content += "<ul>"

    for question in questions:
        # Extract question details
        title = question["title"]
        views = question["view_count"]
        link = question["link"]

        # Check if the "imageURL" key exists in the dictionary
        if "imageURL" in question:
            image_url = question["imageURL"]
        else:
            image_url = ""

        # Generate HTML content for each question
        html_content += "<li>"
        html_content += f"<h3>{title}</h3>"
        html_content += f"<p>Views: {views}</p>"
        html_content += f'<p><a href="{link}">{link}</a></p>'
        html_content += f'<img src="{image_url}">'
        html_content += "</li>"

        html_content += "</ul>"
        html_content += "</body></html>"
    
    # Create the PDF with the questions
    create_pdf(questions)

    # Send the email with the extracted questions
    subject = f'Extracted Questions for {name}'
    send_email(email, subject, html_content)

    print("PDF created and email sent successfully.")
    input("Press enter to quit")

if __name__ == "__main__":
    main()