import sqlite3
import json
from datetime import date
from sqlite3 import Cursor
from sqlite3.dbapi2 import Connection
from flask import Flask, render_template, url_for, send_from_directory, request, redirect
from flask_dropzone import Dropzone
import os
import array

UPLOAD_FOLDER = './static/document/'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
adm: array = ['thyc', 'admin']
dropzone = Dropzone(app)

app.secret_key = 'super_secret_key'


@app.route('/', methods=['GET', 'POST'])
def user():
    logger: str = os.getlogin()
    if adm.__contains__(logger):
        etat = True
    else:
        etat = False

    if request.method == 'POST':
        code = request.form.get('filter')
        return redirect(url_for('get_doc_by_filter', dossier=str(code), etat=etat))

    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    rows = db.execute("SELECT *, date(creation) AS date_creation, date(maj) AS date_maj  FROM doc ORDER BY code;").fetchall()
    return render_template('index.html', doc=rows, etat=etat)


@app.route('/admin/')
def admin():
    logger: str = os.getlogin()
    if adm.__contains__(logger):
        etat = True
        conn: Connection = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        db: Cursor = conn.cursor()
        rows = db.execute("SELECT *, date(creation) AS date_creation, date(maj) AS date_maj  FROM doc ORDER BY code;").fetchall()
        return render_template('admin.html', doc=rows, user=logger, etat=etat)
    else:
        return redirect(url_for('user'))


@app.route('/admin/code/<code>', methods=['GET', 'POST'])
def edit_doc_by_code(code):
    logger: str = os.getlogin()
    print("##### " + request.method + "########")
    print(request.args)
    print(request.data)
    print(request.form)
    print(logger)
    if adm.__contains__(logger):
        print("#### go")
        if request.method == 'POST':
            print("#### Post")
            print(request.form.get('enregistre'))
            code = request.form.get('codeDocument')
            libelle = request.form.get('libelleDocument')
            lien = request.form.get('lienDocument')
            etiquette = request.form.get('etiquetteDocument')
            creation: date = request.form.get('dateCreation')
            maj: date = request.form.get('dateMaj')
            if request.form.get('enregistre'):
                print("enregistre sans upload")
                update_doc(code, libelle, lien, etiquette, creation, maj)
                return redirect(url_for('admin'))
            elif request.form.get('ajoute'):
                print("ajoute sans upload")
                insert_doc(code, libelle, lien, etiquette, creation, maj)
                return redirect(url_for('edit_doc_by_code', code=code))
            '''elif request.files:
                document = request.files["document"]
                if document.filename != '':
                    if request.form.get('enregistre'):
                        print("enregistre")
                        document.save(os.path.join(app.config["UPLOAD_FOLDER"], document.filename))
                        nom_document = document.filename
                        update_doc(code, libelle, nom_document, etiquette, creation, maj)
                        # return redirect(request.url)
                        return redirect(url_for('admin'))
                    elif request.form.get('ajoute'):
                        print("ajoute")
                        document.save(os.path.join(app.config["UPLOAD_FOLDER"], document.filename))
                        nom_document = document.filename
                        insert_doc(code, libelle, nom_document, etiquette, creation, maj)
                        # return redirect(url_for('edit_doc_by_code', code=code))
                        return redirect(url_for('admin'))
                elif request.form.get('enregistre'):
                    print("enregistre sans upload")
                    update_doc(code, libelle, lien, etiquette, creation, maj)
                    return redirect(url_for('edit_doc_by_code', code=code))
                elif request.form.get('ajoute'):
                    print("ajoute sans upload")
                    insert_doc(code, libelle, lien, etiquette, creation, maj)
                    return redirect(url_for('edit_doc_by_code', code=code))'''
        else:
            etat = True
            conn = sqlite3.connect('database.db')
            conn.row_factory = sqlite3.Row
            db = conn.cursor()
            rows = db.execute('SELECT *, date(creation) AS date_creation, date(maj) AS date_maj FROM doc WHERE code=? ORDER BY code;', [code]).fetchall()
            return render_template('edition.html', doc=rows, user=logger, etat=etat)

    print("4")
    etat = True
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    rows = db.execute('SELECT *, date(creation) AS date_creation, date(maj) AS date_maj FROM doc WHERE code=? ORDER BY code;', [code]).fetchall()
    return render_template('edition.html', doc=rows, user=logger, etat=etat)


