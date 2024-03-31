import socketio
import threading
import time

# Function to simulate a client creating a lobby
def create_lobby(client, player_id, lobby_details):
    @client.event
    def connect():
        print(f"Client {player_id} connected to the server.")
        client.emit('create_lobby', {'player_id': player_id, 'lobby_details': lobby_details})

    @client.event
    def message(data):
        print(f"Message received by {player_id}: {data['message']}")
    
    client.connect('http://localhost:5000')  # Adjust the URL to your server

# Function to simulate a client joining a lobby
def join_lobby(client, player_id, lobby_id):
    @client.event
    def connect():
        print(f"Client {player_id} connected to the server.")
        client.emit('join_lobby', {'player_id': player_id, 'lobby_id': lobby_id})

    @client.event
    def message(data):
        print(f"Message received by {player_id}: {data['message']}")
    
    client.connect('http://localhost:5000')  # Adjust the URL to your server

# Function to simulate a client leaving a lobby
def leave_lobby(client, player_id, lobby_id):
    @client.event
    def connect():
        print(f"Client {player_id} connected to the server and is attempting to leave the lobby {lobby_id}.")
        client.emit('join_lobby', {'player_id': player_id, 'lobby_id': lobby_id})
        client.emit('leave_lobby', {'player_id': player_id, 'lobby_id': lobby_id})

    @client.event
    def message(data):
        print(f"Message received by {player_id}: {data['message']}")
    
    client.connect('http://localhost:5000')  # Adjust the URL to your server
    try:
        client.wait()
    except KeyboardInterrupt:
        print("Script interrupted by user.")

# Initialize clients
client1 = socketio.Client()
client2 = socketio.Client()
client3 = socketio.Client()

# Start the first client to create a lobby
threading.Thread(target=create_lobby, args=(client1, 'player1', 'Example Lobby Details')).start()

# Give the server some time to process the creation
time.sleep(2)

# Start the second client to join the lobby
threading.Thread(target=join_lobby, args=(client2, 'player2', '1')).start()  # Assuming '1' is the lobby_id

# Give the server some time to process the join
time.sleep(2)

# Use the second client to leave the lobby
threading.Thread(target=leave_lobby, args=(client3, 'player3', '1')).start()  # Assuming '1' is the lobby_id

time.sleep(2)


# import socketio

# # Create a Socket.IO client
# sio = socketio.Client()

# @sio.event
# def connect():
#     print("I'm connected to the server.")

# @sio.event
# def connect_error(data):
#     print("The connection failed!")

# @sio.event
# def disconnect():
#     print("I'm disconnected from the server.")

# @sio.event
# def message(data):
#     print("Real Time Message received:", data['message'])

# # Connect to the Socket.IO server
# sio.connect('http://localhost:5000')  # Update with your actual server URL
# #
# def test_create_lobby(data):
#     sio.emit("create_lobby", data)
# # Example data to send when creating or joining a lobby
# data = {
#   "player_id": "player123",
#   "lobby_details": "Example Lobby Details"  # Only needed if creating a new lobby
# }

# # Emit the 'create_or_join_lobby' event to the server with the data
# sio.emit("create_lobby", data)

# # Keep the script running to listen for responses
# try:
#     sio.wait()
# except KeyboardInterrupt:
#     print("Script interrupted by user.")


# # // const socket = io.connect();

# # // // Example data to send when creating or joining a lobby
# # // const data = {
# # //   player_id: "player123",
# # //   lobby_details: "Example Lobby Details"  // Only needed if creating a new lobby
# # // };

# # // socket.emit("create_lobby", data);

# # // // Listen for messages
# # // socket.on("message", function(data) {
# # //   console.log(data.message);
# # // });
