from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_socketio import join_room, leave_room, send, SocketIO


app = Flask(__name__)
socketio = SocketIO(app)
app.config["SECRET_KEY"] = "secret"


lobbies = {}
current_lobby_id = 0
max_players = 10

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/create_lobby", methods = ['POST'])
def create_lobby():
    global current_lobby_id

    json_data = request.get_json()

    player_id = json_data['player_id']
    lobby_details = json_data['lobby_details']

    lobby_id = str(current_lobby_id)
    lobbies[lobby_id] = {
        "players": 0,
        "lobby_details": lobby_details,
        "messages": []
    }
    current_lobby_id += 1
 
    session["lobby_id"] = lobby_id
    session["player_id"] = player_id 

    # return jsonify({'lobby_id': lobby_id}), 201
    # return render_template("lobby.html", code=lobby_id, messages=lobbies[lobby_id]["messages"])
    # return jsonify(data=lobbies)
    return jsonify({'redirect_url': url_for('lobby', code=lobby_id, messages=lobbies[lobby_id]["messages"])}), 201


@app.route("/lobby")
def lobby():
    lobby_id = session.get("lobby_id")
    if lobby_id is None or session.get("player_id") is None or lobby_id not in lobbies:
        print("here")
        return redirect(url_for("home"))

    return render_template("lobby.html", code=lobby_id, messages=lobbies[lobby_id]["messages"])

@app.route("/join_lobby", methods = ['POST'])
def join_lobby():
    json_data = request.get_json()

    player_id = json_data['player_id']
    lobby_id = json_data['lobby_id']

    session["lobby_id"] = lobby_id
    session["player_id"] = player_id 

    # return jsonify({'lobby_id': lobby_id}), 201
    return jsonify({'redirect_url': url_for('lobby', code=lobby_id, messages=lobbies[lobby_id]["messages"])}), 201



#list all lobbies
@app.route('/get_lobbies', methods=['GET'])
def get_lobbies():
    return jsonify(lobbies), 200


@socketio.on("message")
def message(data):
    lobby_id = session.get("lobby_id")
    if lobby_id not in lobbies:
        return 
    
    content = {
        "player_id": session.get("player_id"),
        "message": data["data"]
    }
    send(content, to=lobby_id)
    lobbies[lobby_id]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect():
    lobby_id = session.get("lobby_id")
    player_id = session.get("player_id")

    join_room(lobby_id)
    send({"message": f"{player_id} has entered the lobby"}, to=lobby_id)
    lobbies[lobby_id]['players'] += 1

    if lobbies[lobby_id]['players'] >= max_players:
        send({"message": "Game is beginning"}, to=lobby_id)
        del lobbies[lobby_id] 

@socketio.on("disconnect")
def disconnect():
    lobby_id = session.get("lobby_id")
    player_id = session.get("player_id")

    leave_room(lobby_id)

    if lobby_id in lobbies:
        lobbies[lobby_id]['players'] -= 1
        if lobbies[lobby_id]['players'] <= 0:
            del lobbies[lobby_id] 
    
    send({"message": f"{player_id} has left the lobby"}, to=lobby_id)


if __name__ == "__main__":
    socketio.run(app, debug=True)





