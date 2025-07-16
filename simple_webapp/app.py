from flask import Flask, render_template
import uuid

app = Flask(__name__)
startup_uuid = str(uuid.uuid4())

@app.route('/')
def home():
    return render_template('index.html', uuid=startup_uuid)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
