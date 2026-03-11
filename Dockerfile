FROM python:3.9-alpine
WORKDIR /app

# ติดตั้ง Library
RUN pip install flask redis

# ก๊อปปี้ไฟล์ทั้งหมด (รวมถึงโฟลเดอร์ templates และไฟล์ข้างใน)
COPY . .

# เปิดพอร์ต 80
EXPOSE 80

CMD ["python", "app.py"]
