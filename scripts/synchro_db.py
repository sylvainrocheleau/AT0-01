import os
import sys
import subprocess
import traceback

import  pandas as pd
from datetime import datetime
import mysql.connector
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


TABLES = [
    {'name':'V2_Bookies', 'key': ['bookie_id']},
    {'name':'V2_Competitions', 'key': ['competition_id']},
    {'name':'V2_Competitions_Urls', 'key': ['competition_url_id']},
    {'name': 'V2_Cookies', 'key': ['user_agent_hash']},
    {'name': 'V2_Exchanges', 'key': ['bet_id', 'lay_odds']},
    {'name': 'V2_Matches', 'key': ['match_id']},
    {'name': 'V2_Matches_Odds', 'key': ['bet_id', 'bookie_id']},
    {'name':'V2_Matches_Urls', 'key': ['match_url_id']},
    {'name': 'V2_Matches_Urls_No_Ids', 'key': 'match_url_id'},
    {'name': 'V2_Dutcher', 'key': ['bet_id', 'bookie_id', 'bookie_2']},
    {'name': 'V2_Oddsmatcher', 'key': ['bet_id', 'lay_odds', 'bookie_id']},
    {'name': 'V2_Sports', 'key': ['sport_id']},
    {'name':'V2_Teams', 'key': ['team_id']},
]

SQL_PORT = 3306
SQL_DATABASE = "ATO_production"

local_conn_params = {
    'user': "admin_02",
    'password': "43&trdGhqLlMXX",
    'host': "127.0.0.1",
    'port': SQL_PORT,
    'database': SQL_DATABASE,
}

remote_conn_params = {
    'user': "ato_read",
    'password': "43&thFg5#M",
    'host': "164.92.191.102",
    'port': SQL_PORT,
    'database': SQL_DATABASE,
}

try:
    local_conn = mysql.connector.connect(**local_conn_params)
    remote_conn = mysql.connector.connect(**remote_conn_params)
except Exception as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Back up the database
def dump_database(conn_params, output_dir="../archives/db_backups"):
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"{conn_params['database']}_backup_{timestamp}.sql"
    filepath = os.path.join(output_dir, filename)

    os.makedirs(output_dir, exist_ok=True)

    cmd = [
        "mysqldump",
        f"--user={conn_params['user']}",
        f"--password={conn_params['password']}",
        f"--host={conn_params['host']}",
        f"--port={str(conn_params['port'])}",
        "--routines",
        "--events",
        "--single-transaction",
        conn_params["database"]
    ]

    try:
        with open(filepath, "w") as f:
            subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, check=True)
        print(f"Backup successful: {filepath}")
    except subprocess.CalledProcessError as e:
        print(f"Backup failed: {e.stderr.decode()}")

# Drop all localhost database's tables
def drop_local_tables():
    cursor = local_conn.cursor()
    tables_with_v2_logs = TABLES + [{'name': 'V2_Logs', 'key': 'log_id'}]
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        for table in tables_with_v2_logs:
            table_name = table['name']
            cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`;")
            print(f"{table_name} dropped")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        local_conn.commit()
    except Exception as e:
        print(f"Failed to drop tables: {e}")
    finally:
        cursor.close()

# Copy table structures from remote db to localhost db
def clone_table_structures():
    remote_cursor = remote_conn.cursor()
    local_cursor = local_conn.cursor()
    tables_with_v2_logs = TABLES + [{'name': 'V2_Logs', 'key': 'log_id'}]

    for table in tables_with_v2_logs:
        table_name = table['name']
        try:
            remote_cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
            result = remote_cursor.fetchone()
            create_statement = result[1]

            local_cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")

            local_cursor.execute(create_statement)
            print(f"Structure of `{table_name}` cloned successfully.")
        except Exception as e:
            print(f"Failed to clone structure of `{table_name}`: {e}")

    local_conn.commit()
    remote_cursor.close()
    local_cursor.close()

# Synchronize datas of one table from remote db to localhost db
def sync_table(table_info):
    table = table_info['name']
    id_col = table_info['key']
    id_cols = id_col if isinstance(id_col, list) else [id_col]
    query = f"SELECT * FROM {table}"

    try:
        # Ensure the connection is alive before using it
        remote_conn.ping(reconnect=True, attempts=3, delay=5)
        df = pd.read_sql(query, remote_conn)
    except Exception as e:
        print(traceback.format_exc())
        print(f"[{table}] Failed to fetch from remote: {e}")
        return

    if df.empty:
        print(f"[{table}] No rows to sync.")
        return

    print(f"[{table}] Fetched {len(df)} rows to sync.")

    cursor = local_conn.cursor()
    for index, row in df.iterrows():
        row_dict = row.to_dict()

        columns = list(row_dict.keys())
        values = [None if pd.isna(row_dict[col]) else row_dict[col] for col in columns]

        col_list = ", ".join(f"`{col}`" for col in columns)
        placeholders = ", ".join(["%s"] * len(columns))
        updates = ", ".join(
            f"`{col}` = VALUES(`{col}`)"
            for col in columns
            if col not in (id_col if isinstance(id_col, list) else [id_col])
        )

        update_sql = f"""
            INSERT INTO `{table}` ({col_list})
            VALUES ({placeholders})
            ON DUPLICATE KEY UPDATE {updates}
        """

        try:
            cursor.execute(update_sql, values)
        except Exception as e:
            key_values = ", ".join(str(row_dict.get(k)) for k in id_cols)
            print(f"[{table}] Error syncing row [{key_values}]: {e}")

    local_conn.commit()
    print(f"[{table}] Synchro completed.")

# Synchronize all tables from remote db to localhost db
def sync_all_tables():
    for table in TABLES:
        sync_table(table)

if __name__ == "__main__":
    dump_database(remote_conn_params)
    drop_local_tables()
    clone_table_structures()
    sync_all_tables()
