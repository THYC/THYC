import sqlite3
from datetime import date


class Document:
    def __init__(self: object, code: str, libelle: str, lien: str, etiquette: str, date_creation: date, date_maj: date):
        # code : code document
        # libelle : libelle du document
        # lien : libelle du fichier
        # etiquette : mot clé séparé par des points virgules
        # date_creation : date de création du document
        # date_maj : date de mise à jour du document

        self.code = code
        self.libelle = libelle
        self.lien = lien
        self.etiquette = etiquette
        self.date_creation = date_creation
        self.date_maj = date_maj

    def __str__(self: object) -> str:
        return f"[{self.__code},{self.__libelle},{self.__lien},{self.__etiquette},{self.__date_creation},{self.__date_maj}]"

    # getters
    @property
    def code(self) -> str:
        return self.__code

    @property
    def libelle(self) -> str:
        return self.__libelle

    @property
    def lien(self) -> int:
        return self.__lien

    # setters
    @code.setter
    def code(self, code: str):
        if code is not None:
            self.__code = code.strip()

    @libelle.setter
    def libelle(self, libelle: str):
        self.__libelle = libelle.strip()

    @lien.setter
    def lien(self, lien: int):
        self.__lien = lien.strip()

    def update(self) -> bool:
        try:
            sql = ''' UPDATE doc
                      SET libelle = ?,
                          lien = ?,
                          etiquette = ?,
                          creation = DATE(?),
                          maj = DATE(?)
                      WHERE code = ?;'''
            column_values = (self.libelle, self.lien, self.etiquette, self.creation, self.maj, self.code)
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute(sql, column_values)
            conn.commit()
            conn.cursor().fetchall()
        except sqlite3.Error as error:
            print("Erreur de maj des donnees", error)
            return False
        finally:
            if conn:
                conn.close()
                return True
