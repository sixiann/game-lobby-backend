import socketio
import threading
import time

base_url = 'http://localhost:5000'
# Function to simulate a client creating a lobby
def create_lobby(client, player_id, lobby_details):
    @client.event
    def connect():
        print(f"Client {player_id} connected to the server.")
        client.emit('create_lobby', {'player_id': player_id, 'lobby_details': lobby_details})

    @client.event
    def message(data):
        if 'message' in data:
            print(f"Message received by {player_id}: {data['message']}")

    client.connect(base_url)  # Adjust the URL to your server

# Function to simulate a client joining a lobby
def join_lobby(client, player_id, lobby_id):
    @client.event
    def connect():
        print(f"Client {player_id} connected to the server.")
        client.emit('join_lobby', {'player_id': player_id, 'lobby_id': lobby_id})

    @client.event
    def message(data):
        if 'message' in data:
            print(f"Message received by {player_id}: {data['message']}")

    client.connect(base_url)  # Adjust the URL to your server

# Function to simulate a client joining and leaving a lobby
def leave_lobby(client, player_id, lobby_id):
    @client.event
    def connect():
        print(f"Client {player_id} connected to the server and is attempting to leave the lobby {lobby_id}.")
        client.emit('join_lobby', {'player_id': player_id, 'lobby_id': lobby_id})
        client.emit('leave_lobby', {'player_id': player_id, 'lobby_id': lobby_id})

    @client.event
    def message(data):
        if 'message' in data:
            print(f"Message received by {player_id}: {data['message']}")

    client.connect(base_url)  # Adjust the URL to your server

# Initialize clients
client1 = socketio.Client()
client2 = socketio.Client()
client3 = socketio.Client()
client4 = socketio.Client()
client5 = socketio.Client()
client6 = socketio.Client()



# Start the first client to create a lobby
threading.Thread(target=create_lobby, args=(client1, '1', 'Example Lobby Details')).start()

# Give the server some time to process the creation
time.sleep(2)

# Start the second client to join the lobby
threading.Thread(target=join_lobby, args=(client2, '2', '1')).start()  

# Give the server some time to process the join
time.sleep(2)

# Use the third client to join and leave the lobby
threading.Thread(target=leave_lobby, args=(client3, '3', '1')).start() 
time.sleep(2)

# Start fourth, fifth, and sixth clients to join lobby to reach max players and start game
threading.Thread(target=join_lobby, args=(client4, '4', '1')).start() 
time.sleep(2)

threading.Thread(target=join_lobby, args=(client5, '5', '1')).start() 
time.sleep(2)

threading.Thread(target=join_lobby, args=(client6, '6', '1')).start() 
time.sleep(2)


