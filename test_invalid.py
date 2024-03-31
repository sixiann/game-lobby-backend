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
def leave_lobby(client, data):
    @client.event
    def connect():
        # client.emit('join_lobby', data)
        client.emit('leave_lobby', data)


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



def run_test(case, case_type):
    client = socketio.Client()

    # Setup event handlers before connecting

    if case_type == 'create':
        create_lobby(client, case)
    elif case_type == 'join':
        join_lobby(client, case)
    elif case_type == 'leave':
        leave_lobby(client, case)

    # Connect, wait for operations to complete, then disconnect
    client.connect(base_url)
    time.sleep(2)  # Adjust the sleep time as needed for your operations to complete
    client.disconnect()


def run_grouped_tests(test_cases, case_type):
    if case_type == 'create':
        print("\n<---------Testing invalid lobby creations--------->")
    elif case_type == 'join':
        print("\n<---------Testing invalid lobby joins--------->")
    elif case_type == 'leave':
        print("\n<---------Testing invalid lobby leaves--------->")

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

#2. Test invalid join and leave lobbies
invalid_join_leave_cases = [
    {'lobby_id': '1'},                                               # missing player_id 
    {'player_id': '1'},                                             # missing lobby_id
    {'player_id': '100', 'lobby_id': '1'},                          # invalid player_id 
    {'player_id': '1', 'lobby_id': '100'},                          # invalid lobby_id 
]

# Run grouped invalid tests
run_grouped_tests(invalid_create_cases, 'create')
run_grouped_tests(invalid_join_leave_cases, 'join')
run_grouped_tests(invalid_join_leave_cases, 'leave')
