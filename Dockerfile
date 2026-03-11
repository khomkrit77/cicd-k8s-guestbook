FROM python:3.9-alpine
WORKDIR /app
# ติดตั้ง Library สำหรับคุยกับ Redis
RUN pip install flask redis
COPY . .
# ย้าย index.html ไปไว้ในโฟลเดอร์ templates (มาตรฐานของ Flask)
RUN mkdir templates && mv index.html templates/index.html
EXPOSE 80
CMD ["python", "app.py"]
