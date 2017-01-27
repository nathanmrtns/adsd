from flask import Flask
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:root00@localhost/db'
db = SQLAlchemy(app)

class Registro(db.Model):
    __tablename__ = "registro"
    id = db.Column('id', db.Integer, primary_key=True)
    texto = db.Column('texto', db.Unicode)


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
        if registro:
            return str(tf)

@app.route('/read', methods=['GET', 'POST'])
def read():
    if request.method == 'GET':
        import time
        ti = time.time()
        registro = Registro.query.filter_by(texto='textinho').first()
        tf = time.time() - ti
        if registro:
            return str(tf)
        return "EMPTY"

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0')
