from flask import Flask, request, render_template, redirect, url_for
import redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_msg = request.form.get('msg')
        if user_msg:
            r.rpush('guestbook_keys', user_msg)
        return redirect(url_for('index'))
    
    messages = r.lrange('guestbook_keys', 0, -1)
    return render_template('index.html', messages=messages)

# --- ส่วนที่เพิ่มใหม่: ระบบลบข้อมูล ---
@app.route('/delete/<int:index>')
def delete_message(index):
    # ดึงค่าข้อความที่ตำแหน่ง index ออกมา
    msg_to_delete = r.lindex('guestbook_keys', index)
    if msg_to_delete:
        # ลบข้อความนั้นออกจาก List (Redis LREM: ลบค่านี้จำนวน 1 ตัว)
        r.lrem('guestbook_keys', 1, msg_to_delete)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
