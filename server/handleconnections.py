import json
from game import GameRoom

rooms = {}


async def handle_connection(websocket, path):
    # This function will handle incoming WebSocket messages
    global rooms
    async for message in websocket:
        # Do something with the message (e.g. print it)
        print(f"Received message: {message}")

        message = json.loads(message)

        match message["type"]:
            case "createServer":
                game_room = GameRoom()
                game_room.add_player(message["content"])
                rooms[game_room.id] = game_room
                await websocket.send(game_room.id)
                return

            case "joinServer":
                data = message["content"]
                player_name = data["playerName"]
                room_id = data["roomName"]

                if room_id not in rooms:
                    print("ERROR: wrong room_id")
                    await websocket.send("False")
                    return

                game_room = rooms[room_id]
                game_room.add_player(player_name)
                await websocket.send("True")
                return

            case "lobbyUpdate":
                data = message["content"]
                room_id = data["roomName"]
                if room_id not in rooms:
                    print("ERROR: wrong room_id")
                    await websocket.send("False")
                    return
                game_room = rooms[room_id]
                response = game_room.get_lobby_json()
                print(game_room.get_lobby_json())
                await websocket.send(response)
                return

            case "gameStart":
                room_id = message["content"]
                game_room = rooms[room_id]
                game_room.start_game()
                await websocket.send(game_room.get_players_json())
                return
