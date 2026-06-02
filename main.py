from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from email_service import send_email
import uvicorn


app = FastAPI(title="FastAPI Email Service", version="1.0.0")


class EmailRequest(BaseModel):
    subject: str
    recipients: List[EmailStr]
    cc: Optional[List[EmailStr]] = None
    body: str
    html_body: Optional[str] = None


@app.get("/")
def read_root():
    return {"message": "FastAPI Email Service is running!"}

@app.post('/webhook/email')
async def webhook_email(request: Request):
    """
    Expected JSON body:
    {
        "subject": "Email Subject",
        "recipients": ["recipient@example.com"],
        "cc": ["cc@example.com"], (optional)
        "body": "Plain text body",
        "html_body": "<h1>HTML Body</h1>"  (optional)
    }
    """
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or empty JSON body")

    try:
        success, message = await send_email(
            subject=payload.get("subject"),
            recipients=payload.get("recipients", []),
            cc=payload.get("cc", []),
            body=payload.get("body"),
            html_body=payload.get("html_body")
        )
        
        if success:
            return {"message": message}
        else:
            raise HTTPException(status_code=500, detail=message)
    except HTTPException:
        raise
        #print(f"Received email request: {payload}")
        return {"message": "Email request received", "payload": payload}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8809, reload=True)