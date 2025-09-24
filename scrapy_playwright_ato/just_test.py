#!/usr/bin/env python3
import sys
import os
import shutil
import subprocess
import time
import socket
from contextlib import closing
import mysql.connector
from mysql.connector import Error

# SSH details (to Server 1)
SSH_HOST = "95.179.223.212"
SSH_PORT = 22
SSH_USERNAME = "info@sylvainrocheleau.com"  # note: contains '@', so we use -l with ssh
# Optional: provide SSH password via environment variable to enable non-interactive auth with sshpass
SSH_PASSWORD = os.getenv("SSH_PASSWORD", "")

# MariaDB on Server 1 (reachable from that server)
REMOTE_DB_HOST = "127.0.0.1"
REMOTE_DB_PORT = 3306

# Local port for the tunnel on this machine
LOCAL_PORT = 13306  # change if occupied

# MariaDB credentials
DB_USER = "pnmjdhmkxp"
DB_PASSWORD = "8qTFBGEJZJ"
DB_NAME = "pnmjdhmkxp"

def wait_for_port(host: str, port: int, timeout: float = 5.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            try:
                s.connect((host, port))
                return True
            except OSError:
                time.sleep(0.1)
    return False

def start_ssh_tunnel() -> None:
    # Base ssh command
    ssh_args = [
        "ssh",
        "-f",                 # background after authentication
        "-N",                 # do not execute remote command
        "-p", str(SSH_PORT),
        "-l", SSH_USERNAME,   # login name with '@'
        "-o", "ExitOnForwardFailure=yes",
        # Avoid interactive host key prompts in automation/CI
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        # Limit repeated password prompts
        "-o", "NumberOfPasswordPrompts=1",
        # Try these auth methods in order
        "-o", "PreferredAuthentications=publickey,password,keyboard-interactive",
        "-L", f"{LOCAL_PORT}:{REMOTE_DB_HOST}:{REMOTE_DB_PORT}",
        SSH_HOST,
    ]

    cmd: list[str]
    if SSH_PASSWORD:
        # If password provided and sshpass is available, use it to avoid ssh_askpass/TTY issues
        sshpass_path = shutil.which("sshpass")
        if not sshpass_path:
            raise subprocess.CalledProcessError(returncode=255, cmd="sshpass",
                                               output=b"",
                                               stderr=b"sshpass not installed. Install it or set up SSH keys, or unset SSH_PASSWORD.")
        cmd = [sshpass_path, "-p", SSH_PASSWORD] + ssh_args
    else:
        # Rely on SSH agent or key-based auth; without this, -f will fail in headless shells
        cmd = ssh_args

    # This may prompt for the SSH password if SSH_PASSWORD not set but keys/agent are configured
    subprocess.check_call(cmd)


def stop_ssh_tunnel() -> None:
    # Best-effort cleanup of the background ssh process we started
    try:
        subprocess.call([
            "pkill", "-f",
            f"ssh -f -N -p {SSH_PORT} -l {SSH_USERNAME} -L {LOCAL_PORT}:{REMOTE_DB_HOST}:{REMOTE_DB_PORT} {SSH_HOST}"
        ])
    except Exception:
        pass


def fetch_first_ten_v1_dutcher(conn):
    """
    Retrieve the first 10 records from table V1_Dutcher as a list of dicts.
    """
    with closing(conn.cursor(dictionary=True)) as cur:
        cur.execute("SELECT * FROM V1_Dutcher LIMIT 10;")
        return cur.fetchall()


def main():
    # If a tunnel is already listening on LOCAL_PORT, reuse it and do not start a new one
    tunnel_already_running = wait_for_port("127.0.0.1", LOCAL_PORT, timeout=0.5)
    started_by_script = False

    if not tunnel_already_running:
        # Start system SSH tunnel
        try:
            start_ssh_tunnel()
            started_by_script = True
        except subprocess.CalledProcessError as e:
            # Provide actionable guidance
            msg = (
                "Failed to start SSH tunnel. "
                "If you need password auth, export SSH_PASSWORD and install sshpass (sudo apt-get install -y sshpass). "
                "Otherwise set up SSH keys or ensure an agent is available. Original error: %s" % e
            )
            print(msg, file=sys.stderr)
            sys.exit(1)

        if not wait_for_port("127.0.0.1", LOCAL_PORT, timeout=5.0):
            print("Local tunnel port did not become ready in time.", file=sys.stderr)
            if started_by_script:
                stop_ssh_tunnel()
            sys.exit(2)

    print(f"SSH tunnel up: 127.0.0.1:{LOCAL_PORT} -> {REMOTE_DB_HOST}:{REMOTE_DB_PORT} via {SSH_HOST}:{SSH_PORT}")

    try:
        with closing(mysql.connector.connect(
            host="127.0.0.1",
            port=LOCAL_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset="utf8mb4",
            connection_timeout=5,
        )) as conn:
            with closing(conn.cursor(dictionary=True)) as cur:
                cur.execute("SELECT VERSION() AS version, CURRENT_USER() AS `current_user`;")
                row = cur.fetchone()
                print(row)

            # Fetch and display first 10 rows from V1_Dutcher
            try:
                rows = fetch_first_ten_v1_dutcher(conn)
                print(f"V1_Dutcher first 10 rows (count={len(rows)}):")
                for r in rows:
                    print(r)
            except Error as e:
                # Surface a clear message if the table doesn't exist or permission denied
                print(f"Failed to fetch from V1_Dutcher: {e}", file=sys.stderr)
    except Error as e:
        print(f"Database error: {e}", file=sys.stderr)
        sys.exit(3)
    finally:
        if started_by_script:
            stop_ssh_tunnel()

if __name__ == "__main__":
    main()
