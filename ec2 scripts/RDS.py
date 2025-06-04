import boto3

def create_rds_instance(
    AllocatedStorage,
    DBInstanceClass,
    DBInstanceIdentifier,
    Engine,
    MasterUserPassword,
    MasterUsername,
):
    client = boto3.client("rds")
    response = client.create_db_instance(
        AllocatedStorage=AllocatedStorage,
        DBInstanceClass=DBInstanceClass,
        DBInstanceIdentifier=DBInstanceIdentifier,
        Engine=Engine,
        MasterUserPassword=MasterUserPassword,
        MasterUsername=MasterUsername,
    )
    return response

def modify_rds_instance_password(
    DBInstanceIdentifier,
    MasterUserPassword,
    Engine=Engine,
    MasterUserPassword=MasterUserPassword,
    MasterUsername=MasterUsername
)
return response

def modify_rds_instance_password(
    DBInstanceModifier,NewMasterUserPassword):
/*************  ✨ Windsurf Command ⭐  *************/
    """
    Modifies the master user password for the specified RDS instance.

    Parameters:
    DBInstanceModifier (str): The identifier of the RDS instance to modify.
    NewMasterUserPassword (str): The new master user password for the RDS instance.

    Returns:
    dict: Response from the RDS modify_db_instance API call.
    """

/*******  64d0d486-e576-4a11-90ed-e49a011f9b8f  *******/
    client = boto3.client("rds")
    response = client.modify_db_instance(
        DBInstanceIdentifier=DBInstanceIdentifier,
        MasterUserPassword= NewMasterUserPassword,
    )
    return response

def describe_rds_instance(DBInstanceIdentifier):
    client = boto3.client("rds")
    filters = [
        {
            "Name": "db-instance-id",
            "Values":  [DBInstanceIdentifier],
        })
    
    response = client.describe_db_instances(DBInstanceIdentifier=DBInstanceIdentifier)
    return response
 
 def delete_rds_instance(DBInstanceIdentifier):
    client = boto3.client("rds")
    response = client.delete_db_instance(DBInstanceIdentifier=DBInstanceIdentifier)
    return response

def delete_rds_instance(DBInstanceIdentifier):
    client = boto3.client("rds")
    response = client.delete_db_instance(DBInstanceIdentifier=DBInstanceIdentifier)
    DBInstanceIdentifier = DBInstanceIdentifier,
    SkipFinalSnapshot = SkipFinalSnapshot
    )
    return response

create_rds_instance(
    AllocatedStorage,
    DBInstanceClass="db.t2.micro" , 
    DBInstanceIdentifier="database-instance-01", 
    Engine="mysql", 
    MasterUserPassword="testpw0021",
    MasterUsername=  "admin01"
)

modify_rds_instance_password(
    DBInstanceIdentifier="database-instance-01",
    "new-pa$$word")
)

describe_rds_instance(
    DBInstanceIdentifier="database-instance-01"
)

delete_rds_instance(
    "database-instance-01-readreplica",
    SkipFinalSnapshot=True
)
