import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from app.chatbot import ask_ai
from fastapi.middleware.cors import CORSMiddleware
from app.vector_store import get_vectorstore

app = FastAPI()

# CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str


@app.on_event("startup")
def startup_event():
    print("🔥 Preloading vector DB...")
    get_vectorstore()

@app.post("/ask")
def ask_question(data: Query):
    answer = ask_ai(data.query)
    return {"answer": answer}

@app.post("/contact")
def handle_contact(data: ContactRequest):
    smtp_server = os.getenv("SMTP_SERVER", "")
    smtp_port = os.getenv("SMTP_PORT", "587")
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    receiver_email = os.getenv("CONTACT_RECEIVER_EMAIL", "vaibhavrathod303@gmail.com")

    if not all([smtp_server, smtp_user, smtp_password]):
        raise HTTPException(status_code=500, detail="Email service not configured. Please set SMTP environment variables.")

    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = receiver_email
        msg['Subject'] = f"Portfolio Contact: {data.subject}"

        # Create email body (Plain Text fallback)
        text_body = f"""
        New message from your portfolio contact form:
        
        Name: {data.name}
        Email: {data.email}
        Subject: {data.subject}
        
        Message:
        {data.message}
        """

        # Create email body (HTML)
        formatted_message = data.message.replace('\n', '<br>')
        html_body = f"""
        <html>
          <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 0; padding: 0;">
            <div style="max-width: 600px; margin: 40px auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border: 1px solid #e1e8ed;">
              <div style="background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); padding: 30px; text-align: center;">
                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">New Portfolio Inquiry</h1>
                <p style="color: rgba(255,255,255,0.8); margin-top: 5px;">A visitor has reached out to you</p>
              </div>
              <div style="padding: 30px;">
                <div style="margin-bottom: 25px;">
                  <h3 style="color: #4b5563; border-bottom: 2px solid #818cf8; display: inline-block; padding-bottom: 5px; margin-bottom: 15px;">Contact Details</h3>
                  <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                      <td style="padding: 8px 0; color: #6b7280; width: 100px;"><strong>Name</strong></td>
                      <td style="padding: 8px 0; color: #1f2937;">{data.name}</td>
                    </tr>
                    <tr>
                      <td style="padding: 8px 0; color: #6b7280;"><strong>Email</strong></td>
                      <td style="padding: 8px 0;"><a href="mailto:{data.email}" style="color: #4f46e5; text-decoration: none;">{data.email}</a></td>
                    </tr>
                    <tr>
                      <td style="padding: 8px 0; color: #6b7280;"><strong>Subject</strong></td>
                      <td style="padding: 8px 0; color: #1f2937;">{data.subject}</td>
                    </tr>
                  </table>
                </div>
                
                <div style="margin-bottom: 20px;">
                  <h3 style="color: #4b5563; border-bottom: 2px solid #818cf8; display: inline-block; padding-bottom: 5px; margin-bottom: 15px;">Message</h3>
                  <div style="background-color: #f9fafb; border-radius: 8px; padding: 20px; color: #374151; line-height: 1.6; border: 1px solid #f3f4f6;">
                    {formatted_message}
                  </div>
                </div>
              </div>
              <div style="background-color: #f9fafb; padding: 20px; text-align: center; border-top: 1px solid #f3f4f6;">
                <p style="color: #9ca3af; font-size: 13px; margin: 0;">Sent via Vaibhav's Portfolio AI System</p>
              </div>
            </div>
          </body>
        </html>
        """

        msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))

        # Send email
        with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        return {"status": "success", "message": "Email sent successfully"}
    except Exception as e:
        print(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")


# At the bottom:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)