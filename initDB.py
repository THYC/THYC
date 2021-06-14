import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO doc (code, libelle, lien, etiquette) VALUES (?, ?, ?, ?)",
            ('1909188', 'HARMONIE RECOUPABLE', '1909188_HARMONIE_RECOUPABLE.pdf', ';FDC;FDCREC;REC;PARVEAU;')
            )

cur.execute("INSERT INTO doc (code, libelle, lien, etiquette) VALUES (?, ?, ?, ?)",
            ('1910140', 'PORTE RECOUPABLE ALVEOLAIRE', '1910140 PORTE RECOUPABLE ALVEOLAIRE.pdf', ';FDC;FDCREC;REC;PARVEAU;')
            )

cur.execute("INSERT INTO doc (code, libelle, lien, etiquette) VALUES (?, ?, ?, ?)",
            ('1910141', 'PORTE RECOUPABLE PLEINE', '1910141 PORTE RECOUPABLE PLEINE.pdf', ';PTE;REC;DUBUS;DP006;OP19;SERRURE;')
            )

cur.execute("INSERT INTO doc (code, libelle, lien, etiquette) VALUES (?, ?, ?, ?)",
            ('1805280', 'BATTANT HETRE V2019', '1805280 BATTANT HETRE V2019.pdf', ';PTE;RD;DUBUS;DP006;OP19;SERRURE;')
            )

cur.execute("INSERT INTO doc (code, libelle, lien, etiquette) VALUES (?, ?, ?, ?)",
            ('1912100', 'PORTE TUBULAIRE ROMY', '1912100 PORTE TUBULAIRE ROMY.pdf', ';PTE;RD;DUBUS;DP006;OP19;SERRURE;')
            )

cur.execute("INSERT INTO user (idUser, nom, prenom, droit) VALUES (?, ?, ?, ?)",
            ('THYC', 'CLAVEAU', 'THIERRY', 1)
            )

connection.commit()
connection.close()
