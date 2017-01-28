from flask import Flask
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy
import psutil

app = Flask(__name__)
#mysql url - mysql://[user]:[user password]@[localhost]/[database name]
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:root00@localhost/db'
db = SQLAlchemy(app)

class Registro(db.Model):
    __tablename__ = "registro"
    id = db.Column('id', db.Integer, primary_key=True)
    texto = db.Column('texto', db.String(50))

@app.route('/write_and_read', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        import time

        registro = Registro(texto='textinho')
        print registro
        ti = time.time()
        db.session.add(registro)
        db.session.commit()
        tf = time.time() - ti
        registro = Registro.query.filter_by(texto='textinho').first()
        cpu_usage = psutil.cpu_percent(interval=0.1)
        if registro:
            return str(tf) + " " + str(cpu_usage)

@app.route('/read', methods=['GET', 'POST'])
def read():
    if request.method == 'GET':
        import time
        ti = time.time()
        registro = Registro.query.filter_by(texto='textinho').first()
        tf = time.time() - ti
        cpu_usage = psutil.cpu_percent(interval=0.1)
        #print cpu_usage
        if registro:
            return str(tf) + " " + str(cpu_usage)
        return "EMPTY"

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0')
