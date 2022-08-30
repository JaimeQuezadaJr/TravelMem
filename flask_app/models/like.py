from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request     
from flask_app.models import user   

class Like:
    db_name = "travel_mem_schema_many" 
    def __init__( self , data ):
        self.id = data['id']
        self.memory_id = data['memory_id']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