@app.route('/admin2/code/<code>', methods=['GET', 'POST'])
def edit_doc_by_code2(code):
    logger: str = os.getlogin()
    print("##### " + request.method + "########")
    print(request.args)
    print(request.data)
    print(request.form)

    if adm.__contains__(logger):
        if request.method == 'POST':
            code = request.form.get('codeDocument')
            libelle = request.form.get('libelleDocument')
            lien = request.form.get('lienDocument')
            etiquette = request.form.get('etiquetteDocument')
            creation: date = request.form.get('dateCreation')
            maj: date = request.form.get('dateMaj')
            if request.form.get('enregistre'):
                print("enregistre sans upload")
                update_doc(code, libelle, lien, etiquette, creation, maj)
                return redirect(url_for('admin'))
            elif request.form.get('ajoute'):
                print("ajoute sans upload")
                insert_doc(code, libelle, lien, etiquette, creation, maj)
                return redirect(url_for('edit_doc_by_code', code=code))
            elif request.files:
                document = request.files["document"]
                if document.filename != '':
                    if request.form.get('enregistre'):
                        print("enregistre")
                        document.save(os.path.join(app.config["UPLOAD_FOLDER"], document.filename))
                        nom_document = document.filename
                        update_doc(code, libelle, nom_document, etiquette, creation, maj)
                        # return redirect(request.url)
                        return redirect(url_for('admin'))
                    elif request.form.get('ajoute'):
                        print("ajoute")
                        document.save(os.path.join(app.config["UPLOAD_FOLDER"], document.filename))
                        nom_document = document.filename
                        insert_doc(code, libelle, nom_document, etiquette, creation, maj)
                        # return redirect(url_for('edit_doc_by_code', code=code))
                        return redirect(url_for('admin'))
                elif request.form.get('enregistre'):
                    print("enregistre sans upload")
                    update_doc(code, libelle, lien, etiquette, creation, maj)
                    return redirect(url_for('edit_doc_by_code', code=code))
                elif request.form.get('ajoute'):
                    print("ajoute sans upload")
                    insert_doc(code, libelle, lien, etiquette, creation, maj)
                    return redirect(url_for('edit_doc_by_code', code=code))

    print("4")
    etat = True
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    rows = db.execute('SELECT *, date(creation) AS date_creation, date(maj) AS date_maj FROM doc WHERE code=? ORDER BY code;', [code]).fetchall()
    return render_template('edition.html', doc=rows, user=logger, etat=etat)


@app.route('/filter/code/<code>')
def edit_doc_by_code_filter(code):
    return redirect(url_for('edit_doc_by_code', code=code))


@app.route('/code/<code>')
def get_doc_by_code(code):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    rows = db.execute('SELECT * FROM doc WHERE code=?;', [code]).fetchall()
    return render_template('index.html', doc=rows, user="")


@app.route('/filter/<dossier>')
def get_doc_by_filter(dossier):
    logger: str = os.getlogin()
    page = 'index.html'

    if adm.__contains__(logger):
        etat = True
        page = 'admin.html'
    else:
        etat = False

    filtre = 'Dossier : ' + dossier
    code = dossier + '%'
    libelle = '%' + dossier + '%'
    dossier = '%;' + dossier + ';%'
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    rows = db.execute('SELECT *, date(creation) AS date_creation, date(maj) AS date_maj  FROM doc WHERE etiquette LIKE ? OR libelle Like ? OR code LIKE ? ORDER BY code;', [dossier, libelle, code]).fetchall()
    return render_template(page, doc=rows, filtre=filtre, etat=etat)


@app.route('/filter/')
def erreur404():
    return redirect(url_for('user'))


@app.route('/api/code/<code>')
def get_json_doc_by_code(code):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    rows = db.execute('SELECT * FROM doc WHERE code=?;', [code]).fetchall()
    obj = json.dumps([dict(ix) for ix in rows])
    return obj


@app.route('/api/filter/<dossier>')
def get_json_doc_by_filter(dossier):
    dossier = '%;' + dossier + ";%"
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    rows = db.execute('SELECT * FROM doc WHERE dossier LIKE ?;', [dossier]).fetchall()
    obj = json.dumps([dict(ix) for ix in rows])
    return obj


@app.route('/document/<doc>')
def publish(doc):
    return send_from_directory("./static/document/", doc)


def update_doc(code, libelle, lien, dossier):
    sql = ''' UPDATE doc
              SET libelle = ?,
                  lien = ?,
                  dossier = ?
              WHERE code = ?;'''
    column_values = (str(libelle), str(lien), str(dossier), str(code))
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(sql, column_values)
    conn.commit()
    conn.cursor().fetchall()


def update_doc(code, libelle, lien, dossier, creation, maj):
    sql = ''' UPDATE doc
              SET libelle = ?,
                  lien = ?,
                  etiquette = ?,
                  creation = DATE(?),
                  maj = DATE(?)
              WHERE code = ?;'''
    column_values = (str(libelle), str(lien), str(dossier), creation, maj, str(code))
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(sql, column_values)
    conn.commit()
    conn.cursor().fetchall()


def insert_doc(code, libelle, lien, dossier, creation, maj):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO doc (code,libelle,lien,etiquette, creation, maj) VALUES (?,?,?,?,?,?)", (str(code), str(libelle), str(lien), str(dossier), creation, maj))
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")


def insert_doc(code, libelle, lien, dossier):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO doc (code,libelle,lien,etiquette) VALUES (?,?,?,?)", (str(code), str(libelle), str(lien), str(dossier)))
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")


@app.route("/upload/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if request.files:
            document = request.files.get('file')  # ["document"]
            '''if document.filename != '':'''
            document.save(os.path.join(app.config["UPLOAD_FOLDER"], document.filename))
            '''nom_document = document.filename'''
            '''return render_template("upload.html", lien=nom_document)'''
            '''return redirect(request.url)'''
    return render_template("upload.html")
    '''if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], f.filename))
        return redirect(request.url)
    return render_template("upload.html")'''


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == '__user__':
    app.run(debug=True)
