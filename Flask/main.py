import functools
import re
from flask import Flask, json, make_response, request, jsonify
from flask.globals import g
from bson import ObjectId
from pymongo import MongoClient
import jwt
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_cors import CORS

# Configuration Lines of Code

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'PasswordSecret'

client = MongoClient("mongodb://127.0.0.1:27017")
mongo_database = client.COM661


mongo_blacklist = mongo_database.Blacklist
mongo_user = mongo_database.Users
mongo_posts = mongo_database.Posts
mongo_comments = mongo_database.Comments



# End of Configuration Lines of Code

# User Defined Wrappers for Protecting End Points
def user_authentication_required(func):
    @wraps(func)
    def decorated(*args,**kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            blacklist_token = mongo_blacklist.find_one({"token":token})
            if blacklist_token is not None:
                return make_response(jsonify({"ALERT!": "JSON Web Token has been Revoked. Please Login Again."}), 401)
        if not token:
            return jsonify({"ALERT!": "Missing JSON Web Token"}), 401
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], options={"verify_signature": False})
        except:
            return jsonify({"ALERT!": "Invalid JSON Web Token"}), 401
        return func(*args,**kwargs)
    return decorated


def admin_authentication_required(func):
    @wraps(func)
    def decorated(*args,**kwargs):
        token = request.headers["x-access-token"]
        payload = jwt.decode(token, app.config['SECRET_KEY'], options={"verify_signature": False})
        if payload["User_Admin"]:
            return func(*args, **kwargs)
        else:
            return make_response(jsonify({'ALERT!' : 'Admin Authentication Required.'}), 401)
    return decorated














@app.route("/api/v1.0/posts", methods=["GET"])
def get_all_posts():
    if request.method == "GET":

        page_num, page_size = 1, 5

        if request.args.get('pn'):
            page_num = int(request.args.get('pn'))
        if request.args.get('ps'):
            page_size = int(request.args.get('ps'))

        page_start = (page_size * (page_num - 1))
        data_to_return = []

        for Post_Object in mongo_posts.find().sort("post_uuid", -1).skip(page_start).limit(page_size):
            Post_Object['_id'] = str(Post_Object['_id'])

            data_to_return.append(Post_Object)

        return make_response( jsonify(data_to_return), 200 )






@app.route("/api/v1.0/posts/<int:Post_UUID>", methods=["GET"])
def get_one_post(Post_UUID):
    if request.method == "GET":
        data_to_return = []
        for Post_Object in mongo_posts.find({"post_uuid": Post_UUID}):
            Post_Object["_id"] = str(Post_Object["_id"])
            data_to_return.append(Post_Object)
            return make_response(jsonify(data_to_return), 200)
        else:
            return make_response(jsonify({"ALERT!": "Post not found. Please Try Again"}), 200)



@app.route("/api/v1.0/posts/<int:Post_UUID>", methods=["DELETE"])
def delete_one_post(Post_UUID):
   if request.method == "DELETE":
        Post_Object = mongo_posts.delete_one({'post_uuid':Post_UUID})
        if Post_Object.deleted_count == 1:
            return make_response( jsonify( {} ), 204)
        else:
            return make_response( jsonify({ "ALERT!" : "Invalid Post ID. Please Try Again." } ), 404)


@app.route("/api/v1.0/posts", methods=["POST"])
def create_one_post():
    if request.method == "POST":
        data_to_retrun = []
        for Post_Object in mongo_posts.find().sort("post_uuid", -1).limit(1):
            data_to_retrun.append(Post_Object)
        
        next_post_uuid = data_to_retrun[-1]["post_uuid"] + 1

        date_now = str(datetime.date.today())
        new_post = {
            "post_uuid": next_post_uuid,
            "post_author_username": request.form["Post_Author"],
            "post_title": request.form["Post_Title"],
            "post_body": request.form["Post_Body"],
            "post_creation_datetime": date_now, 
            "post_comments": [],
            "post_upvotes": 0,
        }

        mongo_posts.insert_one(new_post)
        new_post_link = "http://localhost:5000/api/v1.0/posts/"+ str(next_post_uuid)
        return make_response(jsonify({"SUCCESS! URL TO POST": new_post_link }), 201)


