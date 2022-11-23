from flask import Flask, request, render_template, redirect, flash, session, g
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",                 # à modifier
            user="mnourry3",                     # à modifier
            password="2909",                # à modifier
            database="BDD_mnourry3",        # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_accueil():
    return render_template('layout.html')


@app.route('/bus/show')
def show_bus():
    bdd = get_db().cursor()
    sql = "SELECT b.id_bus, b.date_achat, b.conso_annuelle, b.id_reservoir, COUNT(c.id_bus) AS nb_changement\
           FROM bus b\
           LEFT JOIN changement_reservoir c ON b.id_bus = c.id_bus\
           GROUP BY b.id_bus"
    bdd.execute(sql)
    bus = bdd.fetchall()
    return render_template('bus/show_bus.html', bus=bus)


# @app.route('/tableaux/card')
# def show_cards():
#     bdd = get_db().cursor()
#     sql = "SELECT id_tableau AS id, \
#               nom_tableau AS nom, \
#               prix_assurance AS prixAssurance, \
#               date_realisation AS dateRealisation, \
#               peintre, \
#               localisation_musee AS localisationMusee, \
#               photo, \
#               mouvement, \
#               type_epoque_id AS typeEpoque_id \
#               FROM tableau \
#               ORDER BY id_tableau"

#     bdd.execute(sql)
#     tableau = bdd.fetchall()
#     return render_template('tableaux/card_tableaux.html', tableaux=tableau)


# @app.route('/tableaux/add', methods=['GET'])
# def add_tableau():
#     bdd = get_db().cursor()
#     sql = "SELECT id_type_epoque, libelle FROM type_epoque ORDER BY id_type_epoque"
#     bdd.execute(sql)
#     type_epoque = bdd.fetchall()
#     return render_template('tableaux/add_tableau.html', typeEpoque=type_epoque)


# @app.route('/tableaux/add', methods=['POST'])
# def valid_add_tableau():
#     nom = request.form.get('nom', '')
#     prixAssurance = request.form.get('prixAssurance', '')
#     dateRealisation = request.form.get('dateRealisation', '')
#     peintre = request.form.get('peintre', '')
#     localisationMusee = request.form.get('localisationMusee', '')
#     photo = request.form.get('photo', '')
#     mouvement = request.form.get('mouvement', '')
#     typeEpoque_id = request.form.get('typeEpoque_id', '')

#     bdd = get_db().cursor()
#     sql = "INSERT INTO tableau( \
#               nom_tableau, \
#               prix_assurance, \
#               date_realisation, \
#               peintre, \
#               localisation_musee, \
#               photo, \
#               mouvement, \
#               type_epoque_id) \
#               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#     bdd.execute(sql, [nom, prixAssurance, dateRealisation, peintre, localisationMusee, photo, mouvement, typeEpoque_id])
#     get_db().commit()

#     message = u'Article ajouté, Nom: '+nom + ', Prix assurance: ' + prixAssurance + '€, Date réalisation: ' + dateRealisation + ', Peintre: '+ peintre + ', Musée: ' + localisationMusee + ', Photo: ' + photo + ', Mouvement: ' + mouvement + ', Type Epoque ID: ' + typeEpoque_id
#     flash(message, 'alert-success')
#     return redirect('/tableaux/show')


# @app.route('/tableaux/delete', methods=['GET'])
# def delete_tableau():
#     id_tableau = request.args.get('id', '')
#     bdd = get_db().cursor()
#     sql = "DELETE FROM tableau WHERE id_tableau = %s"
#     bdd.execute(sql)
#     get_db().commit()
#     message = u'Un tableau supprimé, Nom: ' + id_tableau
#     flash(message, 'alert-danger')
#     return redirect('/tableaux/show')


# @app.route('/tableaux/edit', methods=['GET'])
# def edit_tableau():
#     id = request.args.get('id', '')
#     id = int(id)
#     tableaux = tableauTab[id-1]
#     return render_template('tableaux/edit_tableau.html', tableau=tableaux, typeEpoque=typeEpoque)


# @app.route('/tableaux/edit', methods=['POST'])
# def valid_edit_tableau():
#     nom = request.form['nom']
#     prixAssurance = request.form.get('prixAssurance', '')
#     dateRealisation = request.form.get('dateRealisation', '')
#     peintre = request.form.get('peintre', '')
#     localisationMusee = request.form.get('localisationMusee', '')
#     mouvement = request.form.get('mouvement', '')
#     typeEpoque_id = request.form.get('typeEpoque_id', '')
#     message = u'Tableau modifié, Nom: ' + nom + ", Prix de l'assurance: " + prixAssurance + '€, Date de réalisation: ' + dateRealisation + ', Peintre: ' + peintre + ', Musée: ' + localisationMusee + ', Mouvement: ' + mouvement + ', ID Epoque: ' + typeEpoque_id
#     flash(message, 'alert-warning')
#     return redirect('/tableaux/show')


# @app.route('/type_epoque/show')
# def show_type_epoque():
#     bdd = get_db().cursor()
#     sql = "SELECT id_type_epoque AS id, libelle FROM type_epoque ORDER BY id_type_epoque"
#     bdd.execute(sql)
#     type_epoque = bdd.fetchall()
#     return render_template('type_epoque/show_type_epoque.html', typeEpoque=type_epoque)


# @app.route('/type_epoque/add', methods=['GET'])
# def add_type_epoque():
#     return render_template('type_epoque/add_type_epoque.html')


# @app.route('/type_epoque/add', methods=['POST'])
# def valid_add_type_epoque():
#     libelle = request.form.get('libelle', '')
#     bdd = get_db().cursor()
#     sql = "INSERT INTO type_epoque(libelle) VALUES (%s)"
#     bdd.execute(sql, [libelle])
#     get_db().commit()
#     message = u'Type ajouté, Libellé: ' + libelle
#     flash(message, 'alert-success')
#     return redirect('/type_epoque/show')


# @app.route('/type_epoque/delete', methods=['GET'])
# def delete_type_article():
#     id = request.args.get('id', '')
#     message = u'Type d\'époque supprimé, Libellé: ' + id
#     flash(message, 'alert-danger')
#     return redirect('/type_epoque/show')


# @app.route('/type_epoque/edit', methods=['GET'])
# def edit_type_article():
#     id = request.args.get('id', '')
#     id = int(id)
#     type_epoque = typeEpoque[id-1]
#     return render_template('type_epoque/edit_type_epoque.html', type_epoque=type_epoque)


# @app.route('/type_epoque/edit', methods=['POST'])
# def valid_edit_type_article():
#     libelle = request.form['libelle']
#     id = request.form.get('id', '')
#     message=u"Type d'époque modifié, ID: " + id + ", Libellé: " + libelle
#     flash(message, 'alert-warning')
#     return redirect('/type_epoque/show')


# if __name__ == '__main__':
#     app.run()
