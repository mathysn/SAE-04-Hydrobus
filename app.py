from flask import Flask, request, render_template, redirect, flash, session, g
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",
            user="mnourry3",
            password="2909",
            database="BDD_mnourry3",
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

### BUS ###
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

@app.route('/bus/add', methods=['GET'])
def add_bus():
    bdd = get_db().cursor()
    sql = """SELECT r.id_reservoir
             FROM reservoir r"""
    bdd.execute(sql)
    reservoir = bdd.fetchall()
    return render_template('bus/add_bus.html', reservoir=reservoir)

@app.route('/bus/add', methods=['POST'])
def valid_add_bus():
    dateAchat = request.form.get('date-achat', '')
    consommation = request.form.get('conso', '')
    idReservoir = request.form.get('reservoir_id', '')

    bdd = get_db().cursor()
    sql = """INSERT INTO bus (
              date_achat,
              conso_annuelle, 
              id_reservoir)
              VALUES (%s, %s, %s)"""
    bdd.execute(sql,(dateAchat, consommation, idReservoir))
    get_db().commit()
    message = u'Bus ajouté, DateAchat: '+ dateAchat + ', Consommation: ' + consommation + 'L, IDReservoir: ' + idReservoir
    flash(message, 'alert-success')
    return redirect('/bus/show')

@app.route('/bus/delete', methods=['GET'])
def delete_bus():
    id_bus = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = "DELETE FROM bus WHERE id_bus = %s"
    bdd.execute(sql, id_bus)
    get_db().commit()
    message = u'Bus supprimé, ID: ' + id_bus
    flash(message, 'alert-danger')
    return redirect('/bus/show')


### RESERVOIR ###
@app.route('/reservoir/show')
def show_reservoir():
    bdd = get_db().cursor()
    sql = """SELECT r.*, m.libelle_modele
             FROM reservoir r
             LEFT JOIN modele m ON r.code_modele = m.code_modele
             ORDER BY r.id_reservoir"""
    bdd.execute(sql)
    reservoir = bdd.fetchall()
    return render_template('reservoir/show_reservoir.html', reservoir=reservoir)

@app.route('/reservoir/add', methods=['GET'])
def add_reservoir():
    bdd = get_db().cursor()
    sql = """SELECT m.*
             FROM modele m"""
    bdd.execute(sql)
    modele = bdd.fetchall()
    return render_template('reservoir/add_reservoir.html', modele=modele)

@app.route('/reservoir/add', methods=['POST'])
def valid_add_reservoir():
    volume = request.form.get('volume', '')
    modele = request.form.get('modele', '')

    bdd = get_db().cursor()
    sql = """INSERT INTO reservoir (
              volume_reservoir,
              code_modele)
              VALUES (%s, %s)"""
    bdd.execute(sql,(volume, modele))
    get_db().commit()
    message = u'Réservoir ajouté, Volume: '+ volume + ' L, Modèle: ' + modele
    flash(message, 'alert-success')
    return redirect('/reservoir/show')

@app.route('/reservoir/delete', methods=['GET'])
def delete_reservoir():
    id_reservoir = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = "DELETE FROM reservoir WHERE id_reservoir = %s"
    bdd.execute(sql, id_reservoir)
    get_db().commit()
    message = u'Réservoir supprimé, ID: ' + id_reservoir
    flash(message, 'alert-danger')
    return redirect('/reservoir/show')


### MODELE ### add/delete à finir
@app.route('/modele/show')
def show_modele():
    bdd = get_db().cursor()
    sql = """SELECT m.*
             FROM modele m"""
    bdd.execute(sql)
    modele = bdd.fetchall()
    return render_template('modele/show_modele.html', modele=modele)

@app.route('/modele/add', methods=['GET'])
def add_modele():
    bdd = get_db().cursor()
    sql = """SELECT t.*
              FROM type_incident t"""
    bdd.execute(sql)
    type_incident = bdd.fetchall()
    return render_template('incident/add_incident.html', type_incident=type_incident)

@app.route('/modele/add', methods=['POST'])
def valid_add_modele():
    dateIncident = request.form.get('date-incident', '')
    idBus = request.form.get('id-bus', '')
    incidentID = request.form.get('incident-id', '')

    bdd = get_db().cursor()
    sql = """INSERT INTO incident (
              date_incident,
              id_bus, 
              id_type_incident)
              VALUES (%s, %s, %s)"""
    bdd.execute(sql,(dateIncident, idBus, incidentID))
    get_db().commit()
    message = u'Incident ajouté, Date: '+ dateIncident + ', Bus: ' + idBus + 'L, Type d\'incident: ' + incidentID
    flash(message, 'alert-success')
    return redirect('/modele/show')