@app.route("/api/v1.0/posts/<int:Post_UUID>", methods=["PUT"])
def edit_one_post(Post_UUID):
    if request.method == "PUT":
        if "Post_Title" in request.form and "Post_Body" in request.form and "Post_Author" in request.form and "Post_Upvotes" in request.form:
            Post_Object = mongo_posts.update_one({ "post_uuid" : Post_UUID },
                {
                    "$set": {
                            "post_author_username": request.form["Post_Author"],
                            "post_title": request.form["Post_Title"],
                            "post_body": request.form["Post_Body"],
                            "post_upvotes": request.form["Post_Upvotes"],

                    }
                }
            )
            if Post_Object.matched_count == 1:
                edited_post_link = "http://localhost:5000/api/v1.0/posts/" + str(Post_UUID)
                return make_response(jsonify({"SUCCESS! URL TO POST": edited_post_link }), 200)
            else: 
                return make_response( jsonify( { "ALERT!":"Invalid Post ID" } ), 404)
        else:
            return make_response( jsonify({ "ALERT!" : "Missing Form Data. Please Try Again." } ), 404)
         


        






@app.route("/api/v1.0/profile/<string:Username>", methods=["GET"])
def user_profile(Username):
    if request.method == "GET":
        User_Object = mongo_comments.find_one({"username":Username})
        if User_Object is not None:
            User_Object_Information = []
            User_Object["_id"]  = str(User_Object["_id"])
            User_Object_Information.append({
                "username": User_Object["username"], 
                "first_name": User_Object["first_name"], 
                "last_name": User_Object["last_name"], 
                "registered_date": User_Object["registered_date"]
            })
            return make_response(jsonify(User_Object_Information), 200)
        else:
            return make_response(jsonify({"ALERT!": "USER ACCOUNT NOT FOUND. PLEASE TRY AGAIN"}), 401)



@app.route("/api/v1.0/register", methods=["POST"])
def user_register():
    if request.method == "POST":
        if "Username" in request.form and  "First_Name" in request.form and  "Last_Name" in request.form and "Email_1" in request.form and "Email_2" in request.form and "Password_1" in request.form and "Password_2" in request.form:
            if request.form["Username"] == "" or request.form["First_Name"] == "" or request.form["Last_Name"] == "" or request.form["Email_1"] == "" or request.form["Email_2"] == "" or request.form["Password_1"] == "" or request.form["Password_2"] == None:
                return make_response(jsonify({"ALERT!": "MISSING FORM DATA. PLEASE TRY AGAIN."}))

            check_username = mongo_user.find_one({"username": request.form["Username"]})
            if check_username is not None:
                return make_response(jsonify({"ALERT!": "USERNAME ALREADY TAKEN. PLEASE CHOSE A DIFFERENT USERNAME"}), 400)
            
            elif request.form["Email_1"] != request.form["Email_2"]:
                return make_response(jsonify({"ALERT!": "EMAILS DO NOT MATCH. PLEASE ENSURE YOUR EMAILS MATCH"}), 400)

            elif request.form["Password_1"] != request.form["Password_2"]:
                return make_response(jsonify({"ALERT!": "PASSWORDS DO NOT MATCH. PLEASE ENSURE YOUR PASSWORDS MATCH"}), 400)

            else:
                date_now = str(datetime.date.today())
                new_user = {
                    "username": request.form["Username"],
                    "first_name": request.form["First_Name"],
                    "last_name": request.form["Last_Name"],
                    "password": generate_password_hash(request.form["Password_1"]),
                    "email": request.form["Email_1"],
                    "registered_date": date_now,
                    "user_admin": False
                }
                print(generate_password_hash(request.form["Password_1"]))
                mongo_user.insert_one(new_user)
                return make_response(jsonify({"SUCCESS!": "NEW USER CREATED"}), 200)

        return make_response(jsonify({"ALERT!": "RECIEVED AN EMPTY FORM"}), 400)


