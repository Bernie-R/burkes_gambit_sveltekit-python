import json
from game import GameRoom
import random
import uuid
import websockets

rooms = {}
CONNECTIONS = {}

def new_game_id() -> str:
    global rooms
    id = str(uuid.uuid4())[:4]
    return new_game_id() if id in rooms else id

async def broadcast_to_room(msg_type, game_room_id, message):
    """Send a message to all players in a game room."""
    game_room = rooms[game_room_id]
    for player_id in game_room.get_lobby().get("player_id_list"):
        await message_user(msg_type, player_id, message)

async def message_user(msg_type ,user_id, message):
    """Send a message to a specific user."""
    print("message sent to", user_id)
    websocket = CONNECTIONS.get(user_id)
    if not websocket:
        print(f"User {user_id} is not connected.")
        return

    try:
        message["user_id"] = user_id
        message["type"] = msg_type
        message = json.dumps(message)
        
        await websocket.send(message)

    except websockets.ConnectionClosed:
        print(f"Connection with user {user_id} was closed.")
        del CONNECTIONS[user_id]


async def handle_connection(websocket, path):
    global rooms

    async for message in websocket:
        print(f"Received message: {message}")

        message = json.loads(message)

        match message["type"]:
            case "createServer":
                game_room = GameRoom(new_game_id())
                player = game_room.add_player(message["content"], is_admin = True)
                CONNECTIONS[player.id] = websocket
                rooms[game_room.id] = game_room
                await message_user(message["type"], player.id, game_room.get_game_state(player))

            case "joinRoom":
                data = message["content"]
                player_name = data["playerName"]
                room_id = data["roomName"]

                if room_id not in rooms:
                    print("ERROR: wrong room_id")
                    await message_user(user_id, "False")
                    continues

                game_room = rooms[room_id]
                player = game_room.add_player(player_name)
                CONNECTIONS[player.id] = websocket
                # Send a message to all players in the room about the new player joining
                join_message = game_room.get_lobby()
                await broadcast_to_room(message["type"], game_room.id, join_message)

            case "lobbyUpdate":
                data = message["content"]
                room_id = data["roomName"]
                user_id = data["user_id"]
                
                if room_id not in rooms:
                    print("ERROR: wrong room_id")
                    await websocket.send("False")
                    return

                game_room = rooms[room_id]
                await message_user(message["type"], user_id, game_room.get_lobby())
                return

            case "gameStart":
                room_id = message["content"]
                game_room = rooms[room_id]
                game_room.start_game()
                await broadcast_to_room(message["type"], game_room.id, {})
                return

            case "reconnect":
                if message["content"]:
                    CONNECTIONS[message.get("content").get("user_id")] = websocket