@app.route('/modele/delete', methods=['GET'])
def delete_modele():
    id_incident = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = "DELETE FROM incident WHERE id_incident = %s"
    bdd.execute(sql, id_incident)
    get_db().commit()
    message = u'Incident supprimé, ID: ' + id_incident
    flash(message, 'alert-danger')
    return redirect('/modele/show')


### REVISION ###
@app.route('/revision/show')
def show_revision():
    bdd = get_db().cursor()
    sql = """SELECT r.*
           FROM revision r"""
    bdd.execute(sql)
    revision = bdd.fetchall()
    return render_template('revision/show_revision.html', revision=revision)


### INCIDENT ###
@app.route('/incident/show')
def show_incidents():
    bdd = get_db().cursor()
    sql = """SELECT i.*, type.infos_type_incident
           FROM incident i
           LEFT JOIN type_incident type ON i.id_type_incident = type.id_type_incident
           GROUP BY i.id_incident"""
    bdd.execute(sql)
    incident = bdd.fetchall()
    return render_template('incident/show_incident.html', incident=incident)

@app.route('/incident/add', methods=['GET'])
def add_incident():
    bdd1 = get_db().cursor()
    bdd2 = get_db().cursor()
    sql1 = """SELECT t.*
              FROM type_incident t"""
    sql2 = """SELECT b.id_bus
              FROM bus b
              ORDER BY id_bus"""
    bdd1.execute(sql1)
    bdd2.execute(sql2)
    type_incident = bdd1.fetchall()
    bus = bdd2.fetchall()
    return render_template('incident/add_incident.html', type_incident=type_incident, bus=bus)

@app.route('/incident/add', methods=['POST'])
def valid_add_incident():
    dateIncident = request.form.get('date-incident', '')
    idBus = request.form.get('id-bus', '')
    incidentID = request.form.get('incident-id', '')

    bdd = get_db().cursor()
    sql = """INSERT INTO incident (
              date_incident,
              id_bus, 
              id_type_incident)
              VALUES (%s, %s, %s)"""
    bdd.execute(sql,(dateIncident, idBus, incidentID))
    get_db().commit()
    message = u'Incident ajouté, Date: '+ dateIncident + ', Bus: ' + idBus + 'L, Type d\'incident: ' + incidentID
    flash(message, 'alert-success')
    return redirect('/incident/show')

@app.route('/incident/delete', methods=['GET'])
def delete_incident():
    id_incident = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = "DELETE FROM incident WHERE id_incident = %s"
    bdd.execute(sql, id_incident)
    get_db().commit()
    message = u'Incident supprimé, ID: ' + id_incident
    flash(message, 'alert-danger')
    return redirect('/incident/show')


### TYPE INCIDENT ###
@app.route('/type_incident/show')
def show_type_incident():
    bdd = get_db().cursor()
    sql = """SELECT t.*
             FROM type_incident t"""
    bdd.execute(sql)
    type_incident = bdd.fetchall()
    return render_template('type_incident/show_type_incident.html', type_incident=type_incident)

@app.route('/type_incident/add', methods=['GET'])
def add_type_incident():
    return render_template('type_incident/add_type_incident.html')

@app.route('/type_incident/add', methods=['POST'])
def valid_add_type_incident():
    libelleType = request.form.get('libelle-type', '')

    bdd = get_db().cursor()
    sql = """INSERT INTO type_incident (
              infos_type_incident)
              VALUES (%s)"""
    bdd.execute(sql,(libelleType))
    get_db().commit()
    message = u'Incident ajouté, Libellé: '+ libelleType
    flash(message, 'alert-success')
    return redirect('/type_incident/show')

@app.route('/type_incident/delete', methods=['GET'])
def delete_type_incident():
    id_type_incident = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = "DELETE FROM type_incident WHERE id_type_incident = %s"
    bdd.execute(sql, id_type_incident)
    get_db().commit()
    message = u'Type d\'incident supprimé, ID: ' + id_type_incident
    flash(message, 'alert-danger')
    return redirect('/type_incident/show')


### KILOMETRAGE ###
@app.route('/kilometrage/show')
def show_kilometrage():
    bdd = get_db().cursor()
    sql = """SELECT k.*
           FROM kilometrage k"""
    bdd.execute(sql)
    kilometrage = bdd.fetchall()
    return render_template('kilometrage/show_kilometrage.html', kilometrage=kilometrage)

@app.route('/kilometrage/delete', methods=['GET'])
def delete_kilometrage():
    id_kilometrage = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = "DELETE FROM kilometrage WHERE id_kilometrage = %s"
    bdd.execute(sql, id_kilometrage)
    get_db().commit()
    message = u'Kilometrage supprimé, ID: ' + id_kilometrage
    flash(message, 'alert-danger')
    return redirect('/kilometrage/show')


    
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