# Hello

@app.route("/api/v1.0/login", methods=["POST"])
def user_login():
    if request.method == "POST":
        authentication = request.authorization
        if authentication:
            user_exist = mongo_user.find_one( {'username': authentication.username } )
            if user_exist is not None:
                if check_password_hash(user_exist['password'], authentication.password):
                    token = jwt.encode(
                    {
                        'Username': authentication.username,
                        'User_Admin': user_exist['user_admin'],
                        'Expiration': str(datetime.datetime.utcnow() + datetime.timedelta(seconds=900))
                    },
                    app.config['SECRET_KEY'])
                    return jsonify({"Token": token})
                else:
                    return make_response(jsonify({'ALERT!':'Bad Password. Please Try Again.'}), 401)
            else:
                return make_response(jsonify({'ALERT!':'Bad Username. Please Try Again.'}), 401)
        else:
            return make_response(jsonify({'ALERT!':'Authentication Required'}), 401)


@app.route("/api/v1.0/logout", methods=["GET"])
@user_authentication_required
def user_logout():
    token = request.headers['x-access-token']
    mongo_blacklist.insert_one({ "token": token })
    return make_response(jsonify({"SUCCESS": "Logout was Successful"}), 200)


@app.route("/api/v1.0/admin/users", methods=["GET"])
@user_authentication_required
@admin_authentication_required
def users_all():
    data_to_return = []
    for User_Object in mongo_user.find():
        User_Object['_id'] = str(User_Object['_id'])
        data_to_return.append(User_Object)
    return make_response(jsonify(data_to_return), 200)


@app.route("/api/v1.0/admin/users/<string:User_ID>", methods=["GET"])
@user_authentication_required
@admin_authentication_required
def users_get_one(User_ID):
    if request.method == "GET":
        User_Object = mongo_user.find_one({"_id":ObjectId(User_ID)})
        if User_Object is not None:
            User_Object['_id'] = str(User_Object['_id'])
            return make_response(jsonify(User_Object), 200)
        else:
            return make_response(jsonify({"ALERT!": "USER NOT FOUND IN DATABASE"}), 404)

@app.route("/api/v1.0/admin/users/delete/<string:User_ID>", methods=["DELETE"])
@user_authentication_required
@admin_authentication_required
def user_delete_one(User_ID):
    if request.method  == "DELETE":
        User_Object = mongo_user.delete_one({"_id":ObjectId(User_ID)})
        if User_Object.deleted_count == 1:
            return make_response( jsonify( {} ), 204)
        else:
            return make_response( jsonify({ "ALERT!" : "Invalid User ID. Please Try Again." } ), 404)


@app.route("/api/v1.0/admin/users/update/<string:User_ID>", methods=["PUT"])
@user_authentication_required
@admin_authentication_required
def user_update(User_ID):
    if request.method == "PUT":
        if "Username" in request.form and "First_Name" in request.form and "Last_Name" in request.form and "Email_Address" in request.form:
            User_Object = mongo_user.update_one(
                {"_id": ObjectId(User_ID)},
                {
                "$set": {
                    "username": request.form["Username"],
                    "first_name": request.form["First_Name"], 
                    "last_name": request.form["Last_Name"],
                    "email": request.form["Email_Address"],
                }
                }
            )

            if User_Object.matched_count == 1:
                username = mongo_user.find_one({"_id": ObjectId(User_ID)})
                updated_user_link = "http://localhost:5000/api/v1.0/profile/" + str(username["username"])
                return make_response(jsonify({"SUCCESS! URL TO POST": updated_user_link }), 200)
            else: 
                return make_response( jsonify( { "ALERT!":"Invalid Post ID" } ), 404)
        else:
            return make_response( jsonify({ "ALERT!" : "Missing Form Data. Please Try Again." } ), 404)

    
