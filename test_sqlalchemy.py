from sqlalchemy import create_engine

url = "mysql+mysqlconnector://TE6nZ5S1Wksbas9.root:LXPL0yuuONE2JiUP@gateway01.eu-central-1.prod.aws.tidbcloud.com:4000/gymcopy?ssl_ca=dummy.crt"
engine = create_engine(url)

try:
    conn = engine.connect()
    print("Connected successfully!")
except Exception as e:
    print(f"Error: {e}")
