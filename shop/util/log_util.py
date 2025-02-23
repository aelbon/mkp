from django.db import connection
import logging

logger = logging.getLogger('shop')

def log_session_info(location: str):
   with connection.cursor() as cursor:
        # Log session info
        cursor.execute("SELECT pg_backend_pid(), current_setting('shop.current_user_id', TRUE)")
        pid, user_id = cursor.fetchone()

        # Log more session details
        cursor.execute("""
            SELECT pid, usename, application_name, client_addr, backend_start, state
            FROM pg_stat_activity 
            WHERE pid = pg_backend_pid()
        """)
        session_info = cursor.fetchone()
        logger.info(f"{location}: Postgres PID: {pid}, CurUsr: {user_id} Session details: {session_info}")