@app.route("/api/v1.0/posts", methods=["GET"])
def database_posts_all():
    if request.method == "GET":

        data_to_return = []
        for Post_Object in mongo_posts.find():
            Post_Object['_id'] = str(Post_Object['_id'])
            data_to_return.append(Post_Object)

            # page_num, page_size = 1, 10
            # if request.args.get('pn'):
            #     page_num = int(request.args.get('pn'))
            #     if request.args.get('ps'):
            #         page_size = int(request.args.get('ps'))
            #         page_start = (page_size * (page_num - 1))

            #         businesses_list = [ { X : Y } for X, Y in Post_Object.items() ]
            #         print(businesses_list)
            #         data_to_return = businesses_list[ page_start:page_start + page_size]
            #         print(data_to_return)

        return make_response(jsonify(data_to_return), 200)


@app.route("/api/v1.0/post/upvote/<string:Post_ID>", methods=["GET"])
# @user_authentication_required
def post_upvote(Post_ID):
    if request.method == "GET":
        Post_Object_0 = mongo_posts.find_one({"_id": ObjectId(Post_ID)})
        Post_Object = mongo_posts.update_one({"_id": ObjectId(Post_ID)}, {"$set": {"post_upvotes": Post_Object_0["post_upvotes"] + 1,}})
        if Post_Object.matched_count == 1:
            return make_response(jsonify({"SUCCESS!": "Upvoted Comment was Successful!"}))
        else:
            return make_response(jsonify({"ALERT!": "POST NOT FOUND"}))

@app.route("/api/v1.0/posts/create", methods=["POST"])
# @user_authentication_required
def database_posts_create():
    if request.method == "POST":
        # token = request.headers["x-access-token"]
        # username = jwt.decode(token, app.config['SECRET_KEY'], options={"verify_signature": False})

        date_now = str(datetime.date.today())
        post_content = {
            "post_author_username": request.form["Post_Author"], 
            "post_title": request.form["Post_Title"],
            "post_body": request.form["Post_Body"],
            "post_comments": [],
            "post_upvotes": 0,
            "post_creation_datetime": date_now,
            "post_last_edited_datetime": None, 
            "post_edited": False
        }
        new_post_id = mongo_posts.insert_one(post_content)
        new_post_link = "http://localhost:5000/api/v1.0/posts/"+ str(new_post_id.inserted_id)
        return make_response(jsonify({"SUCCESS! URL TO POST": new_post_link }), 201)

@app.route("/api/v1.0/posts/delete/<string:Post_ID>", methods=["DELETE"])
@user_authentication_required
def database_posts_delete(Post_ID):
    # NEED TO CHECK IF THE AUTHOR IS ALSO AUTHENTICATED
    if request.method == "DELETE":
        Post_Object = mongo_posts.delete_one({'_id':ObjectId(Post_ID)})
        if Post_Object.deleted_count == 1:
            return make_response( jsonify( {} ), 204)
        else:
            return make_response( jsonify({ "ALERT!" : "Invalid Post ID. Please Try Again." } ), 404)


@app.route("/api/v1.0/posts/update/<string:Post_ID>", methods=["PUT"])
@user_authentication_required
def database_posts_update(Post_ID):
    if request.method == "PUT":
    # NEED TO CHECK IF THE AUTHOR IS ALSO AUTHENTICATED
        if "Post_Title" in request.form and "Post_Body" in request.form:
            date_now = str(datetime.date.today())
            Post_Object = mongo_posts.update_one(
                { "_id" : ObjectId(Post_ID) },
                {
                    "$set": {
                            "post_title": request.form["Post_Title"],
                            "post_body": request.form["Post_Body"],
                            "post_last_edited_datetime": date_now, 
                            "post_edited": True
                    }
                }
            )

            if Post_Object.matched_count == 1:
                edited_post_link = "http://localhost:5000/api/v1.0/businesses/" + Post_ID
                return make_response(jsonify({"SUCCESS! URL TO POST": edited_post_link }), 200)
            else: 
                return make_response( jsonify( { "ALERT!":"Invalid Post ID" } ), 404)
        else:
            return make_response( jsonify({ "ALERT!" : "Missing Form Data. Please Try Again." } ), 404)


