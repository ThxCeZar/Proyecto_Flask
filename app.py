from flask import Flask, render_template
from pymongo.mongo_client import MongoClient


# Importing Flask and render_template to create a web application
app = Flask(__name__)

@app.route('/')

def home():
    return render_template('/templates/PaginaInicioSes.html')

if __name__ == '__main__':
    app.run(debug=True)
    


uri = "mongodb+srv://KimmyCesy:dLH5SqZntK53xu3z@clustercar.dd10bwo.mongodb.net/?retryWrites=true&w=majority&appName=ClusterCAR"
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)