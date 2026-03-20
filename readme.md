# odoo

Template de base odoo

## Structure du projet

mon-projet-odoo/
├── docker-compose.yml
├── config/
│   └── odoo.conf
    addons/
    └── mon_blog/
        ├── __manifest__.py
        ├── __init__.py
        ├── models/
        │   ├── __init__.py
        │   └── blog_article.py
        ├── controllers/
        │   ├── __init__.py
        │   └── main.py
        ├── views/
        │   └── templates.xml
        ├── security/
        │   └── ir.model.access.csv
        └── static/
            └── src/
                └── css/
                    └── blog.css

## commandes utiles

### Démarrer les containers
docker compose up -d

### Voir les logs en direct
docker compose logs odoo -f

### Mettre à jour la liste des modules
docker compose exec odoo odoo -u base -d odoo17-db --stop-after-init

### Installer le module
docker compose exec odoo odoo -i mon_blog -d odoo17-db --stop-after-init

### Redémarrer odoo seul (après modif d'un module)
docker compose restart odoo

### Arrêter tout
docker compose down


## mise en place

docker compose up -d
docker compose exec odoo odoo -u base -d odoo17-db --stop-after-init
docker compose exec odoo odoo -i mon_blog -d odoo17-db --stop-after-init
docker compose restart odoo
http://localhost:8069/web?debug=1
maj de la liste + activer "mon blog"

## étapes pour l'installer sur vps ovh

Étape 1 — Exporter la base de données (depuis Docker local)
bash# Identifier le nom du conteneur PostgreSQL
docker ps

### Faire le dump
docker exec -t nom_conteneur_pg pg_dump -U odoo nom_bdd > dump.sql

Étape 2 — Exporter le filestore
bash# Le filestore est dans le volume Docker, souvent mappé ici :
zip -r filestore.zip ~/.local/share/Odoo/filestore/nom_bdd/

### ou selon ton docker-compose :
zip -r filestore.zip ./volumes/odoo-data/filestore/nom_bdd/

Étape 3 — Préparer le module
bashzip -r mon_module.zip ./addons/mon_module/

Étape 4 — Envoyer les fichiers sur le VPS
bash# Depuis ta machine locale :
scp dump.sql filestore.zip mon_module.zip user@IP_VPS:/home/user/odoo-migration/

Étape 5 — Sur le VPS : installer Odoo avec Docker
bashssh user@IP_VPS

mkdir odoo && cd odoo
### Crée un docker-compose.yml avec odoo + postgres
docker-compose up -d

Étape 6 — Importer la base de données
bash# Créer la base vide
docker exec -it nom_pg createdb -U odoo ma_bdd

### Importer le dump
docker exec -i nom_pg psql -U odoo ma_bdd < /home/user/odoo-migration/dump.sql

Étape 7 — Restaurer filestore et module
bash# Copier le filestore dans le volume
unzip filestore.zip -d /chemin/vers/volume/filestore/

### Copier le module dans le dossier addons
unzip mon_module.zip -d /chemin/vers/addons/

### Redémarrer et mettre à jour
docker-compose restart
docker exec -it nom_odoo odoo -u mon_module -d ma_bdd

Étape 8 — Nginx + SSL (optionnel mais recommandé)
bashapt install nginx certbot python3-certbot-nginx

### Config Nginx : proxy vers localhost:8069
certbot --nginx -d mondomaine.com