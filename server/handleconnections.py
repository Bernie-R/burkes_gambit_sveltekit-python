# server\handleconnections.py
import json
import asyncio
import uuid
from game import GameRoom, Action, Face, History, HistoryEvent
import websockets

rooms = {}
rooms_lock = asyncio.Lock()

def new_game_id() -> str:
    id = str(uuid.uuid4())[:4]
    return new_game_id() if id in rooms else id

async def broadcast_all(room_id, message):
    async with rooms_lock:
        if room_id not in rooms:
            return
        game_room = rooms[room_id]
        if game_room.players:
            for player in game_room.players:
               if player.websocket and player.websocket.open:
                   try:
                       await player.websocket.send(json.dumps(message))
                   except Exception as e:
                       print(f"Error sending message to {player}: {e}")
                       pass #ignore any broken sockets.

async def broadcast_player(player, message):
    if player and player.websocket and player.websocket.open:
        try:
             await player.websocket.send(json.dumps(message))
        except Exception as e:
            print(f"Error sending message to {player}: {e}")
            pass #ignore any broken sockets.

async def handle_connection(websocket, path):
    global rooms

    try:
        async for raw_message in websocket:
            print(raw_message)
            try:
                message = json.loads(raw_message)
            except json.JSONDecodeError:
                await websocket.send(json.dumps({"error": "Invalid JSON"}))
                continue

            msg_type = message.get("type")
            content = message.get("content")

            match msg_type:
                case "createServer":
                    async with rooms_lock:
                        game_room = GameRoom(new_game_id())
                        player = game_room.add_player(content, websocket=websocket)
                        rooms[game_room.id] = game_room
                    response = {"type": "createServer", "content": game_room.get_game_state(player)}
                    await websocket.send(json.dumps(response))

                case "joinRoom":
                    if not isinstance(content, dict) or "playerName" not in content or "roomName" not in content:
                        await websocket.send(json.dumps({"error": "Invalid joinRoom content"}))
                        continue

                    player_name = content["playerName"]
                    room_id = content["roomName"].strip()

                    async with rooms_lock:
                        if room_id not in rooms:
                            await websocket.send(json.dumps({"error": "Room not found"}))
                            continue
                        game_room = rooms[room_id]

                    player = game_room.add_player(player_name, websocket=websocket)
                    response = {"type": "joinRoom", "content": game_room.get_game_state(player)}
                    await websocket.send(json.dumps(response))
                    
                    await broadcast_all(room_id, {"type": "players", "content": game_room.get_lobby_json()})

                case "lobbyUpdate":
                    if not isinstance(content, dict) or "roomName" not in content:
                        await websocket.send(json.dumps({"error": "Invalid lobbyUpdate content"}))
                        continue

                    room_id = content["roomName"]

                    async with rooms_lock:
                        if room_id not in rooms:
                           await websocket.send(json.dumps({"error": "Room not found"}))
                           continue
                        game_room = rooms[room_id]

                    response = {"type": "players", "content": game_room.get_lobby_json()}
                    await broadcast_all(room_id, response)

                case "gameStart":
                    if not isinstance(content, str):
                        await websocket.send(json.dumps({"error": "Invalid gameStart content"}))
                        continue

                    room_id = content

                    async with rooms_lock:
                        if room_id not in rooms:
                            await websocket.send(json.dumps({"error": "Room not found"}))
                            continue
                        game_room = rooms[room_id]

                    game_room.start_game()
                    response = {"type": "gameState", "content": game_room.get_game_state(game_room.admin)}

                    await broadcast_all(room_id, response)

                case "gameState":
                    if not isinstance(content, dict):
                        await websocket.send(json.dumps({"error": "Invalid gameState content"}))
                        continue

                    print(content)
                    room_id = content.get("roomName")
                    player = content.get("player")

                        
                    async with rooms_lock:
                        if room_id not in rooms:
                            await websocket.send(json.dumps({"error": "Room not found"}))
                            continue
                        game_room = rooms[room_id]
                        player_obj = game_room.get_player_by_name(player)
                    response = {"type": "gameState", "content": game_room.get_game_state(player_obj)}
                    await websocket.send(json.dumps(response))
                
                case "rollDice":
                    if not isinstance(content, dict):
                        await websocket.send(json.dumps({"error": "Invalid rollDice content"}))
                        continue
                    
                    room_id = content.get("roomName")
                    player_name = content.get("player")
                    reroll = content.get("reroll", False)

                    async with rooms_lock:
                        if room_id not in rooms:
                            await websocket.send(json.dumps({"error": "Room not found"}))
                            continue
                        
                        game_room = rooms[room_id]
                        player = game_room.get_player_by_name(player_name)

                        if player is None:
                            await websocket.send(json.dumps({"error": "Player not found"}))
                            continue

                        if game_room.current_player != player:
                            await websocket.send(json.dumps({"error": "Not your turn"}))
                            continue
                        
                        if reroll:
                            dice_roll_result = game_room.execute_action(player, Action.REROLL)
                        else:
                             dice_roll_result = game_room.execute_action(player, Action.PICK_AND_ROLL)
                        
                        # Prepare individual responses for each player
                        for p in game_room.players:
                            player_state = game_room.get_game_state(p)
                            response = {"type": "gameState", "content": player_state, "diceResult": dice_roll_result}
                            await broadcast_player(p, response)

                case "resolveDice":
                    if not isinstance(content, dict):
                        await websocket.send(json.dumps({"error": "Invalid resolveDice content"}))
                        continue

                    room_id = content.get("roomName")
                    player_name = content.get("player")
                    resolve = content.get("resolve", True)
                    target_player_name = content.get("targetPlayer")

                    async with rooms_lock:
                        if room_id not in rooms:
                            await websocket.send(json.dumps({"error": "Room not found"}))
                            continue
                        
                        game_room = rooms[room_id]
                        player = game_room.get_player_by_name(player_name)
                        target_player = game_room.get_player_by_name(target_player_name) if target_player_name else None

                        if player is None:
                            await websocket.send(json.dumps({"error": "Player not found"}))
                            continue
                        
                        if game_room.current_player != player:
                            await websocket.send(json.dumps({"error": "Not your turn"}))
                            continue

                        if not resolve:
                             game_room._dice_bag.return_dice(game_room.current_dice)
                             game_room.current_dice = None;
                             game_room.next_turn()
                        else:
                            if game_room.current_dice is not None:
                              game_room.use_dice_action(player, game_room.current_dice.face, target_player)
                              game_room._dice_bag.return_dice(game_room.current_dice)
                              game_room.current_dice = None;
                              game_room.next_turn()

                        # Prepare individual responses for each player
                        for p in game_room.players:
                            player_state = game_room.get_game_state(p)
                            response = {"type": "gameState", "content": player_state}
                            await broadcast_player(p, response)

                case "reserveDice":
                    if not isinstance(content, dict):
                        await websocket.send(json.dumps({"error": "Invalid reserveDice content"}))
                        continue
                    
                    room_id = content.get("roomName")
                    player_name = content.get("player")
                    
                    async with rooms_lock:
                        if room_id not in rooms:
                            await websocket.send(json.dumps({"error": "Room not found"}))
                            continue
                            
                        game_room = rooms[room_id]
                        player = game_room.get_player_by_name(player_name)

                        if player is None:
                            await websocket.send(json.dumps({"error": "Player not found"}))
                            continue

                        if game_room.current_player != player:
                            await websocket.send(json.dumps({"error": "Not your turn"}))
                            continue
                        
                        game_room.execute_action(player, Action.RESERVE_DICE)

                        # Prepare individual responses for each player
                        for p in game_room.players:
                            player_state = game_room.get_game_state(p)
                            response = {"type": "gameState", "content": player_state}
                            await broadcast_player(p, response)

                case "returnDice":
                    if not isinstance(content, dict):
                       await websocket.send(json.dumps({"error": "Invalid returnDice content"}))
                       continue

                    room_id = content.get("roomName")
                    player_name = content.get("player")

                    async with rooms_lock:
                         if room_id not in rooms:
                             await websocket.send(json.dumps({"error": "Room not found"}))
                             continue

                         game_room = rooms[room_id]
                         player = game_room.get_player_by_name(player_name)
                         if player is None:
                             await websocket.send(json.dumps({"error": "Player not found"}))
                             continue
                         if game_room.current_player != player:
                             await websocket.send(json.dumps({"error": "Not your turn"}))
                             continue
                         game_room._dice_bag.return_dice(game_room.current_dice)
                         game_room.current_dice = None
                         
                         # Prepare individual responses for each player
                         for p in game_room.players:
                            player_state = game_room.get_game_state(p)
                            response = {"type": "gameState", "content": player_state}
                            await broadcast_player(p, response)

                case "endTurn":
                    
                    continue
                
                case "submitVote":
                    if not isinstance(content, dict):
                       await websocket.send(json.dumps({"error": "Invalid submitVote content"}))
                       continue
                    
                    room_id = content.get("roomName")
                    player_name = content.get("player")
                    vote = content.get("vote")
                    
                    async with rooms_lock:
                         if room_id not in rooms:
                            await websocket.send(json.dumps({"error": "Room not found"}))
                            continue
                         game_room = rooms[room_id]
                         player = game_room.get_player_by_name(player_name)
                         if player is None:
                            await websocket.send(json.dumps({"error": "Player not found"}))
                            continue
                         
                         game_room.add_vote(player, vote)

                         # Prepare individual responses for each player
                         for p in game_room.players:
                            player_state = game_room.get_game_state(p)
                            response = {"type": "gameState", "content": player_state}
                            await broadcast_player(p, response)
                
                case "resolveEndGame":
                    if not isinstance(content, dict):
                        await websocket.send(json.dumps({"error": "Invalid resolveEndGame content"}))
                        continue
                    
                    room_id = content.get("roomName")

                    async with rooms_lock:
                        if room_id not in rooms:
                            await websocket.send(json.dumps({"error": "Room not found"}))
                            continue
                        game_room = rooms[room_id]
                    
                    player_sacrificed = game_room.resolve_end_game()
                    
                    # Prepare individual responses for each player
                    for p in game_room.players:
                         player_state = game_room.get_game_state(p)
                         response = {"type": "gameState", "content": player_state, "sacrificedPlayer": player_sacrificed.name if player_sacrificed else None }
                         await broadcast_player(p, response)

                case _:
                    await websocket.send(json.dumps({"error": "Unknown message type"}))
                    

    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")
    except Exception as e:
        print("Unexpected error:", e)