import boto3
import json 
import mysql.connector
import tabulate 

secrets_manager = boto3.client(
    'secretsmanager',
    db_host = "DB_HOST"
    
    def get_secretvalue():
        secret_name = secrets_manager.get_secret_value(
            secret_dict = json.loads(secret_name['SecretString'])
            db_username = secret_dict['username']
            db_password = secret_dict['password']
            return db_username,db_password
           
           def execute_query(db_name,query):
                db_username,db_password = get_secretvalue()
                
                for db in db_name:
                    try:
                        connection = mysql.connector.connect(
                            host=db_host,
                            user=db_username,
                            password=db_password,
                            database=db
                        )
                    cursor=connection.cursor()
                    cursor.execute(query)
                    result = cursor.fetchall()
                    row_count = cursor.rowcount
                    
                    if query.upper().startswith("SELECT","SHOW","DESCRIBE")):
                        if result:
                            header =[column_name[0] for column_name in cursor.description]
                            table_output = [header] + list(result)
                            print(f"Running query on {db}: {query}")
                            print(tabulate(table_output,tablefmt="pipe"))
                            
                        else:
                            print("Empty result set")
                        else:
                            connection.commit()
                            print(f"{row_count} rows affected in {db}")
        except Except as :",e)
        
            print("Error:",e)
            finally:
            if 'connection' in locals():
            connection.close()
            
    db_names = input("Enter the database name:")
    split()
    query = input("Enter the query:")
    execute_query(db_names,query)
    
    for row in result:
        print(tabulate([row],tablefmt="pipe",headers=[column_name[0] for column_name in cursor.description]))
               result:
        print(tabulate([row],tablefmt="pipe",headers=[column_name[0] for column_name in cursor.description])) cursor.description]))
               result:
        print(tabulate([row],tablefmt="pipe",headers=[column_name[0] for column_name in cursor.description]))
               result:
        print(tabulate([row],tablefmt="pipe",headers=[column_name[0] for column_name in cursor.description]))