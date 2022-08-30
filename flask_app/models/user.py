from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request  
from flask_app.models import memory, user, comment      
import re
import string

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db_name = "travel_mem_schema_many"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.city = data['city']
        self.state = data['state']
        self.email = data['email'] 
        self.password = data['password']
        self.profile_pic = data['profile_pic'] 
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.memories = []
        self.comments = []
 
    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        if len(results) == 0:
            return []
        else:
            for user in results:
                users.append( cls(user) )
            return users

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            return cls(results[0])

    
    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users ( first_name , last_name , city, state, email , password , profile_pic, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(city)s, %(state)s, %(email)s  , %(password)s , %(profile_pic)s , NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db_name).query_db( query, data )

    @classmethod
    def edit_user(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, city = %(city)s, state = %(state)s, profile_pic = %(profile_pic)s WHERE id = %(id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db_name).query_db( query, data )


    @classmethod
    def delete_user(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db_name).query_db( query, data )

    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('travel_mem_schema_many').query_db(query, user)
        if len(user['first_name']) < 2 or str.isalpha(user['first_name']) == False:
            flash("First Name must be at least 2 characters long.", "register")
            is_valid = False
        if len(user['last_name']) < 2 or str.isalpha(user['last_name']) == False:
            flash("Last Name must be at least 2 characters long.", "register")
            is_valid = False
        if len(user['city']) < 3 or (user['city']).replace(' ', '').isalpha() == False:
            flash("City must be at least 3 characters long.", "register")
            is_valid = False
        if len(user['state']) < 4 or (user['state']).replace(' ', '').isalpha() == False:
            flash("State must be at least 4 characters long.", "register")
            is_valid = False
        if len(results) >= 1:
            flash("Email already taken.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must contain at least 8 characters.", "register")
            is_valid = False
        if user['confirm_password'] != user['password']:
            flash("Password does not match", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_edit_user(user):
        is_valid = True
        if len(user['first_name']) < 2 or str.isalpha(user['first_name']) == False:
            flash("First Name must be at least 2 characters long.", "update")
            is_valid = False
        if len(user['last_name']) < 2 or str.isalpha(user['last_name']) == False:
            flash("Last Name must be at least 2 characters long.", "update")
            is_valid = False
        if len(user['city']) < 3 or (user['city']).replace(' ', '').isalpha() == False:
            flash("City must be at least 3 characters long.", "update")
            is_valid = False
        if len(user['state']) < 4 or (user['state']).replace(' ', '').isalpha() == False:
            flash("State must be at least 4 characters long.", "update")
            is_valid = False
        return is_valid

    @classmethod
    def grab_one_user_with_all_memories(cls, data):
        query = "SELECT * FROM users LEFT JOIN memories ON users.id = memories.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        if len(results) == 0:
            return None # Return None as we can only get at most one item
        else:
            # Create the user
            this_user_instance = cls(results[0]) # Only holds data for the user itself
            # Loop through each memory and then link to the list of memories for this user
            for this_memory_dictionary in results:
                # Create a new dictionary for the user data
                new_memory_dictionary = {
                    # Table name = table you're joining with - in this case, memories
                    "id": this_memory_dictionary["memories.id"], # Notice the table name here due to duplicate column names!!
                    "location": this_memory_dictionary["location"],
                    "country": this_memory_dictionary["country"],
                    "date": this_memory_dictionary["date"],
                    "description": this_memory_dictionary["description"],
                    "img_name": this_memory_dictionary["img_name"],
                    "user_id": this_memory_dictionary["user_id"],
                    "created_at": this_memory_dictionary["memories.created_at"], # Notice the table name here due to duplicate column names!!
                    "updated_at": this_memory_dictionary["memories.updated_at"], # Notice the table name here due to duplicate column names!!
                }
                # Creating a memory
                this_memory_instance = memory.Memory(new_memory_dictionary)
                # Add this memory to the list of memories for this user
                this_user_instance.memories.append(this_memory_instance)
            # Return the user - with all memories linked
            return this_user_instance
    # Future: You will use static methods to perform validations
    # @staticmethod

    @classmethod
    def get_all_users_with_memories(cls):
        query = "SELECT * FROM users JOIN memories ON users.id = memories.user_id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        user_instances =[]
        if len(results) == 0:
            return []
        else:
            for user_dictionary in results:
                user_instance = cls(user_dictionary)
                this_memory_dictionary = {
                    "id": user_dictionary['memories.id'],
                    "location": user_dictionary['location'],
                    "country": user_dictionary['country'],
                    "date": user_dictionary['date'],
                    "description": user_dictionary['description'],
                    "img_name": user_dictionary['img_name'],
                    "user_id": user_dictionary['user_id'],
                    "created_at": user_dictionary['memories.created_at'],
                    "updated_at": user_dictionary['memories.updated_at']
                }
                this_memory_instance = memory.Memory(this_memory_dictionary)
                user_instance.memories = this_memory_instance
                user_instances.append(user_instance)
            return user_instances

    @classmethod
    def grab_one_user_with_all_memory_likes(cls, data):
        query = '''
        SELECT * FROM users 
        JOIN memories ON memories.user_id = users.id
        LEFT JOIN likes ON memories.id = likes.memory_id
        WHERE likes.user_id = %(id)s;
        '''
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        if len(results) == 0:
            return None # Return None as we can only get at most one item
        else:
            # Create the user
            this_user_instance = cls(results[0]) # Only holds data for the user itself
            # Loop through each memory and then link to the list of memories for this user
            for this_memory_dictionary in results:
                # Create a new dictionary for the user data
                new_memory_dictionary = {
                    # Table name = table you're joining with - in this case, memories
                    "id": this_memory_dictionary["memories.id"], # Notice the table name here due to duplicate column names!!
                    "location": this_memory_dictionary["location"],
                    "country": this_memory_dictionary["country"],
                    "date": this_memory_dictionary["date"],
                    "description": this_memory_dictionary["description"],
                    "img_name": this_memory_dictionary["img_name"],
                    "user_id": this_memory_dictionary["user_id"],
                    "created_at": this_memory_dictionary["memories.created_at"], # Notice the table name here due to duplicate column names!!
                    "updated_at": this_memory_dictionary["memories.updated_at"], # Notice the table name here due to duplicate column names!!
                }
                # Creating a memory
                this_memory_instance = memory.Memory(new_memory_dictionary)
                # Add this memory to the list of memories for this user
                this_user_instance.memories.append(this_memory_instance)
            # Return the user - with all memories linked
            return this_user_instance

    @classmethod
    def grab_one_user_with_all_memory_comments(cls, data):
        query = '''
        SELECT * FROM users 
        JOIN memories ON memories.user_id = users.id
        LEFT JOIN comments ON memories.id = comments.memory_id
        WHERE comments.memory_id = %(id)s;
        '''
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        if len(results) == 0:
            return None # Return None as we can only get at most one item
        else:
            # Create the user
            this_user_instance = cls(results[0]) # Only holds data for the user itself
            # Loop through each memory and then link to the list of memories for this user
            for this_comment_dictionary in results:
                # Create a new dictionary for the user data
                new_comment_dictionary = {
                    # Table name = table you're joining with - in this case, memories
                    "id": this_comment_dictionary["comments.id"], # Notice the table name here due to duplicate column names!!
                    "comment": this_comment_dictionary["comment"],
                    "memory_id": this_comment_dictionary["memory_id"],
                    "user_id": this_comment_dictionary["comments.user_id"],
                    "created_at": this_comment_dictionary["comments.created_at"], # Notice the table name here due to duplicate column names!!
                    "updated_at": this_comment_dictionary["comments.updated_at"], # Notice the table name here due to duplicate column names!!
                }
                # Creating a comment
                this_comment_instance = comment.Comment(new_comment_dictionary)
                # Add this comment to the list of memories for this user
                this_user_instance.comments.append(this_comment_instance)
            # Return the user - with all memories linked
            return this_user_instance

    
    #WHEN TypeERROR : object of type 'bool' has no len() it usually means the table name in your query is incorrect!!!!