# @app.route("/api/v1.0/posts/<string:Post_ID>", methods=["GET"])
# def database_posts_one(Post_ID):
#     if request.method == "GET":
#         Post_Object = mongo_posts.find_one({'_id':ObjectId(Post_ID)})
#         if Post_Object is not None:
#             Post_Object['_id'] = str(Post_Object['_id'])
#             return make_response(jsonify(Post_Object), 200)
#         else:
#             return make_response(jsonify({"ALERT!": "POST NOT FOUND"}), 401)








@app.route("/api/v1.0/comment/add/<string:Post_ID>", methods=["POST"])
# @user_authentication_required
def comment_add(Post_ID):
    if request.method == "POST":
        token = request.headers["x-access-token"]
        username = jwt.decode(token, app.config['SECRET_KEY'], options={"verify_signature": False})

        post_uuid = mongo_posts.find_one({"_id": ObjectId(Post_ID)})
        print(post_uuid["_id"])

        date_now = str(datetime.date.today())
        comment_content = {
            "post_uuid": post_uuid, 
            "comment_author_username": username['Username'],
            "comment_body": request.form["Comment_Body"],
            "comment_creation_datetime": date_now,
            "last_edited_date_time": None,
            "comment_edited": False,
            "comment_upvotes": 0
            }
        new_comment_id = mongo_comments.insert_one(comment_content)
        new_comment_link = "http://localhost:5000/api/v1.0/comments/"+ str(new_comment_id.inserted_id)
        mongo_posts.update_one({"_id": ObjectId(Post_ID)},{"$push": {"post_comments": str(new_comment_link)}})
        return make_response(jsonify({"SUCCESS! URL TO COMMENT": new_comment_link }), 201)










@app.route("/api/v1.0/comments/<string:Post_ID>", methods=["GET"])
@user_authentication_required
def database_comments_all_per_post(Post_ID):
    if request.method == "GET":
        data_to_return = []
        for Comment_Object in mongo_comments.find({"post_uuid": Post_ID}):
            Comment_Object['_id'] = str(Comment_Object['_id'])
            data_to_return.append(Comment_Object)
        return make_response(jsonify(data_to_return), 200)



@app.route("/api/v1.0/comments/create/<string:Post_ID>", methods=["POST"])
@user_authentication_required
def comment_create(Post_ID):
    if request.method == "POST":
        token = request.headers["x-access-token"]
        username = jwt.decode(token, app.config['SECRET_KEY'], options={"verify_signature": False})

        post_uuid = str(mongo_posts.find_one({"_id": ObjectId(Post_ID)}))

        date_now = str(datetime.date.today())
        comment_content = {
            "post_uuid": post_uuid, 
            "comment_author_username": username['Username'],
            "comment_body": request.form["Comment_Body"],
            "comment_creation_datetime": date_now,
            "last_edited_date_time": None,
            "comment_edited": False,
            "comment_upvotes": 0
            }
        new_comment_id = mongo_comments.insert_one(comment_content)
        new_comment_link = "http://localhost:5000/api/v1.0/comments/"+ str(new_comment_id.inserted_id)
        return make_response(jsonify({"SUCCESS! URL TO COMMENT": new_comment_link }), 201)




@app.route("/api/v1.0/comments/update/<string:Comment_ID>", methods=["PUT"])
@user_authentication_required
def comment_edit(Comment_ID):
    if request.method == "PUT":
        if "Comment_Body" in request.form:
            date_now = str(datetime.date.today())
            Comment_Object = mongo_comments.update_one({"_id": ObjectId(Comment_ID)},
            {
                "$set": {
                    "comment_body": request.form["Comment_Body"],
                    "comment_edited": True,
                    "last_edited_datetime": date_now
                }
            }
            )
            if Comment_Object.matched_count == 1:
                return make_response(jsonify({"SUCCESS!": "COMMENT WAS UPDATED"}), 200)
            else: 
                return make_response( jsonify( { "ALERT!":"Invalid Comment" } ), 404)
        
    else:
        return make_response( jsonify({ "ALERT!" : "Missing Form Data. Please Try Again." } ), 404)


            
