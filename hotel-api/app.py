import psycopg, os
from psycopg.rows import dict_row
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS 


load_dotenv()

PORT=8432

db_url = os.environ.get("DB_URL")
print(os.environ.get("FOO"))

conn = psycopg.connect(db_url, autocommit=True, row_factory=dict_row)

app = Flask(__name__)
CORS(app) # Tillåt cross-origin requests

roomsTEMP = [
    { 'number': 101, 'type': "single" },
    { 'number': 202, 'type': "double" },
    { 'number': 303, 'type': "suite" }
]

@app.route("/", )
def info():
    #return "<h1>Hello, Flask!</h1>"
    return "Hotel API, endpoints /rooms, /bookings"


@app.route("/rooms", methods=['GET', 'POST'])
def rooms_endoint():
    if request.method == 'POST':
        request_body = request.get_json()
        print(request_body)
        roomsTEMP.append(request_body)
        return { 
            'msg': f"Du har skapat ett nytt rum, id: {len(roomsTEMP)-1}!"
        }
    else:
        with conn.cursor() as cur:
            cur.execute("""SELECT * 
                        FROM hotel_room 
                        ORDER BY room_number""")
            return cur.fetchall()
        

@app.route("/guests", methods=['GET', 'POST'])
def guests_endoint():
    if request.method == 'POST':
        request_body = request.get_json()
        print(request_body)
        roomsTEMP.append(request_body)
        return { 
            'msg': f"Du har skapat ett nytt rum, id: {len(roomsTEMP)-1}!"
        }
    else:
        with conn.cursor() as cur:
            cur.execute("""SELECT * 
                        FROM hotel_guest
                        ORDER BY firstname""")
            return cur.fetchall()

@app.route("/rooms/<int:id>", methods=['GET', 'PUT', 'PATCH', 'DELETE'] )
def one_room_endpoint(id):
        if request.method == 'GET':
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * 
                    FROM hotel_room 
                    WHERE id = %s""", [id])

                return cur.fetchone()
        
@app.route("/bookings", methods=['GET', 'POST'])
def bookings():
    if request.method == 'GET':
        with conn.cursor() as cur:
            cur.execute("""SELECT 
                         hotel_booking.*,
                         hotel_room,
                         hotel_guest
                    FROM hotel_booking
                    INNER JOIN hotel_room r
                        ON r.id = r.room_number
                    INNER JOIN hotel_guest g
                        ON g.id = g.firstname   
                    ORDER BY hotel_booking.datefrom
                    """)
            return cur.fetchall()
        
    if request.method == 'POST':
        body = request.get_json()
        with conn.cursor() as cur:
            cur.execute("""   
                    INSERT INTO hotel_booking(
                    room_id,
                    guest_id, 
                    datefrom
                    ) VALUES(
                    %s,
                    %s,
                    %s
                    )RETURNING id""", [
                    body['room'], 
                    body['guest'], 
                    body['datefrom']
            ])
            result= cur.fetchone()
        return{"msg": " Du har bokat ett rum!", "result": result}


        # Skapa rad i hotel_booking med sql INSERT INTO...
     

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True, ssl_context=(
        '/etc/letsencrypt/fullchain.pem', 
        '/etc/letsencrypt/privkey.pem'
    ))