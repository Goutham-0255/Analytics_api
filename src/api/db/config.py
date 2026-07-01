from decouple import config as decouple_config

# This looks for a DATABASE_URL in your environment or .env file
DATABASE_URL = decouple_config("DATABASE_URL", default="")

if DATABASE_URL == "":
    # Prevents the app from starting up if the DB configuration is completely missing
    raise NotImplementedError("DATABASE_URL environment variable must be set.")
