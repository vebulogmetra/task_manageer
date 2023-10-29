import os
from pathlib import Path

import pexpect
import pytest

from src.core.settings.config import SETTINGS_DIR, settings
from src.core.utils.database import test_db_helper

# # Устанавливаем os.environ, чтобы использовать тестовую БД
# os.environ["TESTING"] = "True"


SQL_SCRIPTS_DIR: str = Path(SETTINGS_DIR).parent
SQL_SCRIPTS_DIR = os.path.join(SQL_SCRIPTS_DIR, "tests/db/scripts")


@pytest.fixture(scope="module")
def temp_db():
    create_database_script()
    print(">>>>>>>>>>Test database created")
    # create_tables_script()
    # print(">>>>>>>>>>All tables in database created")
    # insert_values_script()
    # print(">>>>>>>>>>All data inserted in database")

    yield database

    drop_database_script()
    print(">>>>>>>>>>Test database deleted")


def _run_psql_script(command: str, password: str, prompt: str, encoding: str = "UTF-8"):
    try:
        with pexpect.spawn(command, encoding=encoding) as psql:
            psql.expect("Password:")
            psql.sendline(password)
            psql.expect(prompt)
    except Exception as e:
        print(f"Error: {e}")


def create_database_script():
    sql_script_filepath = os.path.join(SQL_SCRIPTS_DIR, "create_test_database.sql")
    command = f"psql -h {settings.test_db_host} -U {settings.test_db_user} -d {settings.db_name} -f {sql_script_filepath} -W"
    _run_psql_script(
        command=command,
        password=f"{settings.test_db_password}",
        prompt="CREATE DATABASE",
    )


def drop_database_script():
    sql_script_filepath = os.path.join(SQL_SCRIPTS_DIR, "drop_test_database.sql")
    command = f"psql -h {settings.test_db_host} -U {settings.test_db_user} -d {settings.db_name} -f {sql_script_filepath} -W"
    _run_psql_script(
        command=command, password=f"{settings.test_db_password}", prompt="DROP DATABASE"
    )
