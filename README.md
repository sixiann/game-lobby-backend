# Multiplayer game lobby

This is a simple backend system that manages game lobbies for a multiplayer game. The system allows players to create lobbies, join and leave lobbies, and start a game when all players are ready.

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- Python 3.6 or newer
- pip (Python package installer)

## Setup Instructions

Follow these steps to set up the project environment and install necessary dependencies.

1. **Clone the repository**

   Clone the project repository to your local machine.

   ```bash
   git clone https://github.com/sixiann/game-lobby-backend.git
   cd game-lobby-backend
2. **Run the setup script**

   ```bash
   ./bash.sh
3. **Run the server script**

    ```bash
   python server.py
4. **Run the test script**

    ```bash
   python main.py

## Design Decisions

### Data Structures:

- **lobbies**: A dictionary mapping lobby IDs to their details (players in the lobby, lobby details).
- **players**: A dictionary mapping player IDs to their current lobby ID (or `None` if not in any lobby).
- **current_lobby_id**: An integer counter used to generate unique lobby IDs.

### Player and Lobby Management:

- Each player is identified by a unique player ID. At startup, 20 dummy players are registered for testing.
- A lobby can contain a maximum number of players, specified by `max_players`. The default value is 5.
- When a lobby reaches the maximum number of players, the game starts automatically, removing all players from the lobby and deleting the lobby.



## API Endpoints

### GET `/get_lobbies`
- **Description:** Returns a list of all active lobbies and their details.
- **Response:** JSON object containing the lobby IDs and their details (player list, lobby details).


## WebSocket Events

### `create_lobby`
- **Data Required:**
  - `player_id`: The ID of the player creating the lobby.
  - `lobby_details`: Additional details about the lobby (e.g., game settings).
- **Behavior:** Creates a new lobby with the specified details and adds the creator to the lobby. Sends a message to the lobby indicating its creation.
- **Returns:** The details of the newly created lobby.

### `join_lobby`
- **Data Required:**
  - `player_id`: The ID of the player wanting to join a lobby.
  - `lobby_id`: The ID of the lobby the player wants to join.
- **Behavior:** Adds the player to the specified lobby if it exists and the player is not already in another lobby. Sends a message to the lobby indicating the player has joined. If the lobby reaches `max_players`, the game starts automatically.
- **Returns:** The details of the lobby the player joined.

### `leave_lobby`
- **Data Required:**
  - `player_id`: The ID of the player wanting to leave a lobby.
  - `lobby_id`: The ID of the lobby the player wants to leave.
- **Behavior:** Removes the player from the specified lobby. Sends a message to the lobby indicating the player has left. If the lobby is empty after the player leaves, it is deleted.
- **Returns:** The details of the lobby the player left.


## Interaction with the System

To interact with lobbies, the client must first establish a connection to the backend server using the `connect` method.
Then, implement an event handler on the client side to listen for messages from the server. This includes lobby notifications and any potential error messages.


### Creating a Lobby:
- A player creates a lobby by emitting a `create_lobby` event with their `player_id` and `lobby_details`.

### Joining a Lobby:
- A player joins an existing lobby by emitting a `join_lobby` event with their `player_id` and the `lobby_id` they wish to join.

### Leaving a Lobby:
- A player leaves a lobby by emitting a `leave_lobby` event with their `player_id` and the `lobby_id` they are in.

### Viewing Active Lobbies:
- To view all active lobbies, send a GET request to `/get_lobbies`.


## Test script

The script runs through several predefined test scenarios:

- **Valid Create, Join, Leave, and Reach Max Players:** Tests the normal operation of creating a lobby, players joining, one player leaving, and the lobby reaching maximum capacity, triggering the game to start.

- **Get All Lobbies:** Tests retrieving a list of all active lobbies.

- **Invalid Create Lobby Cases:** Tests creating a lobby with missing information or invalid data.

- **Invalid Join Lobby Cases:** Tests joining lobbies with missing or incorrect information.

- **Invalid Leave Lobby Cases:** Tests leaving lobbies with missing or incorrect information.

- **Delete Lobby When Empty:** Tests the automatic deletion of a lobby when the last player leaves.

The script outputs the results of each test case to the console, including any errors returned by the server and notifications of actions taken by simulated players in lobbies. 


## Additional Notes
- In-memory data structures are often preferred for real-time aspects of applications due to their speed and simplicity, which are crucial for operations such as players entering and leaving lobbies. This approach enables faster read and write operations compared to querying a database, thereby providing a smoother and more responsive user experience. While this choice simplifies development and testing by avoiding the overhead and complexity of database management, it's important to consider data persistence. In a production environment, a hybrid approach that uses in-memory structures for managing active state and a persistent storage solution like a database for long-term data storage and complex queries might be more appropriate. This ensures the benefits of speed and simplicity for real-time operations while also maintaining data durability and supporting scalability.
- It's assumed that if a client disconnects, they have the ability to reconnect and re-enter the same lobby. This distinction is why `leave_lobby` and `disconnect` are treated as separate actions. Disconnecting does not automatically remove a player from a lobby.
- For simplicity, `lobby_details` are assumed to be a string. However, this can be adapted to use a dictionary for more complex data structures,allowing for the inclusion of multiple parameters to define a lobby.
- The `current_lobby_id` counter and the use of simple integers for `lobby_id` and `player_id` are chosen to simplify testing and development. In a real-world scenario, a more robust method for ID generation would be necessary to ensure uniqueness across sessions and prevent collisions. Techniques such as UUIDs (Universally Unique Identifiers) or database auto-increment features could be employed for this purpose.
- Error handling is included for common scenarios such as missing data, invalid player IDs, players trying to join multiple lobbies, and attempting to join or leave non-existent lobbies.
- The automatic game start mechanism when a lobby is full simplifies flow and ensures games begin promptly.