@app.route("/api/v1.0/comments/delete/<string:Comment_ID>", methods=["DELETE"])
def comment_delete(Comment_ID):
    if request.method  == "DELETE":
        Comment_Object = mongo_comments.delete_one({"_id":ObjectId(Comment_ID)})
        if Comment_Object.deleted_count == 1:
            return make_response( jsonify( {} ), 204)
        else:
            return make_response( jsonify({ "ALERT!" : "Invalid Comment ID. Please Try Again." } ), 404)


@app.route("/api/v1.0/comment/<string:Comment_ID>", methods=["GET"])
def comment_get_one(Comment_ID):
    if request.method == "GET":
        Comment_Object = mongo_comments.find_one({"_id":ObjectId(Comment_ID)})
        print(Comment_Object)
        if Comment_Object is not None:
            Comment_Object['_id'] = str(Comment_Object['_id'])
            return make_response(jsonify(Comment_Object), 200)
        else:
            return make_response(jsonify({"ALERT!": "COMMENT NOT FOUND"}))


@app.route("/api/v1.0/admin/users/<string:User_ID>", methods=["GET"])
@user_authentication_required
@admin_authentication_required
def admin_get_one_user(User_ID):
    if request.method == "GET":
        User_Obect = mongo_user.find_one({'_id':ObjectId(User_ID)})
        if User_Obect is not None:
            User_Obect['_id'] = str(User_Obect['_id'])
            return make_response(jsonify(User_Obect), 200)
        else:
            return make_response(jsonify({"ALERT!": "USER NOT FOUND"}), 401)


# @app.route("/api/v1.0/admin/comments/<string:Post_ID>", methods=["POST"])
# @app.route("/api/v1.0/admin/comments/delete/<string:Post_ID>", methods=["POST"])
# Get's all posts from user
# @app.route("/api/v1.0/admin/posts/<string:User_ID>", methods=["POST"])
# Delete Post from database
# @app.route("/api/v1.0/admin/posts/delete/<string:User_ID>", methods=["POST"])
# Get's all users information
# Get's one user information
# @app.route("/api/v1.0/admin/users/<string:User_ID>", methods=["POST"])
# Deletes User from Database
# @app.route("/api/v1.0/admin/users/delete/<string:User_ID>", methods=["POST"])
# Updates user infromation
# @app.route("/api/v1.0/admin/users/update/<string:User_ID>", methods=["POST"])
# Makes new user and will be admin by default
# @app.route("/api/v1.0/admin/new", methods=["POST"])












if __name__ == "__main__":
    app.run(debug=True)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XX                                                                          XX
