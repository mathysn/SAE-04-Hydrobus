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
    sql = """SELECT b.*, COUNT(c.id_bus) AS nb_changement
             FROM bus b
             LEFT JOIN changement_reservoir c ON b.id_bus = c.id_bus
             GROUP BY b.id_bus"""
    bdd.execute(sql)
    bus = bdd.fetchall()
    return render_template('bus/show_bus.html', bus=bus)

@app.route('/bus/etat', methods=['GET'])
def etat_bus():
    id_bus = request.args.get('id', '')
    bdd = get_db().cursor()
    bdd2 = get_db().cursor()
    bdd3 = get_db().cursor()

    sql = """SELECT b.*, COUNT(c.id_bus) AS nb_changement
             FROM bus b
             LEFT JOIN changement_reservoir c ON b.id_bus = c.id_bus
             WHERE b.id_bus = %s"""

    sql2 = """SELECT b.*, SUM(k.nombre_km) AS nb_km_total
              FROM bus b
              LEFT JOIN kilometrage k ON b.id_bus = k.id_bus
              where b.id_bus = %s"""

    sql3 = """SELECT b.*, MAX(k.nombre_km) AS nb_km_max
              FROM bus b
              LEFT JOIN kilometrage k ON b.id_bus = k.id_bus
              WHERE b.id_bus = %s"""

    bdd.execute(sql, [id_bus])
    bdd2.execute(sql2, [id_bus])
    bdd3.execute(sql3, [id_bus])
    bus = bdd.fetchone()
    bus2 = bdd2.fetchone()
    bus3 = bdd3.fetchone()
    return render_template('bus/etat_bus.html', bus=bus, bus2=bus2, bus3=bus3)

@app.route('/bus/etat_retour', methods=['POST'])
def retour_etat_bus():
    return redirect('/bus/show')

@app.route('/bus/add', methods=['GET'])
def add_bus():
    bdd = get_db().cursor()
    sql = """SELECT r.id_reservoir
             FROM reservoir r
             ORDER BY r.id_reservoir"""
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
    bdd.execute(sql, (dateAchat, consommation, idReservoir))
    get_db().commit()
    message = u'Bus ajouté, Date d\'achat: '+ dateAchat + ', Consommation: ' + consommation + ' L, Reservoir: ' + idReservoir
    flash(message, 'alert-success')
    return redirect('/bus/show')

@app.route('/bus/edit', methods=['GET'])
def edit_bus():
    id_bus = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = """SELECT b.*
             FROM bus b
             WHERE id_bus = %s"""
    bdd.execute(sql, [id_bus])
    bus = bdd.fetchone()
    bdd2 = get_db().cursor()
    sql2 = """SELECT r.*
              FROM reservoir r"""
    bdd2.execute(sql2)
    reservoir = bdd2.fetchall()
    return render_template('bus/edit_bus.html', bus=bus, reservoir=reservoir)

@app.route('/bus/edit', methods=['POST'])
def valid_edit_bus():
    bdd = get_db().cursor()
    id_bus = request.form.get('id', '')
    date_achat = request.form.get('date-achat', '')
    conso = request.form.get('conso', '')
    id_reservoir = request.form.get('id-reservoir', '')
    sql = """UPDATE bus 
             SET date_achat = %s,
             conso_annuelle = %s,
             id_reservoir = %s
             WHERE id_bus = %s"""
    bdd.execute(sql, [date_achat, conso, id_reservoir, id_bus])
    get_db().commit()
    message = u'Bus modifié, ID: ' + id_bus + ", Date d'achat: " + date_achat + ', Conso annuelle: ' + conso + ', ID Réservoir: ' + id_reservoir
    flash(message, 'alert-warning')
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

@app.route('/reservoir/etat', methods=['GET'])
def etat_reservoir():
    id_reservoir = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = """SELECT res.*, COUNT(revision.id_revision) AS nb_revision
             FROM reservoir res
             LEFT JOIN revision ON res.id_reservoir = revision.id_reservoir
             WHERE res.id_reservoir = %s"""
    bdd.execute(sql, [id_reservoir])
    reservoir = bdd.fetchone()
    return render_template('reservoir/etat_reservoir.html', reservoir=reservoir)

@app.route('/reservoir/etat_retour', methods=['POST'])
def retour_etat_reservoir():
    return redirect('/reservoir/show')

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

@app.route('/reservoir/edit', methods=['GET'])
def edit_reservoir():
    id_reservoir = request.args.get('id', '')
    bdd1 = get_db().cursor()
    sql1 = """SELECT modele.*
              FROM modele"""
    bdd1.execute(sql1)
    modele = bdd1.fetchall()

    bdd2 = get_db().cursor()
    sql2 = """SELECT r.*, modele.*
              FROM reservoir r
              LEFT JOIN modele ON r.code_modele = modele.code_modele
              WHERE id_reservoir = %s"""
    bdd2.execute(sql2, [id_reservoir])
    reservoir = bdd2.fetchone()
    return render_template('reservoir/edit_reservoir.html', modele=modele, reservoir=reservoir)

