from flask import Flask
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy
import psutil
import time
import csv

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
        server_resp_timei = time.time()
        registro = Registro(texto='textinho')
        bd_timei = time.time()
        db.session.add(registro)
        db.session.commit()
        bd_timef = time.time() - bd_timei
        registro = Registro.query.filter_by(texto='textinho').first()
        cpu_usage = psutil.cpu_percent(interval=0.1)
        if registro:
            server_resp_timef = time.time() - server_resp_timei
            self.write_data("write", server_resp_timef,bd_timef,cpu_usage)
            return str(server_resp_timef) + " " + str(bd_timef) + " " + str(cpu_usage)

@app.route('/read', methods=['GET', 'POST'])
def read():
    if request.method == 'GET':
        server_resp_timei = time.time()
        bd_timei = time.time()
        registro = Registro.query.filter_by(texto='textinho').first()
        bd_timef = time.time() - bd_timei
        cpu_usage = psutil.cpu_percent(interval=0.1)
        #print cpu_usage
        if registro:
            server_resp_timef = time.time() - server_resp_timei
            write_data("write", server_resp_timef,bd_timef,cpu_usage)
            return str(server_resp_timef) + " " + str(bd_timef) + " " + str(cpu_usage)
        return "EMPTY"

# saves the data
def write_data(command, server_response, bd_response, cpu_usage):
    fd = open("output.csv", 'a')
    output = csv.writer(fd, delimiter=' ')
    output.writerow([command, server_response, bd_response, cpu_usage])
    fd.close()

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0')
