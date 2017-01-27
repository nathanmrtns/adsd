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
        db.session.add(registro)
        db.session.commit()
        registro = Registro.query.filter_by(texto='textinho').first()
        if registro:
            return registro.texto

@app.route('/read', methods=['GET', 'POST'])
def read():
    if request.method == 'GET':
        registro = Registro.query.filter_by(texto='textinho').first()
        if registro:
            print registro
            return registro.texto
        return "EMPTY"

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0')