@app.route('/reservoir/edit', methods=['POST'])
def valid_edit_reservoir():
    bdd = get_db().cursor()
    id_reservoir = request.form.get('id', '')
    volumeReservoir = request.form.get('volume', '')
    codeModele = request.form.get('code-modele', '')
    idTypeIncident = request.form.get('id-type-incident', '')
    sql = """UPDATE reservoir 
             SET volume_reservoir = %s,
             code_modele = %s
             WHERE id_reservoir = %s"""
    bdd.execute(sql, [volumeReservoir, codeModele, id_reservoir])
    get_db().commit()
    message = u'Réservoir modifié, ID: ' + id_reservoir + ", Volume: " + volumeReservoir + ' L, Modèle: ' + codeModele
    flash(message, 'alert-warning')
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


### MODELE ###
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
    return render_template('modele/add_modele.html')

@app.route('/modele/add', methods=['POST'])
def valid_add_modele():
    libelleModele = request.form.get('libelle-modele', '')
    infosModele = request.form.get('infos-modele', '')

    bdd = get_db().cursor()
    sql = """INSERT INTO modele (
              libelle_modele,
              infos_modele)
              VALUES (%s, %s)"""
    bdd.execute(sql,(libelleModele, infosModele))
    get_db().commit()
    message = u'Modèle ajouté, Libellé: '+ libelleModele + ', Informations: ' + infosModele
    flash(message, 'alert-success')
    return redirect('/modele/show')

@app.route('/modele/edit', methods=['GET'])
def edit_modele():
    code_modele = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = """SELECT modele.*
             FROM modele
             WHERE code_modele = %s"""
    bdd.execute(sql, [code_modele])
    modele = bdd.fetchone()
    return render_template('modele/edit_modele.html', modele=modele)

@app.route('/modele/edit', methods=['POST'])
def valid_edit_modele():
    bdd = get_db().cursor()
    code_modele = request.form.get('id', '')
    libelleModele = request.form.get('libelle-modele', '')
    infosModele = request.form.get('infos-modele', '')
    sql = """UPDATE modele 
             SET libelle_modele = %s,
             infos_modele = %s
             WHERE code_modele = %s"""
    bdd.execute(sql, [libelleModele, infosModele, code_modele])
    get_db().commit()
    message = u'Type d\'incident modifié, ID: ' + code_modele + ", Libellé: " + libelleModele + ", Informations: " + infosModele
    flash(message, 'alert-warning')
    return redirect('/modele/show')

@app.route('/modele/delete', methods=['GET'])
def delete_modele():
    code_modele = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = "DELETE FROM modele WHERE code_modele = %s"
    bdd.execute(sql, code_modele)
    get_db().commit()
    message = u'Modèle supprimé, ID: ' + code_modele
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

@app.route('/revision/add', methods=['GET'])
def add_revision():
    bdd = get_db().cursor()
    sql = """SELECT reservoir.*
              FROM reservoir"""
    bdd.execute(sql)
    reservoir = bdd.fetchall()
    return render_template('revision/add_revision.html', reservoir=reservoir)

@app.route('/revision/add', methods=['POST'])
def valid_add_revision():
    descriptif = request.form.get('descriptif', '')
    dateRevision = request.form.get('date-revision', '')
    idReservoir = request.form.get('id-reservoir', '')

    bdd = get_db().cursor()
    sql = """INSERT INTO revision (
              descriptif_revision,
              date_revision, 
              id_reservoir)
              VALUES (%s, %s, %s)"""
    bdd.execute(sql, (descriptif, dateRevision, idReservoir))
    get_db().commit()
    message = u'Révision ajoutée, Descriptif: ' + descriptif + 'Date: '+ dateRevision + ', Réservoir: ' + idReservoir
    flash(message, 'alert-success')
    return redirect('/revision/show')

@app.route('/revision/edit', methods=['GET'])
def edit_revision():
    id_revision = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = """SELECT revision.*
             FROM revision
             WHERE id_revision = %s"""
    bdd.execute(sql, [id_revision])
    revision = bdd.fetchone()
    bdd2 = get_db().cursor()
    sql2 = """SELECT reservoir.*
              FROM reservoir""" 
    bdd2.execute(sql2)
    reservoir = bdd2.fetchall()
    return render_template('revision/edit_revision.html', revision=revision, reservoir=reservoir)

