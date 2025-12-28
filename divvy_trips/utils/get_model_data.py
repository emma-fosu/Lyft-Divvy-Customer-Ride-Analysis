import subprocess
import os
import pandas as pd
from pathlib import Path
from databricks import sql as dbSql
from .get_model_name import get_model_name

async def get_model_data(file: str, directory: str = "analyses", options: dict[str, any] = {}):
    model_name = get_model_name(file, directory)

    if options.get("shouldCompile"):
        subprocess.run(["dbt", "compile", "--select", model_name])

    current_file = Path(file).resolve()

    project_root = current_file.parents[1]

    compiled_sql_path = project_root / "target" / "compiled" / "divvy_trips" / "analyses" / f"{model_name}.sql"

    connection = dbSql.connect(
        server_hostname=os.getenv("DB_SERVER_HOSTNAME"),
        http_path=os.getenv("DB_HTTP_PATH"),
        access_token=os.getenv("DB_ACCESS_TOKEN")
    )

    sql = ""

    with open(compiled_sql_path) as f:
        sql = f.read()

    df = pd.read_sql(sql, connection)

    return df
