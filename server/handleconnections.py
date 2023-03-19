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
            case 'createServer':
                game_room = GameRoom()
                game_room.add_player(message['content'])
                rooms[game_room.id] = game_room
                await websocket.send(game_room.id)
                return

            case 'joinServer':
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

            case 'lobbyUpdate':
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

            # TODO: Move this logic to the GameRoom class
            case "gameStart":
                return
                #roomName = message["content"]
                #cursor.execute(f"SELECT * FROM Players WHERE roomNumber = '{roomName}'")
                #rows = cursor.fetchall()
                #player_names = [row[0] for row in rows]
                #num_players = len(player_names)
                #captain_assigned = False
                #        
                ## select all characters from the Character table
                #cursor.execute("SELECT * FROM Character")
                #all_characters = cursor.fetchall()

                ## shuffle the player names to randomize the order
                #random.shuffle(player_names)

                ## randomly select one character for each player, except Captain
                #assigned_characters = {}
                #used_characters = set()
                #for i in range(num_players):
                #    if not captain_assigned:
                #        # assign Captain to the first player
                #        captain_row = ("Captain",)
                #        for row in all_characters:
                #            if row[0] == "Captain":
                #                captain_row = row
                #                break
                #        character = (captain_row[0], captain_row[1])
                #        assigned_characters[player_names[i]] = {"character": character[0], "description": character[1]}
                #        captain_assigned = True
                #        all_characters.remove(captain_row)
                #    else:
                #        # randomly select a character from the remaining characters (excluding Captain)
                #        available_characters = [row for row in all_characters if row[0] != "Captain" and row not in used_characters]
                #        if not available_characters:
                #            # If there are no more available characters, raise an exception
                #            raise Exception("Not enough characters for all players")
                #        character_row = random.choice(available_characters)
                #        character = (character_row[0], character_row[1])
                #        assigned_characters[player_names[i]] = {"character": character[0], "description": character[1]}
                #        used_characters.add(character_row)
                #            
                #    # update the Players table with the assigned character
                #    cursor.execute(f"UPDATE Players SET character='{character[0]}', description='{character[1]}' WHERE Player='{player_names[i]}'")
                #    connection.commit()

                ## create the assigned characters dictionary
                #assigned_characters_dict = {"players": assigned_characters}

                ## count the number of players
                #num_players = len(player_names)

                ## update the "good" and "infected" columns in the Players table based on the number of players
                #if num_players == 4:
                #    cursor.execute(f"UPDATE Players SET good=1 WHERE roomNumber='{roomName}'")
                #    random_name = random.choice(player_names)
                #    cursor.execute(f"UPDATE Players SET good=0 WHERE roomNumber='{roomName}' AND Player='{random_name}'")
                #    cursor.execute(f"UPDATE Players SET infected=1 WHERE roomNumber='{roomName}' AND Player='{random_name}'")
                #elif num_players == 5:
                #    cursor.execute(f"UPDATE Players SET good=1 WHERE roomNumber='{roomName}'")
                #    random_names = random.sample(player_names, 2)
                #    cursor.execute(f"UPDATE Players SET good=0 WHERE roomNumber='{roomName}' AND Player IN {tuple(random_names)}")
                #    random_name = random.choice(player_names)
                #    cursor.execute(f"UPDATE Players SET infected=1 WHERE roomNumber='{roomName}' AND Player='{random_name}'")
                #elif num_players == 6:
                #    cursor.execute(f"UPDATE Players SET good=1 WHERE roomNumber='{roomName}'")
                #    random_names = random.sample(player_names, 2)
                #    cursor.execute(f"UPDATE Players SET good=0 WHERE roomNumber='{roomName}' AND Player IN {tuple(random_names)}")
                #    random_name = random.choice(player_names)
                #    cursor.execute(f"UPDATE Players SET infected=1 WHERE roomNumber='{roomName}' AND Player='{random_name}'")
                #elif num_players == 7:
                #    cursor.execute(f"UPDATE Players SET good=1 WHERE roomNumber='{roomName}'")
                #    random_names = random.sample(player_names, 3)
                #    cursor.execute(f"UPDATE Players SET good=0 WHERE roomNumber='{roomName}' AND Player IN {tuple(random_names)}")
                #    random_name = random.choice(player_names)
                #    cursor.execute(f"UPDATE Players SET infected=1 WHERE roomNumber='{roomName}' AND Player='{random_name}'")
                #elif num_players >= 8:
                #    cursor.execute(f"UPDATE Players SET good=1 WHERE roomNumber='{roomName}'")
                #    random_names = random.sample(player_names, 3)
                #    cursor.execute(f"UPDATE Players SET good=0 WHERE roomNumber='{roomName}' AND Player IN {tuple(random_names)}")
                #    random_name = random.choice(player_names)
                #    cursor.execute(f"UPDATE Players SET infected=1 WHERE roomNumber='{roomName}' AND Player='{random_name}'")

                #if num_players == 4:
                #    cursor.execute(f"UPDATE Rooms SET max_lightning=3 WHERE roomNumber='{roomName}'")
                #elif num_players == 5:
                #    cursor.execute(f"UPDATE Rooms SET max_lightning=4 WHERE roomNumber='{roomName}'")
                #elif num_players == 6:
                #    cursor.execute(f"UPDATE Rooms SET max_lightning=5 WHERE roomNumber='{roomName}'")
                #elif num_players >= 7:
                #    cursor.execute(f"UPDATE Rooms SET max_lightning=6 WHERE roomNumber='{roomName}'")
                #connection.commit()

                ## send the assigned characters dictionary to the client
                #data_json = json.dumps(assigned_characters_dict)
                #await websocket.send(data_json)

