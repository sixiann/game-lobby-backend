import socketio
import threading
import time

base_url = 'http://localhost:5000'

# Function to test a client creating a lobby
def create_lobby(client, data):
    @client.event
    def connect():
        print(f"Client connected to the server.")
        client.emit('create_lobby', data)

    @client.event
    def message(data):
        if 'error' in data:
            print("Error:", data['error'])
        else:
            print(f"Message received by {player_id}: {data['message']}")
    
    client.connect(base_url)

    try:
        client.wait()
    except KeyboardInterrupt:
        print("Script interrupted by user.")
    

# Function to simulate a client joining a lobby
def join_lobby(client, player_id, lobby_id):
    @client.event
    def connect():
        print(f"Client {player_id} connected to the server.")
        client.emit('join_lobby', {'player_id': player_id, 'lobby_id': lobby_id})

    @client.event
    def message(data):
        print(f"Message received by {player_id}: {data['message']}")
    
    client.connect(base_url)

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
    
    client.connect(base_url)
    try:
        client.wait()
    except KeyboardInterrupt:
        print("Script interrupted by user.")

# Initialize clients
client1 = socketio.Client()
client2 = socketio.Client()
client3 = socketio.Client()
client4 = socketio.Client()
client5 = socketio.Client()


#1. Test invalid create lobbies 
print("<---------Testing invalid lobby creations--------->")
invalid_cases = [
    {'lobby_details': 'Example Lobby Details'},                     # missing player_id 
    {'player_id': '1'},                                             # missing lobby_details
    {'player_id': '100', 'lobby_details': 'Example Lobby Details'}, # invalid player_id 
]

def run_test(case):
    client = socketio.Client()

    # Setup event handlers before connecting
    create_lobby(client, case)

    # Connect, wait for operations to complete, then disconnect
    client.connect(base_url)
    time.sleep(2)  # Adjust the sleep time as needed for your operations to complete
    client.disconnect()

# Create a thread for each test case
for case in invalid_cases:
    threading.Thread(target=run_test, args=(case,)).start()

# for case in invalid_cases:
#     test_client = socketio.Client()
#     threading.Thread(target=create_lobby, args=(test_client, case, False)).start()
#     test_client.disconnect()
# threading.Thread(target=create_lobby, args=(client1, {'player_id': 'player123', 'lobby_details': 'Example Lobby Details'})).start() #invalid player_id
# threading.Thread(target=create_lobby, args=(client1, '25', 'Example Lobby Details')).start() #invalid player_id






# # Start the first client to create a lobby
# threading.Thread(target=create_lobby, args=(client1, '1', 'Example Lobby Details')).start()

# # Give the server some time to process the creation
# time.sleep(2)

# # Start the second client to join the lobby
# threading.Thread(target=join_lobby, args=(client2, '2', '1')).start()  # Assuming '1' is the lobby_id

# # Give the server some time to process the join
# time.sleep(2)

# # Use the second client to leave the lobby
# threading.Thread(target=leave_lobby, args=(client3, '3', '1')).start()  # Assuming '1' is the lobby_id

# time.sleep(2)
