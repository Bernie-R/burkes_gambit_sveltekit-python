import sqlite3
import json
import asyncio
import websockets
from handleconnections import handle_connection

async def main():
    # Connect to the SQLite server and create the Rooms and Players databases
    connection = sqlite3.connect("server.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Rooms (roomNumber TEXT, serverCreated DATETIME, running INTEGER CHECK (running IN (0,1,2)))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Players (Player TEXT, admin BOOLEAN, roomNumber INTEGER, life INTEGER, infected BOOLEAN, character TEXT, good BOOLEAN, latestAction DATETIME, holdingDice INTEGER NULL)")
    
    # Create the Character database if it does not exist
    cursor.execute("CREATE TABLE IF NOT EXISTS Character (Character TEXT, Description TEXT)")
    
    # Load the character descriptions from the file "character.json"
    with open("characters.json", "r") as file:
        character_data = json.load(file)
    
    # Insert each character and description into the Character table
    for character, description in character_data.items():
        cursor.execute("INSERT INTO Character (Character, Description) VALUES (?, ?)", (character, description))
    
    connection.commit()
    
    async with websockets.serve(handle_connection, "0.0.0.0", 8765):
        print("WebSocket server started")
        await asyncio.Future()  # Run forever

asyncio.run(main())

