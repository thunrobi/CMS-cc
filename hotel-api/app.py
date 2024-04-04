from flask import Flask, request, jsonify
from flask_cors import CORS 
import json
PORT=8432


app = Flask(__name__)
CORS(app) # Tillåt cross-origin requests

@app.route("/")
def hello():
    #return "<h1>Hello, World!</h1>"

    ip_address = request.remote_addr
    respData = {"ip_address": ip_address}
    return{ jsonify(respData)
    }

@app.route("/test")
def test():
    if request.method =='POST':
          #skapa rad i databasen, returnera id...
          new_id=555
          return{
        'msg': "Du har skapat en ny rad i databasen, id är",
        'method': request.method
    }
    else:
        return{
            'msg': "TESTING!",
            'method': request.method
        }
@app.route("/test/<int:id>",methods=['GET','PATCH','PUT','DELETE'])
def testId(id):
    if request.method =='GET':
        return{
            'msg':f"här får du id:{id}",
            'method':request.method
        }
    if request.method =='PUT' or request.method =='PATCH' :
        return{
            'msg':f"här får du id:{id}",
            'method':request.method
        }
    
    if request.method == 'DELETE':
        return{
                'msg':f"Du har raferat:{id}",
                'method':request.method
                }
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True, ssl_context=(
        '/etc/letsencrypt/fullchain.pem', 
        '/etc/letsencrypt/privkey.pem'
    ))