# XX   MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM   XX
# XX   MMMMMMMMMMMMMMMMMMMMMssssssssssssssssssssssssssMMMMMMMMMMMMMMMMMMMMM   XX
# XX   MMMMMMMMMMMMMMMMss'''                          '''ssMMMMMMMMMMMMMMMM   XX
# XX   MMMMMMMMMMMMyy''                                    ''yyMMMMMMMMMMMM   XX
# XX   MMMMMMMMyy''                                            ''yyMMMMMMMM   XX
# XX   MMMMMy''                                                    ''yMMMMM   XX
# XX   MMMy'                                                          'yMMM   XX
# XX   Mh'                                                              'hM   XX
# XX   -                                                                  -   XX
# XX                                                                          XX
# XX   ::                                                                ::   XX
# XX   MMhh.        ..hhhhhh..                      ..hhhhhh..        .hhMM   XX
# XX   MMMMMh   ..hhMMMMMMMMMMhh.                .hhMMMMMMMMMMhh..   hMMMMM   XX
# XX   ---MMM .hMMMMdd:::dMMMMMMMhh..        ..hhMMMMMMMd:::ddMMMMh. MMM---   XX
# XX   MMMMMM MMmm''      'mmMMMMMMMMyy.  .yyMMMMMMMMmm'      ''mmMM MMMMMM   XX
# XX   ---mMM ''             'mmMMMMMMMM  MMMMMMMMmm'             '' MMm---   XX
# XX   yyyym'    .              'mMMMMm'  'mMMMMm'              .    'myyyy   XX
# XX   mm''    .y'     ..yyyyy..  ''''      ''''  ..yyyyy..     'y.    ''mm   XX
# XX           MN    .sMMMMMMMMMss.   .    .   .ssMMMMMMMMMs.    NM           XX
# XX           N`    MMMMMMMMMMMMMN   M    M   NMMMMMMMMMMMMM    `N           XX
# XX            +  .sMNNNNNMMMMMN+   `N    N`   +NMMMMMNNNNNMs.  +            XX
# XX              o+++     ++++Mo    M      M    oM++++     +++o              XX
# XX                                oo      oo                                XX
# XX           oM                 oo          oo                 Mo           XX
# XX         oMMo                M              M                oMMo         XX
# XX       +MMMM                 s              s                 MMMM+       XX
# XX      +MMMMM+            +++NNNN+        +NNNN+++            +MMMMM+      XX
# XX     +MMMMMMM+       ++NNMMMMMMMMN+    +NMMMMMMMMNN++       +MMMMMMM+     XX
# XX     MMMMMMMMMNN+++NNMMMMMMMMMMMMMMNNNNMMMMMMMMMMMMMMNN+++NNMMMMMMMMM     XX
# XX     yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy     XX
# XX   m  yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy  m   XX
# XX   MMm yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy mMM   XX
# XX   MMMm .yyMMMMMMMMMMMMMMMM     MMMMMMMMMM     MMMMMMMMMMMMMMMMyy. mMMM   XX
# XX   MMMMd   ''''hhhhh       odddo          obbbo        hhhh''''   dMMMM   XX
# XX   MMMMMd             'hMMMMMMMMMMddddddMMMMMMMMMMh'             dMMMMM   XX
# XX   MMMMMMd              'hMMMMMMMMMMMMMMMMMMMMMMh'              dMMMMMM   XX
# XX   MMMMMMM-               ''ddMMMMMMMMMMMMMMdd''               -MMMMMMM   XX
# XX   MMMMMMMM                   '::dddddddd::'                   MMMMMMMM   XX
# XX   MMMMMMMM-                                                  -MMMMMMMM   XX
# XX   MMMMMMMMM                                                  MMMMMMMMM   XX
# XX   MMMMMMMMMy                                                yMMMMMMMMM   XX
# XX   MMMMMMMMMMy.                                            .yMMMMMMMMMM   XX
# XX   MMMMMMMMMMMMy.                                        .yMMMMMMMMMMMM   XX
# XX   MMMMMMMMMMMMMMy.                                    .yMMMMMMMMMMMMMM   XX
# XX   MMMMMMMMMMMMMMMMs.                                .sMMMMMMMMMMMMMMMM   XX
# XX   MMMMMMMMMMMMMMMMMMss.           ....           .ssMMMMMMMMMMMMMMMMMM   XX
# XX   MMMMMMMMMMMMMMMMMMMMNo         oNNNNo         oNMMMMMMMMMMMMMMMMMMMM   XX
# XX                                                                          XX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

#     .o88o.                               o8o                .
#     888 `"                               `"'              .o8
#    o888oo   .oooo.o  .ooooo.   .ooooo.  oooo   .ooooo.  .o888oo oooo    ooo
#     888    d88(  "8 d88' `88b d88' `"Y8 `888  d88' `88b   888    `88.  .8'
#     888    `"Y88b.  888   888 888        888  888ooo888   888     `88..8'
#     888    o.  )88b 888   888 888   .o8  888  888    .o   888 .    `888'
#    o888o   8""888P' `Y8bod8P' `Y8bod8P' o888o `Y8bod8P'   "888"      d8'
#                                                                 .o...P'
#                                                                 `XER0'

