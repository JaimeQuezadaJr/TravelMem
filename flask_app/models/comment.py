from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request     
from flask_app.models import user   

class Comment:
    db_name = "travel_mem_schema_many" 
    def __init__( self , data ):
        self.id = data['id']
        self.comment = data['comment']
        self.memory_id = data['memory_id']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def add_comment(cls,data):
        query = "INSERT INTO comments (comment, memory_id, user_id) VALUES (%(comment)s, %(id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db( query, data)

    @classmethod
    def delete_comment(cls,data):
        query = "DELETE FROM comments WHERE memory_id = %(id)s AND user_id = %(user_id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db_name).query_db( query, data )

    @staticmethod
    def validate_comment(comment):
        is_valid = True
        if len(comment['comment']) < 1:
            flash("Empty comment field")
            is_valid = False
        return is_valid
