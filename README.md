https://myaccount.google.com/apppasswords set SMTP_PASSWORD

- python -m venv .venv
- pip install -r requirements.txt

docker build -t fastapi-email-service .
docker run -p 8809:8809 --env-file .env --name fastapi-email-service fastapi-email-service