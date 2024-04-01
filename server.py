from flask import Flask, request, jsonify
from flask_socketio import join_room, leave_room, send, SocketIO

# #TODO: 
# 1. add last few invalid create, join and leave test cases 
# 2. documentation 
# 3. requirements file   

app = Flask(__name__)
socketio = SocketIO(app)
app.config["SECRET_KEY"] = "secret"

#Data structures to store data  
lobbies = {} #maps lobbies to the list of players
players = {} #maps players to the lobby they are in, None if not in lobby
current_lobby_id = 1 #Sets the lobby_id of new lobbies. Using simple integer for easier testing


#insert 20 valid registered players for dummy data, initially not in lobby
for i in range(20):
    players[str(i)] = None

#maximum number of players per lobby - change if needed
max_players = 5


def start_game(lobby_id): 
    send({"message": f"Max {max_players} players reached. Game is beginning"}, to=lobby_id)
    #remove everyone from the lobby 
    for player_id in lobbies[lobby_id]['players']:
        players[player_id] = None
    
    #delete the lobby after starting game
    del lobbies[lobby_id]

    #make everyone leave the socketio room
    leave_room(lobby_id) 

#socket for create lobby 
@socketio.on('create_lobby')
def create_lobby(data):
    #declare global to modify global variables and not local variables
    global lobbies
    global players
    global current_lobby_id 

    #check if player_id is in data
    if "player_id" not in data:
        send({"error": "Missing required parameter: player_id"}, to=request.sid)
        return

    #check if lobby_details is in data
    if "lobby_details" not in data:
        send({"error": "Missing required parameter: lobby_details"}, to=request.sid)
        return

    #extract player_id and lobby_details and ensure correct formatting
    player_id = str(data['player_id'])
    lobby_details = str(data['lobby_details'])

    #check if player_id is a valid registered player
    if player_id not in players: 
        send({"error": "Invalid player_id"}, to=request.sid)
        return
    
    #check if player_id is already in a lobby 
    if players[player_id]: 
        send({"error": f"Player {player_id} is already in lobby {players[player_id]}"}, to=request.sid)
        return

    #create a new lobby with current_lobby_id
    lobby_id = str(current_lobby_id)
    lobbies[lobby_id] = {
        "players": [player_id], #initialize list of players with player_id who created it
        "lobby_details": lobby_details,
    }

    #associate player with lobby
    players[player_id] = lobby_id

    #increment current_lobby_id for the next lobby
    current_lobby_id += 1

    #join the socketio room associated with lobby_id
    join_room(lobby_id)

    #send message that player_id has created a lobby to lobby_id 
    send({"message": f"Player {player_id} has created lobby {lobby_id}"}, to=lobby_id)

    #return information to the client #modify this based on frontend's needs
    return lobbies[lobby_id]


#socket for joining lobby
@socketio.on('join_lobby')
def join_lobby(data):
    #declare global to modify global variables and not local variables
    global lobbies
    global players


    #check if player_id is in data
    if "player_id" not in data:
        send({"error": "Missing required parameter: player_id"}, to=request.sid)
        return

    #check if lobby_id is in data
    if "lobby_id" not in data:
        send({"error": "Missing required parameter: lobby_id"}, to=request.sid)
        return
    
    #extract player_id and lobby_id and ensure correct formatting
    player_id = str(data['player_id'])
    lobby_id = str(data['lobby_id'])

    #check if player_id is a valid registered player
    if player_id not in players: 
        send({"error": "Invalid player_id"}, to=request.sid)
        return
    
    #check if lobby_id is a valid existing lobby
    if lobby_id not in lobbies:
        send({"error": "Invalid lobby_id, does not exist"}, to=request.sid)
        return

    #check if player_id is already in a lobby 
    if players[player_id]: 
        send({"error": f"Player {player_id} is already in lobby {players[player_id]}"}, to=request.sid)
        return

    #join the socketio room associated with lobby_id
    join_room(lobby_id)

    #send message that player_id has joined lobby_id to lobby_id 
    send({"message": f"Player {player_id} has entered the lobby"}, to=lobby_id)

    #modify lobbies and players to include the new player_id
    lobbies[lobby_id]['players'].append(player_id)
    players[player_id] = lobby_id

    #check if number of players exceeds max players and start game if True
    if len(lobbies[lobby_id]['players']) >= max_players:
        start_game(lobby_id)
        return 
    
    #return information to the client #modify this based on frontend's needs
    return lobbies[lobby_id]

#leaving lobby
@socketio.on("leave_lobby")
def leave_lobby(data):
    #declare global to modify global variables and not local variables
    global lobbies
    global players

    #check if player_id is in data
    if "player_id" not in data:
        send({"error": "Missing required parameter: player_id"}, to=request.sid)
        return

    #check if lobby_id is in data
    if "lobby_id" not in data:
        send({"error": "Missing required parameter: lobby_id"}, to=request.sid)
        return
    
    #extract player_id and lobby_id and ensure correct formatting
    player_id = str(data['player_id'])
    lobby_id = str(data['lobby_id'])

    #check if player_id is a valid registered player
    if player_id not in players: 
        send({"error": "Invalid player_id"}, to=request.sid)
        return
    
    #check if lobby_id is a valid existing lobby
    if lobby_id not in lobbies:
        send({"error": "Invalid lobby_id, does not exist"}, to=request.sid)
        return

    #check if player_id is not in this lobby
    if players[player_id] != lobby_id: 
        
        send({"error": f"Player {player_id} is not in lobby {lobby_id}"}, to=request.sid)
        return

    #send message that player_id has left lobby_id to lobby_id 
    send({"message": f"Player {player_id} has left the lobby"}, to=lobby_id)

    #make client leave the socketio room associated with lobby_id
    leave_room(lobby_id)

    #modify lobbies and players to remove the player_id
    lobbies[lobby_id]['players'].remove(player_id)
    players[player_id] = None 

    #delete the lobby if there are no more players
    if len(lobbies[lobby_id]['players']) <= 0:
        del lobbies[lobby_id]
    

#list all lobbies
@app.route('/get_lobbies', methods=['GET'])
def get_lobbies():
    return jsonify(lobbies), 200



if __name__ == "__main__":
    socketio.run(app, debug=True)