@app.route('/revision/edit', methods=['POST'])
def valid_edit_revision():
    bdd = get_db().cursor()
    id_revision = request.form.get('id', '')
    descriptifRevision = request.form.get('descriptif-revision', '')
    dateRevision = request.form.get('date-revision', '')
    idReservoir = request.form.get('id-reservoir', '')
    sql = """UPDATE revision 
             SET descriptif_revision = %s,
             date_revision = %s,
             id_reservoir = %s
             WHERE id_revision = %s"""
    bdd.execute(sql, [descriptifRevision, dateRevision, idReservoir, id_revision])
    get_db().commit()
    message = u'Révision modifiée, ID: ' + id_revision + ", Descriptif: " + descriptifRevision + ', Date: ' + dateRevision + ', ID Réservoir: ' + idReservoir
    flash(message, 'alert-warning')
    return redirect('/revision/show')

@app.route('/revision/delete', methods=['GET'])
def delete_revision():
    id_revision = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = "DELETE FROM revision WHERE id_revision = %s"
    bdd.execute(sql, id_revision)
    get_db().commit()
    message = u'Révision supprimée, ID: ' + id_revision
    flash(message, 'alert-danger')
    return redirect('/revision/show')


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
    message = u'Incident ajouté, Date: '+ dateIncident + ', Bus: ' + idBus + ', Type d\'incident: ' + incidentID
    flash(message, 'alert-success')
    return redirect('/incident/show')

@app.route('/incident/edit', methods=['GET'])
def edit_incident():
    id_incident = request.args.get('id', '')
    bdd1 = get_db().cursor()
    bdd2 = get_db().cursor()
    bdd3 = get_db().cursor()

    sql1 = """SELECT t.*
              FROM type_incident t"""

    sql2 = """SELECT i.*, type_incident.*
             FROM incident i
             LEFT JOIN type_incident ON i.id_type_incident = type_incident.id_type_incident
             WHERE id_incident = %s"""

    sql3 = """SELECT bus.*
              FROM bus"""

    bdd1.execute(sql1)
    bdd2.execute(sql2, [id_incident])
    bdd3.execute(sql3)

    type_incident = bdd1.fetchall()
    incident = bdd2.fetchone()
    bus = bdd3.fetchall()
    return render_template('incident/edit_incident.html', type_incident=type_incident, incident=incident, bus=bus)

@app.route('/incident/edit', methods=['POST'])
def valid_edit_incident():
    bdd = get_db().cursor()
    id_incident = request.form.get('id', '')
    dateIncident = request.form.get('date-incident', '')
    idBus = request.form.get('id-bus', '')
    idTypeIncident = request.form.get('id-type-incident', '')
    sql = """UPDATE incident 
             SET date_incident = %s,
             id_bus = %s,
             id_type_incident = %s
             WHERE id_incident = %s"""
    bdd.execute(sql, [dateIncident, idBus, idTypeIncident, id_incident])
    get_db().commit()
    message = u'Incident modifié, ID: ' + id_incident + ", Date de l'incident: " + dateIncident + ', Bus: ' + idBus + ', Type d\'incident: ' + idTypeIncident
    flash(message, 'alert-warning')
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

@app.route('/type_incident/edit', methods=['GET'])
def edit_type_incident():
    id_type_incident = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = """SELECT type_incident.*
             FROM type_incident
             WHERE id_type_incident = %s"""
    bdd.execute(sql, [id_type_incident])
    type_incident = bdd.fetchone()
    return render_template('type_incident/edit_type_incident.html', type_incident=type_incident)

@app.route('/type_incident/edit', methods=['POST'])
def valid_edit_type_incident():
    bdd = get_db().cursor()
    id_type_incident = request.form.get('id', '')
    libelleType = request.form.get('libelle-type', '')
    sql = """UPDATE type_incident 
             SET infos_type_incident = %s
             WHERE id_type_incident = %s"""
    bdd.execute(sql, [libelleType, id_type_incident])
    get_db().commit()
    message = u'Type d\'incident modifié, ID: ' + id_type_incident + ", Libellé: " + libelleType
    flash(message, 'alert-warning')
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

@app.route('/kilometrage/add', methods=['GET'])
def add_kilometrage():
    bdd = get_db().cursor()
    sql = """SELECT bus.*
             FROM bus
             ORDER BY id_bus"""
    bdd.execute(sql)
    bus = bdd.fetchall()
    return render_template('kilometrage/add_kilometrage.html', bus=bus)

@app.route('/kilometrage/add', methods=['POST'])
def valid_add_kilometrage():
    dateKilo = request.form.get('date-kilo', '')
    distance = request.form.get('distance', '')
    idBus = request.form.get('id-bus', '')

    bdd = get_db().cursor()
    sql = """INSERT INTO kilometrage (
              date_periode,
              nombre_km, 
              id_bus)
              VALUES (%s, %s, %s)"""
    bdd.execute(sql, (dateKilo, distance, idBus))
    get_db().commit()
    message = u'Kilométrage ajouté, Date de la période: '+ dateKilo + ', Nombre de km: ' + distance + ' km, Bus: ' + idBus
    flash(message, 'alert-success')
    return redirect('/kilometrage/show')

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