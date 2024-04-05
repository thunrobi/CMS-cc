import psycopg, os
from psycopg.rows import dict_row
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS 


load_dotenv()

PORT=8432

db_url = os.environ.get("DB_URL") 
print(db_url)
conn = psycopg.connect(db_url,autocommit=True, row_factory=dict_row)

app = Flask(__name__)
CORS(app) # Tillåt cross-origin requests

roomsTEMP = [
    {'number': 101, 'type': "single"},
     {'number': 102, 'type': "double"},
     {'number': 103, 'type': "single"},
     {'number': 104, 'type': "suite"},
]

@app.route("/test", methods=['GET', 'POST'])
def dbtest():
     with conn.cursor() as cur:
        cur.execute("SELECT * from people")
        rows = cur.fetchall()
        return rows
     

    

@app.route("/rooms", methods=['GET', 'POST'])
def room_endpoint():
    if request.method == 'POST':
        # skapa rad i databasen, returnera ny id..
        request_body = request.get_json()
        print(request_body)
        return { 
            'msg': f"Du har skapat ett nytt rum, id: {len(roomsTEMP)-1}!",

        }
 
        

@app.route("/rooms/<int:id>", methods=['GET', 'PUT', 'PATCH', 'DELETE'] )
def one_room_enpoint(id):
        if request.method == 'GET':
            return { roomsTEMP[id]
               
            }
        if request.method == 'PUT' or request.method == 'PATCH':
            return { 
                'msg': f"Du uppdaterar id: {id}",
                'method': request.method 
            }
        if request.method == 'DELETE':
            return { 
                'msg': f"Du har raderat {id}",
                'method': request.method 
            }



@app.route("/ip")
def ip():
    return { 'ip': request.remote_addr }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True, ssl_context=(
        '/etc/letsencrypt/fullchain.pem', 
        '/etc/letsencrypt/privkey.pem'
    ))