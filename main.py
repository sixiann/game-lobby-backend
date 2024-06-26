import socketio
import requests
import threading
import time

server_url = "http://localhost:5000"


# function to run each individual socketio action
def perform_socketio_action(client, action, data, server_url):
    # Event handler for establishing connection
    @client.event
    def connect():
        print(f"\nTesting {action}...")

        # emit the specified action
        client.emit(action, data)

    # Event handler for receiving messages from the server
    @client.event
    def message(response_data):
        # Check for errors in the response and print if present
        if "error" in response_data:
            print("Error:", response_data["error"])
        # Otherwise, print the notification received
        elif "message" in response_data:
            print(f"Notif received by {data['player_id']}: {response_data['message']}")

    # Connect to the server
    client.connect(server_url)

    try:
        # Wait for server events and handle them. Need this to receive lobby notifications
        client.wait()
    except KeyboardInterrupt:
        # Handle script interruption by the user
        print("Script interrupted by user.")


# run test cases
def run_tests(actions):
    clients = []  # Store client instances to disconnect later

    # Iterate over each action to be tested
    for action, data, url in actions:
        # Initialize a new client for each action
        client = socketio.Client()
        clients.append(client)
        # Create a new thread for each client to perform its action, start the thread
        thread = threading.Thread(
            target=perform_socketio_action, args=(client, action, data, url)
        )
        thread.start()
        # pause between actions for clarity
        time.sleep(2)

    # After all actions are completed, disconnect each client
    for client in clients:
        client.disconnect()


if __name__ == "__main__":

    #1. Test valid create lobby
    print("\n" + " Testing create lobbies ".center(80, "-"))
    create_actions = [
        (
            "create_lobby",
            {"player_id": "1", "lobby_details": "my first lobby"},
            server_url,
        ),  # player 1 creates lobby 1
        (
            "create_lobby",
            {"player_id": "2", "lobby_details": "another lobby"},
            server_url,
        ),  # player 2 creates lobby 2
        (
            "create_lobby",
            {"player_id": "3", "lobby_details": "3rd lobby"},
            server_url,
        ),  # player 3 creates lobby 3
    ]
    run_tests(create_actions)
    print("\n" + " Testing create lobbies complete ".center(80, "-"))


    #2. Test valid join lobby, reach max players, start game
    print("\n" + " Testing valid join, and start game ".center(80, "-"))
    actions = [
        (
            "join_lobby",
            {"player_id": "4", "lobby_id": "1"},
            server_url,
        ),  # player 4 joins lobby 1
        (
            "join_lobby",
            {"player_id": "5", "lobby_id": "1"},
            server_url,
        ),  # player 5 joins lobby 1
        (
            "join_lobby",
            {"player_id": "6", "lobby_id": "1"},
            server_url,
        ),  # player 6 joins lobby 1
        (
            "join_lobby",
            {"player_id": "7", "lobby_id": "1"},
            server_url,
        ),  # player 7 joins lobby, reached max players
        # game starts and lobby 1 is deleted
    ]
    run_tests(actions)
    print("\n" + " Testing valid join, and start game complete ".center(80, "-") + "\n")


    #3. Testing get_lobbies
    print("\n" + " Testing get all lobbies ".center(80, "-"))
    response = requests.get(f"{server_url}/get_lobbies")
    print("\nResponse from /get_lobbies:")
    print(response.status_code, response.json())
    print("\n" + " Testing get all lobbies complete ".center(80, "-"))


    #4. Testing invalid create lobbies
    print("\n" + " Testing invalid create lobby cases".center(80, "-"))
    invalid_create_actions = [
        (
            "create_lobby",
            {"lobby_details": "Example Lobby Details"},
            server_url,
        ),  # missing player_id
        ("create_lobby", {"player_id": "1"}, server_url),  # missing lobby_details
        (
            "create_lobby",
            {"player_id": "100", "lobby_details": "Example Lobby Details"},
            server_url,
        ),  # invalid player_id
        (
            "create_lobby",
            {"player_id": "2", "lobby_details": "my second lobby"},
            server_url,
        ),  # player 2 tries to create another lobby
    ]
    run_tests(invalid_create_actions)
    print("\n" + " Testing invalid create lobby cases complete ".center(80, "-") + "\n")




    # 5. Testing invalid join lobbies
    print("\n" + " Testing invalid join lobby ".center(80, "-"))
    invalid_join_actions = [
        ("join_lobby", {"lobby_id": "1"}, server_url),  # missing player_id
        ("join_lobby", {"player_id": "1"}, server_url),  # missing lobby_id
        (
            "join_lobby",
            {"player_id": "100", "lobby_id": "2"},
            server_url,
        ),  # invalid player_id
        (
            "join_lobby",
            {"player_id": "1", "lobby_id": "100"},
            server_url,
        ),  # invalid lobby_id
        (
            "join_lobby",
            {"player_id": "2", "lobby_id": "3"},
            server_url,
        ),  # player 2 tries to join lobby 3
    ]
    run_tests(invalid_join_actions)
    print("\n" + " Testing invalid join lobby cases complete ".center(80, "-") + "\n")




    # 6. Testing invalid leave lobbies
    print("\n" + " Testing invalid leave lobby ".center(80, "-"))
    invalid_leave_actions = [
        ("leave_lobby", {"lobby_id": "1"}, server_url),  # missing player_id
        ("leave_lobby", {"player_id": "1"}, server_url),  # missing lobby_id
        (
            "leave_lobby",
            {"player_id": "100", "lobby_id": "1"},
            server_url,
        ),  # invalid player_id
        (
            "leave_lobby",
            {"player_id": "1", "lobby_id": "100"},
            server_url,
        ),  # invalid lobby_id
        (
            "leave_lobby",
            {"player_id": "2", "lobby_id": "3"},
            server_url,
        ),  # player 2 tries to leave lobby 3
    ]
    run_tests(invalid_leave_actions)
    print("\n" + " Testing invalid leave lobby cases complete ".center(80, "-") + "\n")




    # 7. Testing leave_lobby and delete lobby when empty
    print("\n" + " Testing leave lobby and delete lobby when empty ".center(80, "-"))
    delete_actions = [
        #adding another player to the lobby to show leave_lobby notifications
        ("join_lobby", {"player_id": "4", "lobby_id": "2"}, server_url),  
        ("join_lobby", {"player_id": "5", "lobby_id": "3"}, server_url),  
        #everyone leaves both lobbies
        ("leave_lobby", {"player_id": "2", "lobby_id": "2"}, server_url),
        ("leave_lobby", {"player_id": "3", "lobby_id": "3"}, server_url),
        ("leave_lobby", {"player_id": "4", "lobby_id": "2"}, server_url),  
        ("leave_lobby", {"player_id": "5", "lobby_id": "3"}, server_url), 
    ]  # now both lobby 2 and 3 are empty and deleted
    run_tests(delete_actions)
    response = requests.get(f"{server_url}/get_lobbies")
    print(
        "\nResponse from /get_lobbies:"
    )  # now our get request shows we have no lobbies left
    print(response.status_code, response.json())
    print(
        "\n"
        + " Testing leave lobby and delete lobby when empty complete ".center(80, "-")
    )
