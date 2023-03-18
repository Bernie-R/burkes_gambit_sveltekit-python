import random
import json
import sqlite3
import datetime


async def handle_connection(websocket, path):
    # This function will handle incoming WebSocket messages
    async for message in websocket:
        # Do something with the message (e.g. print it)
        print(f"Received message: {message}")
    
        message = json.loads(message)
        connection = sqlite3.connect("server.db")
        cursor = connection.cursor()

        if message["type"] == 'createServer':
            playerName = message["content"]
            room_number = await create_new_server(playerName)
            await websocket.send(room_number)

        elif message["type"] == 'joinRoom':
            data = message["content"]
            playerName = data["playerName"]
            roomName = data["roomName"]

            # Check if the room exists in the Rooms table
            row = cursor.execute(f"SELECT * FROM Rooms WHERE roomNumber='{roomName}'").fetchone()
            if row is not None:
                # Check if the player already exists in the Players table
                player_row = cursor.execute(f"SELECT * FROM Players WHERE Player='{playerName}' AND roomNumber='{roomName}'").fetchone()
                if player_row is not None:
                    await websocket.send("True")
                else:
                    # Insert the new player into the Players table
                    latest_action = datetime.datetime.now()
                    cursor.execute(f"INSERT INTO Players (Player, Admin, roomNumber, life, infected, character, good, latestAction, description) VALUES ('{playerName}', 0, '{roomName}', 2, 0, NULL, 1, '{latest_action}', NULL)")
                    connection.commit()
                    await websocket.send("True")
            else:
                await websocket.send("False")
        elif message["type"] == "gameStatusUpdate":
            roomName = message["content"]
            print(roomName)
            cursor.execute(f"UPDATE Rooms SET running = {2} WHERE roomNumber = '{roomName}'")
            connection.commit()


        elif message["type"] == 'lobbyUpdate':
            data = message["content"]
            roomName = data["roomName"]
            playerName = data["playerName"]
            cursor.execute(f"SELECT * FROM Players WHERE roomNumber = '{roomName}'")
            rows = cursor.fetchall()
            player_names = [row[0] for row in rows]
            room_data = cursor.execute(f"SELECT running FROM Rooms WHERE roomNumber = '{roomName}'").fetchone()
            running_status = room_data[0] if room_data else None
            admin_data = cursor.execute(f"SELECT admin FROM Players WHERE roomNumber = '{roomName}' AND Player = '{playerName}'").fetchone()
            player_admin = admin_data[0] if admin_data else None
            # Create a dictionary with the player names list, running status, and player admin value
            data = {"player_list": player_names, "running": running_status, "admin": player_admin}
            # Convert the dictionary to a JSON object
            data_json = json.dumps(data)
            await websocket.send(data_json)

        elif message["type"] == "gameStart":
            roomName = message["content"]
            cursor.execute(f"SELECT * FROM Players WHERE roomNumber = '{roomName}'")
            rows = cursor.fetchall()
            player_names = [row[0] for row in rows]
            num_players = len(player_names)
            captain_assigned = False
                    
            # select all characters from the Character table
            cursor.execute("SELECT * FROM Character")
            all_characters = cursor.fetchall()

            # shuffle the player names to randomize the order
            random.shuffle(player_names)

            # randomly select one character for each player, except Captain
            assigned_characters = {}
            used_characters = set()
            for i in range(num_players):
                if not captain_assigned:
                    # assign Captain to the first player
                    captain_row = ("Captain",)
                    for row in all_characters:
                        if row[0] == "Captain":
                            captain_row = row
                            break
                    character = (captain_row[0], captain_row[1])
                    assigned_characters[player_names[i]] = {"character": character[0], "description": character[1]}
                    captain_assigned = True
                    all_characters.remove(captain_row)
                else:
                    # randomly select a character from the remaining characters (excluding Captain)
                    available_characters = [row for row in all_characters if row[0] != "Captain" and row not in used_characters]
                    if not available_characters:
                        # If there are no more available characters, raise an exception
                        raise Exception("Not enough characters for all players")
                    character_row = random.choice(available_characters)
                    character = (character_row[0], character_row[1])
                    assigned_characters[player_names[i]] = {"character": character[0], "description": character[1]}
                    used_characters.add(character_row)
                        
                # update the Players table with the assigned character
                cursor.execute(f"UPDATE Players SET character='{character[0]}', description='{character[1]}' WHERE Player='{player_names[i]}'")
                connection.commit()

            # create the assigned characters dictionary
            assigned_characters_dict = {"players": assigned_characters}

            # count the number of players
            num_players = len(player_names)

            # update the "good" and "infected" columns in the Players table based on the number of players
            if num_players == 4:
                cursor.execute(f"UPDATE Players SET good=1 WHERE roomNumber='{roomName}'")
                random_name = random.choice(player_names)
                cursor.execute(f"UPDATE Players SET good=0 WHERE roomNumber='{roomName}' AND Player='{random_name}'")
                cursor.execute(f"UPDATE Players SET infected=1 WHERE roomNumber='{roomName}' AND Player='{random_name}'")
            elif num_players == 5:
                cursor.execute(f"UPDATE Players SET good=1 WHERE roomNumber='{roomName}'")
                random_names = random.sample(player_names, 2)
                cursor.execute(f"UPDATE Players SET good=0 WHERE roomNumber='{roomName}' AND Player IN {tuple(random_names)}")
                random_name = random.choice(player_names)
                cursor.execute(f"UPDATE Players SET infected=1 WHERE roomNumber='{roomName}' AND Player='{random_name}'")
            elif num_players == 6:
                cursor.execute(f"UPDATE Players SET good=1 WHERE roomNumber='{roomName}'")
                random_names = random.sample(player_names, 2)
                cursor.execute(f"UPDATE Players SET good=0 WHERE roomNumber='{roomName}' AND Player IN {tuple(random_names)}")
                random_name = random.choice(player_names)
                cursor.execute(f"UPDATE Players SET infected=1 WHERE roomNumber='{roomName}' AND Player='{random_name}'")
            elif num_players == 7:
                cursor.execute(f"UPDATE Players SET good=1 WHERE roomNumber='{roomName}'")
                random_names = random.sample(player_names, 3)
                cursor.execute(f"UPDATE Players SET good=0 WHERE roomNumber='{roomName}' AND Player IN {tuple(random_names)}")
                random_name = random.choice(player_names)
                cursor.execute(f"UPDATE Players SET infected=1 WHERE roomNumber='{roomName}' AND Player='{random_name}'")
            elif num_players >= 8:
                cursor.execute(f"UPDATE Players SET good=1 WHERE roomNumber='{roomName}'")
                random_names = random.sample(player_names, 3)
                cursor.execute(f"UPDATE Players SET good=0 WHERE roomNumber='{roomName}' AND Player IN {tuple(random_names)}")
                random_name = random.choice(player_names)
                cursor.execute(f"UPDATE Players SET infected=1 WHERE roomNumber='{roomName}' AND Player='{random_name}'")

            if num_players == 4:
                cursor.execute(f"UPDATE Rooms SET max_lightning=3 WHERE roomNumber='{roomName}'")
            elif num_players == 5:
                cursor.execute(f"UPDATE Rooms SET max_lightning=4 WHERE roomNumber='{roomName}'")
            elif num_players == 6:
                cursor.execute(f"UPDATE Rooms SET max_lightning=5 WHERE roomNumber='{roomName}'")
            elif num_players >= 7:
                cursor.execute(f"UPDATE Rooms SET max_lightning=6 WHERE roomNumber='{roomName}'")
            connection.commit()

            # send the assigned characters dictionary to the client
            data_json = json.dumps(assigned_characters_dict)
            await websocket.send(data_json)





async def check_running_server(playerName):
    pass


async def create_new_server(playerName):
    # Generate a new 4-digit room number that is not already in the Rooms database
    connection = sqlite3.connect("server.db")
    cursor = connection.cursor()
    room_number = str(random.randint(1000, 9999))
    while cursor.execute(f"SELECT COUNT(*) FROM Rooms WHERE roomNumber='{room_number}'").fetchone()[0] > 0:
        room_number = str(random.randint(1000, 9999))
    
    # Insert the new room into the Rooms database
    server_created = datetime.datetime.now()
    cursor.execute(f"INSERT INTO Rooms (roomNumber, serverCreated, running) VALUES ('{room_number}', '{server_created}', 1)")
    connection.commit()

    # Insert the new player into the Players database
    latest_action = datetime.datetime.now()
    cursor.execute(f"INSERT INTO Players (Player, Admin, roomNumber,life, infected, character, good, latestAction, holdingDice) VALUES ('{playerName}', 1,'{room_number}', 2, 0, NULL, 1, '{latest_action}', NULL)")
    connection.commit()

    return room_number