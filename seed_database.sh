rm db.sqlite3
rm -rf ./MiMos_Music_Mods_And_Repairs_Server/migrations

python3 manage.py migrate
python3 manage.py makemigrations music_repairsapi
python3 manage.py migrate music_repairsapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata customers
python3 manage.py loaddata specialties 
python3 manage.py loaddata employees
python3 manage.py loaddata instruments
python3 manage.py loaddata service_tickets