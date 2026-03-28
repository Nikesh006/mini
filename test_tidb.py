import mysql.connector

try:
    print("Connecting to TiDB...")
    conn = mysql.connector.connect(
        host="gateway01.eu-central-1.prod.aws.tidbcloud.com",
        port=4000,
        user="TE6nZ5S1Wksbas9.root",
        password="LXPL0yuuONE2JiUP",
        ssl_verify_cert=True,
        ssl_verify_identity=True
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS gymcopy;")
    print("Successfully connected and created the gymcopy database on TiDB!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
    print("Trying without strict SSL verification...")
    try:
        conn = mysql.connector.connect(
            host="gateway01.eu-central-1.prod.aws.tidbcloud.com",
            port=4000,
            user="TE6nZ5S1Wksbas9.root",
            password="LXPL0yuuONE2JiUP"
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS gymcopy;")
        print("Successfully connected and created gymcopy (without strict SSL)!")
        conn.close()
    except Exception as e2:
        print(f"Failed again: {e2}")
