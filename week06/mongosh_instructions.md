#### Installation instructions:<br>

#### Windows<br>
Download installers from the links below.<br>
Make sure to select the msi installaller formats for both files<br>
https://www.mongodb.com/try/download/community <br>
https://www.mongodb.com/try/download/shell
<br><br>

#### Mac OS
https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/ <br><br>




#### This is a very brief introduction to using the Mongo Shell CLI (Command Line Interface) with a local database. The ```mongosh``` command starts the server. All the other commands can be performed either through the CLI, as described below, or through a Python or Javascript library. In the ```pymongo_demo.ipynb``` file, you can find a demonstration of the PyMongo Python library.

#### 1. Start the database server in the terminal. You will be able to see the local address at which the databases are available. <br>
```$ mongosh```

#### Mac users: if you're getting a MongoNetworkError, run ```brew services start mongodb-community``` first, and then ```mongosh```.

#### 2. Now, using this command you can access help with Mongo:
#### You can also use the documentation: 
```$ help```

#### 3. Dispaly information about all databases:
```$ show dbs```

#### 4. Now, let's create our own database!
Create and start using the created database:<br>
```$ use bigDataDB```

#### 5. Data objects or structures in the database are referred to as documents. The documents are sotred in collections.

Let's create a collection:<br>
```$ db.createCollection("students")```

#### 6. Insert a document into the collection.
```$ db.testItems.insertOne({"name": "Marysia", "last_name": "Tańska"})```

#### Side note - naming conventions:
- use camelCase
- for database names, add "DB", e.g. "marysiaDB"
- for collection names, use plural, e.g. "creativeCompStudents"
- for one-to-one relationships (relationships between documents) or anything relating to IDs, use "_id" suffix
- try to keep the names reasonably short, particularly if your database will be big
