from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_socketio import join_room, leave_room, send, SocketIO


app = Flask(__name__)
socketio = SocketIO(app)
app.config["SECRET_KEY"] = "secret"


lobbies = {}
current_lobby_id = 1
max_players = 5

@socketio.on('create_lobby')
def create_lobby(data):
    global current_lobby_id 

    player_id = data['player_id']
    lobby_details = data['lobby_details']

    lobby_id = str(current_lobby_id)
    lobbies[lobby_id] = {
        "players": [player_id],
        "lobby_details": lobby_details,
        "messages": []
    }
    current_lobby_id += 1

    join_room(lobby_id)
    send({"message": f"{player_id} has created a lobby"}, to=lobby_id)
    return {"lobby_id": lobby_id, 
            "lobby_details": lobbies[lobby_id]['lobby_details'], 
            "messages": lobbies[lobby_id]["messages"]}

@socketio.on('join_lobby')
def join_lobby(data):
    player_id = data['player_id']
    lobby_id = data['lobby_id']

    join_room(lobby_id)
    send({"message": f"{player_id} has entered the lobby"}, to=lobby_id)
    lobbies[lobby_id]['players'].append(player_id)

    if len(lobbies[lobby_id]['players']) >= max_players:
        send({"message": "Max players reached. Game is beginning"}, to=lobby_id)
        del lobbies[lobby_id] 
        leave_room(lobby_id)
    
    return {"lobby_id": lobby_id, 
            "lobby_details": lobbies[lobby_id]['lobby_details'], 
            "messages": lobbies[lobby_id]["messages"]}

#leaving lobby
@socketio.on("leave_lobby")
def leave_lobby(data):
    player_id = data['player_id']
    lobby_id = data['lobby_id']

    leave_room(lobby_id)
    send({"message": f"{player_id} has left the lobby"}, to=lobby_id)


    if lobby_id in lobbies:
        if player_id in lobbies[lobby_id]['players']:
            lobbies[lobby_id]['players'].remove(player_id)
            if len(lobbies[lobby_id]['players']) <= 0:
                del lobbies[lobby_id]
    

#list all lobbies
@app.route('/get_lobbies', methods=['GET'])
def get_lobbies():
    return jsonify(lobbies), 200



if __name__ == "__main__":
    socketio.run(app, debug=True)





