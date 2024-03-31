import socketio
import threading
import time

base_url = 'http://localhost:5000'

# Function to test a client creating a lobby
def create_lobby(client, data):
    @client.event
    def connect():
        client.emit('create_lobby', data)

    @client.event
    def message(data):
        if 'error' in data:
            print("Error:", data['error'])
        else:
            print(f"Notif received by {data['player_id']}: {data['message']}")
    try:
        client.wait()
    except KeyboardInterrupt:
        print("Script interrupted by user.")
    

# Function to simulate a client joining a lobby
def join_lobby(client, data):
    @client.event
    def connect():
        client.emit('join_lobby', data)

    @client.event
    def message(data):
        if 'error' in data:
            print("Error:", data['error'])
        else:
            print(f"Notif received by {data['player_id']}: {data['message']}")
    
    try:
        client.wait()
    except KeyboardInterrupt:
        print("Script interrupted by user.")

    
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



def run_test(case, case_type):
    client = socketio.Client()

    # Setup event handlers before connecting

    if case_type == 'create':
        create_lobby(client, case)
    elif case_type == 'join':
        join_lobby(client, case)

    # Connect, wait for operations to complete, then disconnect
    client.connect(base_url)
    time.sleep(2)  # Adjust the sleep time as needed for your operations to complete
    client.disconnect()


def run_grouped_tests(test_cases, case_type):
    if case_type == 'create':
        print("\n<---------Testing invalid lobby creations--------->")
    elif case_type == 'join':
        print("\n<---------Testing invalid lobby joins--------->")
    
    # Initialize a list to keep track of threads
    threads = []

    # Create a thread for each test case
    for case in test_cases:
        thread = threading.Thread(target=run_test, args=(case, case_type))
        threads.append(thread)

    # Start all threads in this group
    for thread in threads:
        thread.start()

    #Wait for all threads in this group to complete
    for thread in threads:
        thread.join()

#1. Test invalid create lobbies 
invalid_create_cases = [
    {'lobby_details': 'Example Lobby Details'},                     # missing player_id 
    {'player_id': '1'},                                             # missing lobby_details
    {'player_id': '100', 'lobby_details': 'Example Lobby Details'}, # invalid player_id 
]
#2. Test invalid join lobbies
invalid_join_cases = [
    {'lobby_id': '1'},                                               # missing player_id 
    {'player_id': '1'},                                             # missing lobby_id
    {'player_id': '100', 'lobby_id': '1'},                          # invalid player_id 
    {'player_id': '1', 'lobby_id': '100'},                          # invalid lobby_id 
]

# Run grouped tests
run_grouped_tests(invalid_create_cases, 'create')
run_grouped_tests(invalid_join_cases, 'join')








# # Run invalid join test cases
# for case in invalid_create_cases:
#     threading.Thread(target=run_test, args=(case, 'join')).start()




# Initialize clients
client1 = socketio.Client()
client2 = socketio.Client()
client3 = socketio.Client()
client4 = socketio.Client()
client5 = socketio.Client()


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
