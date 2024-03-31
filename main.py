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

# Initialize a list to keep track of clients
clients = []

# Create a function for each action
actions = [
    ('create_lobby', {'player_id': '1', 'lobby_details': 'my first lobby'}, server_url),
    ('join_lobby', {'player_id': '2', 'lobby_id': '1'}, server_url),
    ('leave_lobby', {'player_id': '3', 'lobby_id': '1'}, server_url),
    ('join_lobby', {'player_id': '4', 'lobby_id': '1'}, server_url),
    ('join_lobby', {'player_id': '5', 'lobby_id': '1'}, server_url),
    ('join_lobby', {'player_id': '6', 'lobby_id': '1'}, server_url),
]

for action, data, url in actions:
    client = socketio.Client()
    clients.append(client)
    thread = threading.Thread(target=perform_socketio_action, args=(client, action, data, url))
    thread.start()
    time.sleep(2)  


print("\nAll actions completed. Exiting script.")
for client in clients:
    client.disconnect()

