from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request     
from flask_app.models import user, like   

class Memory:
    db_name = "travel_mem_schema_many" 
    def __init__( self , data ):
        self.id = data['id']
        self.location = data['location']
        self.country = data['country']
        self.date = data['date']
        self.description = data['description']
        self.img_name = data['img_name']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.likes_data = []
        self.users_who_liked = []
        self.user_ids_who_liked =[]
        self.users_who_commented = []
        self.user_ids_who_commented = []

    @classmethod
    def get_all_likes_from_one_memory(cls,data):
        query = ''' 
                    SELECT * FROM memories JOIN users AS creators ON memories.user_id = creators.id
                    LEFT JOIN likes ON memories.id = likes.memory_id
                    LEFT JOIN users as users_who_liked on likes.user_id=users_who_liked.id
                    WHERE memories.id = %(id)s; 
                '''
        results = connectToMySQL(cls.db_name).query_db(query,data)
        # Create an empty list to append our instances of memories
        # Iterate over the db results and create instances of memories with cls.
        print(results)
        if len(results) == 0:
            return []
        else:
            new_memory = True
            for memory_dictionary in results:
                if new_memory:
                    memory_instance = cls(memory_dictionary)
                    this_user_dictionary = {
                        "id": memory_dictionary['creators.id'],
                        "first_name": memory_dictionary['first_name'],
                        "last_name": memory_dictionary['last_name'],
                        "city": memory_dictionary['city'],
                        "state": memory_dictionary['state'],
                        "email": memory_dictionary['email'],
                        "password": memory_dictionary['password'],
                        "profile_pic": memory_dictionary['profile_pic'],
                        "created_at": memory_dictionary['creators.created_at'],
                        "updated_at": memory_dictionary['creators.updated_at'],
                    }
                    this_user_instance = user.User(this_user_dictionary)
                    memory_instance.this_user_instance = this_user_instance 
                    new_memory = False

                if memory_dictionary['users_who_liked.id']:
                    user_who_liked_data = {
                    "id": memory_dictionary['users_who_liked.id'],
                    "first_name": memory_dictionary['users_who_liked.first_name'],
                    "last_name": memory_dictionary['users_who_liked.last_name'],
                    "city": memory_dictionary['users_who_liked.city'],
                    "state": memory_dictionary['users_who_liked.state'],
                    "email": memory_dictionary['users_who_liked.email'],
                    "password": memory_dictionary['users_who_liked.password'],
                    "profile_pic": memory_dictionary['users_who_liked.profile_pic'],
                    "created_at": memory_dictionary['users_who_liked.created_at'],
                    "updated_at": memory_dictionary['users_who_liked.updated_at'],
                }
                    
                    this_user_like_instance = user.User(user_who_liked_data)
                    memory_instance.users_who_liked.append(this_user_like_instance)
                    memory_instance.user_ids_who_liked.append(memory_dictionary['users_who_liked.id'])
            return memory_instance

    @classmethod
    def get_all_comments_from_one_memory(cls,data):
        query = ''' 
                    SELECT * FROM memories JOIN users AS creators ON memories.user_id = creators.id
                    LEFT JOIN comments ON memories.id = comments.memory_id
                    LEFT JOIN users as users_who_commented on comments.user_id=users_who_commented.id
                    WHERE memories.id = %(id)s; 
                '''
        results = connectToMySQL(cls.db_name).query_db(query,data)
        # Create an empty list to append our instances of memories
        # Iterate over the db results and create instances of memories with cls.
        print(results)
        if len(results) == 0:
            return []
        else:
            new_memory = True
            for memory_dictionary in results:
                if new_memory:
                    memory_instance = cls(memory_dictionary)
                    this_user_dictionary = {
                        "id": memory_dictionary['creators.id'],
                        "first_name": memory_dictionary['first_name'],
                        "last_name": memory_dictionary['last_name'],
                        "city": memory_dictionary['city'],
                        "state": memory_dictionary['state'],
                        "email": memory_dictionary['email'],
                        "password": memory_dictionary['password'],
                        "profile_pic": memory_dictionary['profile_pic'],
                        "created_at": memory_dictionary['creators.created_at'],
                        "updated_at": memory_dictionary['creators.updated_at'],
                    }
                    this_user_instance = user.User(this_user_dictionary)
                    memory_instance.this_user_instance = this_user_instance 
                    new_memory = False

                if memory_dictionary['users_who_commented.id']:
                    user_who_commented_data = {
                    "id": memory_dictionary['users_who_commented.id'],
                    "first_name": memory_dictionary['users_who_commented.first_name'],
                    "last_name": memory_dictionary['users_who_commented.last_name'],
                    "city": memory_dictionary['users_who_commented.city'],
                    "state": memory_dictionary['users_who_commented.state'],
                    "email": memory_dictionary['users_who_commented.email'],
                    "password": memory_dictionary['users_who_commented.password'],
                    "profile_pic": memory_dictionary['users_who_commented.profile_pic'],
                    "created_at": memory_dictionary['users_who_commented.created_at'],
                    "updated_at": memory_dictionary['users_who_commented.updated_at'],
                }
                    
                    this_user_like_instance = user.User(user_who_commented_data)
                    memory_instance.users_who_commented.append(this_user_like_instance)
                    memory_instance.user_ids_who_commented.append(memory_dictionary['users_who_commented.id'])
            return memory_instance



                
    @classmethod
    def get_all_likes(cls):
        query = ''' 
                    SELECT * FROM memories JOIN users ON memories.user_id = users.id
                    LEFT JOIN likes ON memories.id = likes.memory_id
                    LEFT JOIN users as users_who_liked on likes.user_id=users_who_liked.id; 
                '''
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db_name).query_db(query)
        # Create an empty list to append our instances of memories
        memories = []
        print(results)
        # Iterate over the db results and create instances of memories with cls.
        if len(results) == 0:
            return []
        else:
            for memory_dictionary in results:
                new_memory = True
                user_who_liked_data = {
                    "id": memory_dictionary['users_who_liked.id'],
                    "first_name": memory_dictionary['users_who_liked.first_name'],
                    "last_name": memory_dictionary['users_who_liked.last_name'],
                    "city": memory_dictionary['users_who_liked.city'],
                    "state": memory_dictionary['users_who_liked.state'],
                    "email": memory_dictionary['users_who_liked.email'],
                    "password": memory_dictionary['users_who_liked.password'],
                    "profile_pic": memory_dictionary['users_who_liked.profile_pic'],
                    "created_at": memory_dictionary['users_who_liked.created_at'],
                    "updated_at": memory_dictionary['users_who_liked.updated_at']
                }

                number_of_likes = len(memories)
                if number_of_likes > 0:
                    last_memory = memories[number_of_likes-1]
                    if last_memory.id == memory_dictionary['id']:
                        last_memory.user_ids_who_liked.append(memory_dictionary['users_who_liked.id'])
                        last_memory.users_who_liked.append(user.User(user_who_liked_data))
                        new_memory = False



                if new_memory:
                    memory_instance = cls(memory_dictionary)
                    this_user_dictionary = {
                        "id": memory_dictionary['users.id'],
                        "first_name": memory_dictionary['first_name'],
                        "last_name": memory_dictionary['last_name'],
                        "city": memory_dictionary['city'],
                        "state": memory_dictionary['state'],
                        "email": memory_dictionary['email'],
                        "password": memory_dictionary['password'],
                        "profile_pic": memory_dictionary['profile_pic'],
                        "created_at": memory_dictionary['users.created_at'],
                        "updated_at": memory_dictionary['users.updated_at']
                    }
                    this_user_instance = user.User(this_user_dictionary)
                    memory_instance.user = this_user_instance 
                    if memory_dictionary['users_who_liked.id']:
                        memory_instance.user_ids_who_liked.append(memory_dictionary['users_who_liked.id'])
                        memory_instance.users_who_liked.append(user.User(user_who_liked_data))
                    memories.append(memory_instance)        
            return memories


    @classmethod
    def get_all_memories(cls):
        query = "SELECT * FROM memories;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db_name).query_db(query)
        # Create an empty list to append our instances of memories
        memories = []
        # Iterate over the db results and create instances of memories with cls.
        if len(results) == 0:
            return []
        else:
            for memory in results:
                memories.append( cls(memory) )
            return memories

    @classmethod
    def get_memory_by_id(cls, data):
        query = "SELECT * FROM memories WHERE id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db_name).query_db(query, data) 
        if len(results) == 0:
            return None
        else:
            return cls(results[0])
    
    @classmethod
    def save_memory(cls, data):
        query = "INSERT INTO memories ( location , country , date , description , img_name , user_id , created_at, updated_at ) VALUES ( %(location)s , %(country)s , %(date)s  , %(description)s ,  %(img_name)s , %(user_id)s,  NOW() , NOW());"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db_name).query_db( query, data )

    @classmethod
    def edit_memory(cls, data):
        query = "UPDATE memories SET location = %(location)s, country = %(country)s, date = %(date)s, description = %(description)s, img_name = %(img_name)s, user_id = %(user_id)s WHERE id = %(id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db_name).query_db( query, data )

    @classmethod
    def delete_memory(cls,data):
        query = "DELETE FROM memories WHERE id = %(id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db_name).query_db( query, data )

    @classmethod
    def like(cls,data):
        query = "INSERT INTO likes (memory_id, user_id) VALUES (%(id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db( query, data)

    @classmethod
    def unlike(cls,data):
        query = "DELETE FROM likes WHERE memory_id = %(id)s AND user_id = %(user_id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db_name).query_db( query, data )

    @classmethod
    def get_memory_by_user(cls,data):
        query = "SELECT * FROM memories JOIN users ON users.id = memories.user_id WHERE memories.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            this_memory_instance = cls(results[0])
            this_user_dictionary = {
                "id": results[0]['users.id'],
                "first_name": results[0]['first_name'],
                "last_name": results[0]['last_name'],
                "city": results[0]['city'],
                "state": results[0]['state'],
                "email": results[0]['email'],
                "password": results[0]['password'],
                "profile_pic": results[0]['profile_pic'],
                "created_at": results[0]['users.created_at'],
                "updated_at": results[0]['users.updated_at']
            }
            this_user_instance = user.User(this_user_dictionary)
            this_memory_instance.user = this_user_instance
        return this_memory_instance

    @classmethod
    def get_all_memories_with_users(cls):
        query = "SELECT * FROM memories JOIN users ON users.id = memories.user_id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        memory_instances =[]
        if len(results) == 0:
            return []
        else:
            for memory_dictionary in results:
                memory_instance = cls(memory_dictionary)
                this_user_dictionary = {
                    "id": memory_dictionary['users.id'],
                    "first_name": memory_dictionary['first_name'],
                    "last_name": memory_dictionary['last_name'],
                    "city": memory_dictionary['city'],
                    "state": memory_dictionary['state'],
                    "email": memory_dictionary['email'],
                    "password": memory_dictionary['password'],
                    "profile_pic": memory_dictionary['profile_pic'],
                    "created_at": memory_dictionary['users.created_at'],
                    "updated_at": memory_dictionary['users.updated_at']
                }
                this_user_instance = user.User(this_user_dictionary)
                memory_instance.user = this_user_instance 
                memory_instances.append(memory_instance)
            return memory_instances


    @staticmethod
    def validate_memory(memory):
        is_valid = True
        if len(memory['location']) < 3 or (memory['location']).replace(' ', '').isalpha() == False:
            flash("Location must be at least 3 characters long and 1 word only.", "memory")
            is_valid = False
        if len(memory['country']) < 3 or (memory['country']).replace(' ', '').isalpha() == False:
            flash("Country must be at least 3 characters long.", "memory")
            is_valid = False
        if len(memory['date']) < 1:
            flash("Fill in date.", "memory")
            is_valid = False
        if len(memory['description']) < 12:
            flash("Description must be at least 12 characters long.", "memory")
            is_valid = False
        return is_valid

    @classmethod
    def get_memories_by_user(cls,data):
        query = "SELECT * FROM memories JOIN users ON users.id = memories.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        list_of_memory_instances =[]
        print(results)
        if len(results) == 0:
            return []  
        else:
            for this_memory_dictionary in results:
                this_memory_instance = cls(this_memory_dictionary)
                this_user_dictionary = {
                    "id": this_memory_dictionary['users.id'],
                    "first_name": this_memory_dictionary['first_name'],
                    "last_name": this_memory_dictionary['last_name'],
                    "city": this_memory_dictionary['city'],
                    "state": this_memory_dictionary['state'],
                    "email": this_memory_dictionary['email'],
                    "password": this_memory_dictionary['password'],
                    "profile_pic": this_memory_dictionary['profile_pic'],
                    "created_at": this_memory_dictionary['users.created_at'],
                    "updated_at": this_memory_dictionary['users.updated_at']
                }
                this_user_instance = user.User(this_user_dictionary)
                this_memory_instance.user = this_user_instance
            return list_of_memory_instances 


        