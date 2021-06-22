import sqlite3
import json
from datetime import date
from sqlite3 import Cursor
from sqlite3.dbapi2 import Connection
from flask import Flask, render_template, url_for, send_from_directory, request, redirect
from flask_dropzone import Dropzone
import os
import array

from document import Document

UPLOAD_FOLDER = './static/document/'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
adm: array = ['thyc', 'admin']
dropzone = Dropzone(app)
app.secret_key = 'super_secret_key'
# docu = Document("", "", "", "", "", "")


@app.route('/', methods=['GET', 'POST'])
def user():
    logger: str = os.getlogin()
    if adm.__contains__(logger):
        etat = True
    else:
        etat = False

    if request.method == 'POST':
        code = request.form.get('filter')
        return redirect(url_for('get_doc_by_filter', etiquette=str(code), etat=etat))

    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    rows = db.execute(
        "SELECT *, date(creation) AS date_creation, date(maj) AS date_maj  FROM doc ORDER BY code;").fetchall()
    return render_template('index.html', doc=rows, etat=etat)


@app.route('/admin/')
def admin():
    logger: str = os.getlogin()
    if adm.__contains__(logger):
        etat = False
        conn: Connection = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        db: Cursor = conn.cursor()
        rows = db.execute(
            "SELECT *, date(creation) AS date_creation, date(maj) AS date_maj  FROM doc ORDER BY code;").fetchall()
        return render_template('admin.html', doc=rows, user=logger, etat=etat)
    else:
        return redirect(url_for('user'))


@app.route('/admin/del/<code>', methods=['GET', 'POST'])
def del_doc_by_code(code):
    print(request.method)
    logger: str = os.getlogin()
    if adm.__contains__(logger):
        print(request.method)
        # if request.method == 'POST':
        delete_doc(code)
        return redirect(url_for('admin'))
    return redirect(url_for('user'))


@app.route('/filter/code/<code>', methods=['GET', 'POST'])
@app.route('/admin/code/<code>', methods=['GET', 'POST'])
def edit_doc_by_code(code):
    logger: str = os.getlogin()
    if adm.__contains__(logger):
        if request.method == 'POST':
            code = request.form.get('codeDocument')
            libelle = request.form.get('libelleDocument')
            lien = request.form.get('lienDocument')
            etiquette = request.form.get('etiquetteDocument')
            creation: date = request.form.get('dateCreation')
            maj: date = request.form.get('dateMaj')
            if request.form.get('enregistre'):
                document = request.files["document"]
                if document.filename != '':
                    document.save(os.path.join(app.config["UPLOAD_FOLDER"], document.filename))
                    lien = document.filename
                update_doc(code, libelle, lien, etiquette, creation, maj)
                return redirect(url_for('edit_doc_by_code', code=code))
            else:
                document = request.files["document"]
                if document.filename != '':
                    document.save(os.path.join(app.config["UPLOAD_FOLDER"], document.filename))
                    lien = document.filename
                insert_doc(code, libelle, lien, etiquette, creation, maj)
                return redirect(url_for('edit_doc_by_code', code=code))
    etat = True
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    rows = db.execute(
        'SELECT *, date(creation) AS date_creation, date(maj) AS date_maj FROM doc WHERE code=? ORDER BY code;',
        [code]).fetchall()
    return render_template('edition.html', doc=rows, user=logger, etat=etat)


@app.route('/admin/code/add/', methods=['GET', 'POST'])
def add_doc():
    logger: str = os.getlogin()
    if adm.__contains__(logger):
        etat = True
        if request.method == 'POST':
            code = request.form.get('codeDocument')
            libelle = request.form.get('libelleDocument')
            lien = request.form.get('lienDocument')
            etiquette = request.form.get('etiquetteDocument')
            creation: date = request.form.get('dateCreation')
            maj: date = request.form.get('dateMaj')
            if request.form.get('enregistre'):
                document = request.files["document"]
                if document.filename != '':
                    document.save(os.path.join(app.config["UPLOAD_FOLDER"], document.filename))
                    lien = document.filename
                insert_doc(code, libelle, lien, etiquette, creation, maj)
                return redirect(url_for('edit_doc_by_code', code=code))
        return render_template('ajout.html', user=logger, etat=etat)
    return redirect(url_for('user'))


@app.route('/code/<code>')
def get_doc_by_code(code):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    rows = db.execute('SELECT * FROM doc WHERE code=?;', [code]).fetchall()
    return render_template('index.html', doc=rows, user="")


