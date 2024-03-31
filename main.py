import socketio
import threading
import time

server_url = 'http://localhost:5000'

def perform_socketio_action(client, action, data, server_url):
    @client.event
    def connect():
        print(f"\nTesting {action}...")
        if action != 'leave_lobby':
            client.emit(action, data)
        else:
            client.emit('join_lobby', data)
            time.sleep(1)
            client.emit('leave_lobby', data)

    @client.event
    def message(response_data):
        if 'error' in response_data:
            print("Error:", response_data['error'])
        elif 'message' in response_data:
            print(f"Notif received by {data['player_id']}: {response_data['message']}")
    
    client.connect(server_url)

    try:
        client.wait()
    except KeyboardInterrupt:
        print("Script interrupted by user.")


def run_tests(actions): 
    clients = []
    for action, data, url in actions:
        client = socketio.Client()
        clients.append(client)
        thread = threading.Thread(target=perform_socketio_action, args=(client, action, data, url))
        thread.start()
        time.sleep(2)
    for client in clients:
        client.disconnect()


#1. Testing valid create, join, leave, and reaching max players
print("\n" + " Testing valid create, join, leave, and reach max players ".center(80, '-'))
actions = [
    ('create_lobby', {'player_id': '1', 'lobby_details': 'my first lobby'}, server_url),          #1st player creates lobby
    ('join_lobby', {'player_id': '2', 'lobby_id': '1'}, server_url),                              #2nd player joins lobby
    ('leave_lobby', {'player_id': '3', 'lobby_id': '1'}, server_url),                             #3rd player joins and leaves lobby
    ('join_lobby', {'player_id': '4', 'lobby_id': '1'}, server_url),                              #4th player joins lobby
    ('join_lobby', {'player_id': '5', 'lobby_id': '1'}, server_url),                              #5th player joins lobby
    ('join_lobby', {'player_id': '6', 'lobby_id': '1'}, server_url),                              #6th player joins lobby, reached max players
]
run_tests(actions)
print("\n" + " Testing valid cases complete ".center(80, '-') + "\n")




#2. Testing invalid create lobbies
print("\n" + " Testing invalid create lobby cases".center(80, '-'))
invalid_create_actions = [
    ('create_lobby', {'lobby_details': 'Example Lobby Details'}, server_url),                                           # missing player_id 
    ('create_lobby', {'player_id': '1'}, server_url),                                                                    # missing lobby_details
    ('create_lobby', {'player_id': '100', 'lobby_details': 'Example Lobby Details'}, server_url),                         # invalid player_id 
]
run_tests(invalid_create_actions)
print("\n" + " Testing invalid create lobby cases complete ".center(80, '-')  + "\n")




#3. Testing invalid join lobbies
print("\n" + " Testing invalid join lobby ".center(80, '-'))
invalid_join_actions = [
    ('join_lobby', {'lobby_id': '1'}, server_url),                                                                      # missing player_id 
    ('join_lobby', {'player_id': '1'}, server_url),                                                                    # missing lobby_id
    ('join_lobby', {'player_id': '100', 'lobby_id': '1'}, server_url),                                                 # invalid player_id
    ('join_lobby', {'player_id': '1', 'lobby_id': '100'}, server_url),                                                 # invalid lobby_id 
]
run_tests(invalid_join_actions)
print("\n" + " Testing invalid join lobby cases complete ".center(80, '-')  + "\n")



#3. Testing invalid leave lobbies
print("\n" + " Testing invalid leave lobby ".center(80, '-'))
invalid_leave_actions = [
    ('leave_lobby', {'lobby_id': '1'}, server_url),                                                                      # missing player_id 
    ('leave_lobby', {'player_id': '1'}, server_url),                                                                    # missing lobby_id
    ('leave_lobby', {'player_id': '100', 'lobby_id': '1'}, server_url),                                                 # invalid player_id
    ('leave_lobby', {'player_id': '1', 'lobby_id': '100'}, server_url),                                                 # invalid lobby_id 
]
run_tests(invalid_leave_actions)
print("\n" + " Testing invalid leave lobby cases complete ".center(80, '-'))
