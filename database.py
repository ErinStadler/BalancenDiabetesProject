import os

import server
import model

os.system("dropdb users")
os.system("createdb users")
os.system("psql < database.sql")

model.connect_to_db(server.app)
model.db.create_all()