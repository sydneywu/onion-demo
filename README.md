### Installation
Install poetry on your machine. Then run "poetry install" on this folder.

### DB Migration

Create a model in models folder (as user.py)

1) Import new model in alembic/env.py

Use the following command to create a new migration file in alembic-migration/versions folder. 
This command needs to be run on root folder:

WINDOWS
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
alembic revision  --autogenerate --rev-id=$timestamp -m "add_user"

LINUX
alembic revision  --autogenerate --rev-id=$(date +%Y%m%d%H%M%S) -m "add_user"

(Note: the env should not have "asyncpg" in the connection string. "asyncpg" is for when the app runs)

Then use the following command to update the new migration file to db:
```alembic upgrade head```

If need to undo use the following command to revert the current migration file in db(check alembic_version table to see current migration file is updating in the db):
```alembic downgrade -1```

To delete migration file. manually delete it from alembic-migration/versions folder.

### To run
poetry shell
uvicorn main:app --reload

### Testing
set path on windows:
$env:PYTHONPATH="C:\Users\path\to\your\project\src"

set path on linux:
export PYTHONPATH=$PYTHONPATH:/path/to/your/project/src