@app.route('/admin/filter')
@app.route('/filter')
def get_doc_by_filter():
    logger: str = os.getlogin()
    page = 'index.html'
    array_etiquette: array = None

    etiquette: str = request.args.get('filter').upper()
    vs: str = request.args.get('radio')

    # check_or = ""
    # check_and = ""

    if vs == "ET":
        vs = "AND"
        check_and = "checked"
        check_or = "unchecked"
    elif vs == "OU":
        vs = "OR"
        check_or = "checked"
        check_and = "unchecked"
    else:
        vs = "AND"
        check_and = "checked"
        check_or = "unchecked"

    if etiquette.__contains__(';'):
        array_etiquette = etiquette.split(";")

    if adm.__contains__(logger):
        etat = True
        page = 'admin.html'
    else:
        etat = False

    if array_etiquette is None:
        filtre = 'Filtre : ' + etiquette
        code = etiquette + '%'
        libelle = '%' + etiquette + '%'
        etiquette = '%;' + etiquette + ';%'
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        db = conn.cursor()
        rows = db.execute(
            'SELECT *, date(creation) AS date_creation, date(maj) AS date_maj  FROM doc WHERE etiquette LIKE ? OR libelle Like ? OR code LIKE ? ORDER BY code;',
            [etiquette, libelle, code]).fetchall()
        return render_template(page, doc=rows, filtre=filtre, filter=request.args.get('filter').upper(),
                               check_and=check_and, check_or=check_or, etat=etat)
    else:
        rqt = ""
        filtre = 'Filtre : '
        for etiq in array_etiquette:
            if rqt != "":
                rqt = rqt + " " + vs + " "
                filtre = filtre + " " + request.args.get('radio').lower() + " " + str(etiq)
            else:
                filtre = filtre + str(etiq)

            rqt = rqt + "etiquette LIKE '%;" + str(etiq) + ";%'"

        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        db = conn.cursor()
        rows = db.execute(
            'SELECT *, date(creation) AS date_creation, date(maj) AS date_maj  FROM doc WHERE ' + rqt).fetchall()
        return render_template(page, doc=rows, filtre=filtre, filter=request.args.get('filter').upper(),
                               check_and=check_and, check_or=check_or, etat=etat)


@app.route('/<vs>/<etiquette>')
@app.route('/api/<vs>/<etiquette>')
def api_get_doc_by_filter(vs, etiquette):
    page = 'index.html'
    etat = False
    array_etiquette: array = None

    if etiquette.__contains__(';'):
        array_etiquette = etiquette.split(";")

    if array_etiquette is None:
        filtre = str(etiquette).upper()
        etiquette = '%;' + etiquette + ';%'
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        db = conn.cursor()
        rows = db.execute(
            'SELECT *, date(creation) AS date_creation, date(maj) AS date_maj  FROM doc WHERE etiquette LIKE ? ORDER BY code;',
            [etiquette]).fetchall()
        return render_template(page, doc=rows, filtre=filtre, etat=etat, api=True)
    else:
        rqt = ""
        filtre = ' : '
        for etiq in array_etiquette:
            if rqt != "":
                rqt = rqt + " " + vs + " "
                filtre = filtre + " " + vs + " " + str(etiq).upper()
            else:
                filtre = filtre + str(etiq).upper()

            rqt = rqt + "etiquette LIKE '%;" + str(etiq) + ";%'"

        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        db = conn.cursor()
        rows = db.execute(
            'SELECT *, date(creation) AS date_creation, date(maj) AS date_maj  FROM doc WHERE ' + rqt).fetchall()
        return render_template(page, doc=rows, filtre=filtre, etat=etat, api=True)


@app.route('/json/code/<code>')
def get_json_doc_by_code(code):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    rows = db.execute('SELECT * FROM doc WHERE code=?;', [code]).fetchall()
    obj = json.dumps([dict(ix) for ix in rows])
    return obj


@app.route('/json/filter/<etiquette>')
def get_json_doc_by_filter(etiquette):
    etiquette = '%;' + etiquette + ";%"
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    rows = db.execute('SELECT * FROM doc WHERE etiquette LIKE ?;', [etiquette]).fetchall()
    obj = json.dumps([dict(ix) for ix in rows])
    print(os.getcwd() + "\\static\\document")
    return obj


@app.route('/document/<doc>')
def publish(doc):
    return send_from_directory("./static/document/", doc)


def update_doc(code, libelle, lien, etiquette, creation, maj):
    try:
        sql = ''' UPDATE doc
                  SET libelle = ?,
                      lien = ?,
                      etiquette = ?,
                      creation = DATE(?),
                      maj = DATE(?)
                  WHERE code = ?;'''
        column_values = (str(libelle), str(lien), str(etiquette), creation, maj, str(code))
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(sql, column_values)
        conn.commit()
        conn.cursor().fetchall()
    except sqlite3.Error as error:
        print("Erreur de maj des donnees", error)
    finally:
        if conn:
            conn.close()


def insert_doc(code, libelle, lien, etiquette, creation, maj):
    try:
        sql = '''INSERT INTO doc 
                (code,libelle,lien,etiquette, creation, maj) 
                VALUES (?,?,?,?,?,?);'''
        column_values = (str(code), str(libelle), str(lien), str(etiquette), creation, maj)
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(sql, column_values)
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Erreur impossible d'ajouter cette enregistrement", error)
    finally:
        if conn:
            conn.close()


def delete_doc(code):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM doc WHERE code = (?)", (str(code),))
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Erreur suppression impossible", error)
    finally:
        if conn:
            conn.close()


@app.route("/upload/", methods=["GET", "POST"])
def upload():
    etat = True
    if request.method == "POST":
        if request.files:
            document = request.files.get('file')
            document.save(os.path.join(app.config["UPLOAD_FOLDER"], document.filename))
    return render_template("upload.html", etat=etat)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_page(e):
    return render_template('500.html'), 500


if __name__ == '__user__':
    app.run(debug=True)
