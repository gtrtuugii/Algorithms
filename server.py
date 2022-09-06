# Tuguldur Gantumur (22677666)
#
# CITS3002 2021 Assignment
# Extended due date: 06/06/2021 5PM
#
# This file implements a basic server that allows a single client to play a
# single game with no other participants, and very little error checking.
#
# Any other clients that connect during this time will need to wait for the
# first client's game to complete.
#
# Your task will be to write a new server that adds all connected clients into
# a pool of players. When enough players are available (two or more), the server
# will create a game with a random sample of those players (no more than
# tiles.PLAYER_LIMIT players will be in any one game). Players will take turns
# in an order determined by the server, continuing until the game is finished
# (there are less than two players remaining). When the game is finished, if
# there are enough players available the server will start a new game with a
# new selection of clients.




# was unable to send player who join mid game, the movements of previous turns
# They will receive board updates from the turn they joined onwards


import socket
import sys
import tiles
import random
from time import sleep
from threading import Thread

# Global variables

# in the tiles.py module max players is set as 4
# 4 players are allowed in a single game, but can allow more spectators
max_players = tiles.PLAYER_LIMIT 

# whom will join if a player leaves the game
# if a player disconnects, the new player from the wait list will enter the game 

# lists to store player objects
connected_players = []
wait_list = []
in_game = []
eliminated_players = [] # Can be implemented to use for tie games
                        # However, who would win? the player who placed the tile or the other one?
live_idnums = []

# initialize Game state
gameFin = False
gameRunning = False


class Player:
  # Player class to store the Player ID, Address, Connection, Name, Elimination State,
  # Tiles in hand, and Tiles placed
  def __init__(self, idnum, address, connection, name, status, hand, tiles_placed):
    self.idnum = idnum
    self.address = address
    self.connection = connection
    self.name = name
    self.status = status # Indicates whether the player is eliminated or not
    self.hand = []
    self.tiles_placed = []
    
  def getPlayerID(self):
    return self.idnum

  def getPlayerAddress(self):
    return self.address

  def getPlayerConnection(self):
    return self.connection

  def getPlayerName(self):
    return self.name

  def getTilesInHand(self):
    return self.hand
    
  def getTilesPlaced(self):
    return self.tiles_placed

  def eliminatePlayer(self):
    self.status = True

  def isPlayerEliminated(self):
    return self.status

  def addTilesPlaced(self, list):
    self.tiles_placed.append(list)

  def clearTilesPlaced(self):
    self.tiles_placed.clear()

  def clearHand(self):
    self.hand.clear()
  
  def addToHand(self, tile):
    self.hand.append(tile)

  def removeFromHand(self, tile):
    self.hand.remove(tile)


class Server:

  def client_handler(connection, address):
    # Method to append new connections to the connected_players global list
    # If a player joins mid-game, they will be stored in wait_list
    if(gameRunning == False): 
      host, port = address
      name = '{}:{}'.format(host, port)

      if(len(connected_players) == 0):
        idnum = 0
      else:
        previous_id = Player.getPlayerID(connected_players[-1])
        idnum = previous_id + 1
      player  = Player(idnum, address, connection, name, False, [], [])
      print("Player with ID: {} joined".format( idnum))
      
  
      # Add the connected player to our connected_players list
      player.connection.send(tiles.MessageWelcome(player.idnum).pack())
      connected_players.append(player)
      # Send the player a MSG 'Welcome!'

    else:
      host, port = address
      name = '{}:{}'.format(host, port)
      previous_id = Player.getPlayerID(connected_players[-1])
      idnum = previous_id + 1
      player  = Player(idnum, address, connection, name, False, [], [])
      player.connection.send(tiles.MessageWelcome(player.idnum).pack())

      for og_player in connected_players:
        Player.getPlayerConnection(player).send(tiles.MessagePlayerJoined(Player.getPlayerName(og_player), Player.getPlayerID(og_player)).pack())

     
      connected_players.append(player)
      wait_list.append(player)

      # An attempt to get tokens and tiles from every player
      #
      # wait_board = tiles.Board()
      # positionupdates, eliminated = wait_board.do_player_movement(live_idnums)

      # if(len(eliminated) > 0):
      #   for playerid in eliminated:
      #     Player.getPlayerConnection(player).send(tiles.MessagePlayerEliminated(playerid).pack())

      # for msg in positionupdates:
      #   for og_player in in_game:
      #     try:
      #       Player.getPlayerConnection(og_player).send(msg.pack())
      #     except BrokenPipeError:
      #       connected_players.remove(og_player)
      #       continue
      # print("CODE REACHES")


  def categorize(connected_players):
    # Function to categorize connected players into their respective lists
    # 4 players will be chosen at random from connected_players and put
    # into in_game, the rest will join as spectators in wait_list
    global in_game, wait_list, live_idnums, gameRunning
    if(not gameRunning):
      players_allowed = len(connected_players)
      if(players_allowed > max_players):
        players_allowed = max_players

      in_game = random.sample(connected_players, players_allowed)

      # if the player is not in the in_game list
      # They will be stored in wait_list (spectators)
      for player in connected_players:
        if player not in in_game:
          wait_list.append(player)

      # According to the Project specs each player will have a random order
      # After being randomly selected?
      random.shuffle(in_game)
      for player in in_game:
        live_idnums.append(Player.getPlayerID(player))
    
      #send all players a notification if a player joins
      for player in connected_players:
        for j in connected_players:
          if(Player.getPlayerID(player) != Player.getPlayerID(j)):
            Player.getPlayerConnection(player).send(tiles.MessagePlayerJoined(Player.getPlayerName(j), Player.getPlayerID(j)).pack())
    else:
      # Handle a client connected mid-game
      for player in connected_players:
        if player not in in_game:
          if player not in wait_list:
            wait_list.append(player)
            #Player.getPlayerConnection(player).send(tiles.MessageWelcome(Player.getPlayerID(player)).pack())
            for og_player in connected_players:
              Player.getPlayerConnection(og_player).send(tiles.MessagePlayerJoined(Player.getPlayerName(player),Player.getPlayerID(player)).pack())
            print("PLAYER JOINED MID GAME")


  def init_game():
    # Annouce the game is starting to each player
    # and give the players in in_game 4 tiles (i.e tiles.HAND_SIZE) each
    global in_game
    
    # announce that the game is starting
    for i in connected_players:
      Player.getPlayerConnection(i).send(tiles.MessageGameStart().pack())
   
    # assign each player a hand of tiles
    for i in in_game:
      tiles_hand = []
      for _ in range(tiles.HAND_SIZE):
        tileid = tiles.get_random_tileid()
        Player.getPlayerConnection(i).send(tiles.MessageAddTileToHand(tileid).pack())
        Player.addToHand(i,tileid)


  def check_pos(x,y,position):
    # There are 8 positions on a tile
    # A position is valid if they touch the borders of the tile
    # tiles.py line 475 - 483 is used to verify whether a position is valid
    # is position in tile valid?
    if (position == 0 or position == 1) and y != tiles.BOARD_HEIGHT - 1:
      return False
    if (position == 2 or position == 3) and x != tiles.BOARD_WIDTH - 1:
      return False
    if (position == 4 or position == 5) and y != 0:
      return False
    if (position == 6 or position == 7) and x != 0:
      return False
    return True
    

  def main_gameplay():
    # Function to run main gameplay
    # receive connections, update positions, movement, and eliminate
    # is further used for the autmo move tier, where the computer will place
    # a tile if the user is idle for 10 seconds

    global live_idnums, in_game, connected_players, unavailable, gameFin
    # initialize a new array to store player ids within the game
    # with purpose to delete the id when a player gets eliminated
    # but not removed from the game
    # i.e create a copy for live_idnums that we can modify
    # live_idnums and in_game have the same order
    player_orders = live_idnums
    current = in_game[0]   # First player, after being shuffled in categorize()
    current_ind = player_orders.index(Player.getPlayerID(current))
    
    for player in connected_players:
      Player.getPlayerConnection(player).send(tiles.MessagePlayerTurn(Player.getPlayerID(current)).pack())

    board = tiles.Board()
    buffer = bytearray()
    
    while True:

      # If a player doesn't make a move for 10 seconds, The Computer will make a move for them
      time_out = Player.getPlayerConnection(current).settimeout(10.0)
      try:
        # Player makes a move
        chunk = Player.getPlayerConnection(current).recv(4096)
        if not chunk:
          # Handling disconnected Players
          print('client {} disconnected'.format(Player.getPlayerAddress(current)))

          # Notify every player that a player left
          for player in connected_players:
            Player.getPlayerConnection(player).send(tiles.MessagePlayerLeft(Player.getPlayerID(current)).pack())
          
          # Remove the disconnected player from lists and save the index
          # The next Player will use the disconnected players index
          
          current_ind = in_game.index(current)
          # The player with the last order disconnected, thus we have to move the index
          # To the first player 
          player_orders.remove(Player.getPlayerID(current))
          in_game.remove(current)
          connected_players.remove(current)

          # One player left
          if(len(in_game) < 2 or len(player_orders) < 2):
            gameFin = True
            return

          # Two or more player left simultaniously 
          if(len(in_game) < 1 or len(player_orders) < 1):
            gameFin = True
            return 

          # Make current point to the next Player
          # the next player will re-use the old index since the player left 
          if(current_ind < len(in_game) - 1):
            current = in_game[current_ind]
          else:
            current_ind = 0
            current = in_game[current_ind]
            
          # Make it the next players turn
          for player in connected_players:
            Player.getPlayerConnection(player).send(tiles.MessagePlayerTurn(Player.getPlayerID(current)).pack())
          continue
    
        buffer.extend(chunk)
      
        while True:
          # While player is not idle receive and read the msg
          msg, consumed = tiles.read_message_from_bytearray(buffer)
            
          if not consumed:
              break


          buffer = buffer[consumed:]
          print('received message {}'.format(msg))

          # If the msg contains tile placement (i.e round 1 or subsequent rounds)
          if isinstance(msg, tiles.MessagePlaceTile):
            if board.set_tile(msg.x, msg.y, msg.tileid, msg.rotation, msg.idnum):
              # notify client that placement was successful
              Player.addTilesPlaced(current,[msg.x,msg.y])
              if(msg.tileid in Player.getTilesInHand(current)):
                Player.removeFromHand(current, msg.tileid)


              try:
                for player in connected_players:
                  Player.getPlayerConnection(player).send(msg.pack())
              except BrokenPipeError:
                connected_players.remove(player)
                print("Player left")
                continue
                
              # check for token movement
              positionupdates, eliminated = board.do_player_movement(player_orders)

              for msg in positionupdates:
                for player in connected_players:
                  try:
                    Player.getPlayerConnection(player).send(msg.pack())
                  except BrokenPipeError:
                    connected_players.remove(player)
                    continue

              # pickup a new tile
              tileid = tiles.get_random_tileid()
              Player.getPlayerConnection(current).send(tiles.MessageAddTileToHand(tileid).pack())
              Player.addToHand(current, tileid)
              

              # Tie game
              if(len(player_orders) < 1 or len(in_game) < 1):
                #gameFin = True
                return

              # increment the current user to the next one according to their
              # elimination status
              x = current_ind
              y = current_ind
              init_id = Player.getPlayerID(current)
              init_del = False

         
              while x < len(in_game) + y:

                index_player =  x % len(in_game)

                if Player.getPlayerID(in_game[index_player]) in eliminated:
                  if(Player.getPlayerID(in_game[index_player]) == init_id):
                    init_del = True
                  print("{} got eliminated".format(Player.getPlayerID((in_game[index_player]))))
                  Player.eliminatePlayer(in_game[index_player])
                
            
                  for player in connected_players:
                    Player.getPlayerConnection(player).send(tiles.MessagePlayerEliminated(Player.getPlayerID(in_game[index_player])).pack())

                  player_orders.remove(Player.getPlayerID(in_game[index_player]))
                  
                  in_game.pop(index_player)
                  if(len(in_game) < 1):
                    gameFin =  True
                    return
                  if(current_ind == index_player):
                    if(index_player < len(in_game)):
                      current = in_game[index_player]
                    else:
                      current_ind = 0
                      current = in_game[current_ind]
                else:
                    x += 1
                    if(not init_del):
                      if(y == index_player):
                        current_ind = (current_ind + 1) % len(in_game)
                        current =  in_game[current_ind]
                      
             

              # 1 or less player remains
              if(len(player_orders) < 2):
                gameFin = True
                return

              # Current players round ended
              # Set next player to current
              for player in connected_players:
                Player.getPlayerConnection(player).send(tiles.MessagePlayerTurn(Player.getPlayerID(current)).pack())

              
              
                
            # sent by the player in the second turn, to choose their token's
            # starting path
          elif isinstance(msg, tiles.MessageMoveToken):
            if not board.have_player_position(msg.idnum):
              if board.set_player_start_position(msg.idnum, msg.x, msg.y, msg.position):

                # check for token movement
                positionupdates, eliminated = board.do_player_movement(player_orders) 

                for msg in positionupdates:
                  for player in connected_players:
                    try:
                      Player.getPlayerConnection(player).send(msg.pack())
                    except BrokenPipeError:
                      connected_players.remove(player)
                      continue


                # increment the current user to the next one according to their
                # elimination status
                x = current_ind
                y = current_ind
                init_id = Player.getPlayerID(current)
                init_del = False

                while x < len(in_game) + y:
                  index_player =  x % len(in_game)
                  if Player.getPlayerID(in_game[index_player]) in eliminated:
                    if(Player.getPlayerID(in_game[index_player]) == init_id):
                      init_del = True
                    print("{} got eliminated".format(Player.getPlayerID((in_game[index_player]))))
                    Player.eliminatePlayer(in_game[index_player])
                
            
                    for player in connected_players:
                      Player.getPlayerConnection(player).send(tiles.MessagePlayerEliminated(Player.getPlayerID(in_game[index_player])).pack())

                    player_orders.remove(Player.getPlayerID(in_game[index_player]))
                    
                    in_game.pop(index_player)
                    if(len(in_game) < 1):
                      return

                    if(current_ind == index_player):
                      if(index_player < len(in_game)):
                        current = in_game[index_player]
                      else:
                        current_ind = 0
                        current = in_game[current_ind]
                  else:
                      x += 1
                      if(not init_del):
                        if(y == index_player):
                          current_ind = (current_ind + 1) % len(in_game)
                          current =  in_game[current_ind]
                   
                # 1 Player left
                if(len(player_orders) < 2 ): 
                  gameFin = True
                  return
                # Tie game
                elif(len(player_orders) < 1 or len(in_game) < 1):
                  # Tie game
                  gameFin = True
                  return
                
                  # Current players round ended
                  # Set next player to current
                for player in connected_players:
                  try:
                    Player.getPlayerConnection(player).send(tiles.MessagePlayerTurn(Player.getPlayerID(current)).pack())
                  except BrokenPipeError:
                    connected_players.remove(player)
                    continue
        continue
      except ConnectionResetError:
        # Handling ConnectionResetError
        # Notify every player that a player left
          for player in connected_players:
            Player.getPlayerConnection(player).send(tiles.MessagePlayerLeft(Player.getPlayerID(current)).pack())
          current_ind = in_game.index(current)
          # The player with the last order disconnected, thus we have to move the index
          # To the first player 
          player_orders.remove(Player.getPlayerID(current))
          in_game.remove(current)
          connected_players.remove(current)

          # One player left
          if(len(in_game) < 2 or len(player_orders) < 2):
            gameFin = True
            return

          # Two or more player left simultaniously 
          if(len(in_game) < 1 or len(player_orders) < 1):
            gameFin = True
            return 

          # Make current point to the next Player
          # the next player will re-use the old index since the player left 
          if(current_ind < len(in_game) - 1):
            current = in_game[current_ind]
          else:
            current_ind = 0
            current = in_game[current_ind]
            
          # Make it the next players turn
          for player in connected_players:
            Player.getPlayerConnection(player).send(tiles.MessagePlayerTurn(Player.getPlayerID(current)).pack())
        
      except socket.timeout:
        # Code executed when a player doesn't make a move for 10 sec
        if(len(Player.getTilesPlaced(current)) == 0):
          #BOARD_WIDTH = 5  # width of the game board, in tiles
          #BOARD_HEIGHT = 5 # height of the game board in tiles
          x_pos = random.randint(0,4)
          y_pos = random.randint(0,4)
          rand_rotation = random.randint(0,3)
          rand_tile = random.choice(Player.getTilesInHand(current))
          borders = [0,4]
          if(x_pos != 0 and y_pos != 0 or x_pos != 4 and y_pos != 4):
            y_pos = random.choice(borders)
          
          # Check whether the random tile is empty, i.e owned by another player
          # Calling board.get_tile and fill the empty tuples
          check_tile, check_rot, check_id = board.get_tile(x_pos, y_pos)

          # If the random board position chosen has a idnum or tileid
          # it means its owned by someone else, thus random again.
          if(check_id != None or check_tile != None):
            while(check_id == None or check_tile == None):
              #Have to set it a new random position
              x_pos = random.randint(0,4)
              y_pos = random.randint(0,4)
              rand_rotation = random.randint(0,1)
              rand_tile = random.choice(Player.getTilesInHand(current))
              borders = [0,4]
              if(x_pos != 0 and y_pos != 0 or x_pos != 4 and y_pos != 4):
                y_pos = random.choice(borders)
              check_tile, check_rot, check_id = board.get_tile(x_pos, y_pos)

          if board.set_tile(x_pos,y_pos,rand_tile, rand_rotation, Player.getPlayerID(current)):
            # Successfully Placed tile
            Player.addTilesPlaced(current, [x_pos, y_pos])

            # Notify other player a tile has been placed
            for player in connected_players:
              Player.getPlayerConnection(player).send(tiles.MessagePlaceTile(Player.getPlayerID(current), rand_tile, rand_rotation, x_pos, y_pos).pack())
            #remove the placed tile from the player hands list
            if(rand_tile in Player.getTilesInHand(current)):
              Player.removeFromHand(current, rand_tile)
            # pickup a new tile
            rtileid = tiles.get_random_tileid()
            Player.addToHand(current, rtileid)
            Player.getPlayerConnection(current).send(tiles.MessageAddTileToHand(rtileid).pack())
            
            # check for token movement
            positionupdates, eliminated = board.do_player_movement(player_orders)

            for msg in positionupdates:
              for player in connected_players:
                Player.getPlayerConnection(player).send(msg.pack())

            # Increment current
            x = current_ind
            y = current_ind
            init_id = Player.getPlayerID(current)
            init_del = False
            # Increment current
            # No one can get eliminated in this round
            while x < len(in_game) + y:

              index_player =  x % len(in_game)

              if Player.getPlayerID(in_game[index_player]) in eliminated:
                if(Player.getPlayerID(in_game[index_player]) == init_id):
                  init_del = True
                print("{} got eliminated".format(Player.getPlayerID((in_game[index_player]))))
                Player.eliminatePlayer(in_game[index_player])
           
            
                for player in connected_players:
                  Player.getPlayerConnection(player).send(tiles.MessagePlayerEliminated(Player.getPlayerID(in_game[index_player])).pack())

                player_orders.remove(Player.getPlayerID(in_game[index_player]))
                  
                in_game.pop(index_player)
                if(current_ind == index_player):
                  if(index_player < len(in_game)):
                    current = in_game[index_player]
                  else:
                    current_ind = 0
                    current = in_game[current_ind]
              else:
                  x += 1
                  if(not init_del):
                    if(y == index_player):
                      current_ind = (current_ind + 1) % len(in_game)
                      current =  in_game[current_ind]

            
            for player in connected_players:
              Player.getPlayerConnection(player).send(tiles.MessagePlayerTurn(Player.getPlayerID(current)).pack())
        
        elif(len(Player.getTilesPlaced(current)) >= 1):
          
          if not board.have_player_position(Player.getPlayerID(current)):
            # Get the current player's list of all tiles he placed, since it is the 2nd turn there will only be 
            # one pair of x,y coordinates at [0][0] and [0][1]
            getboardpos = Player.getTilesPlaced(current)
            x_pos = getboardpos[0][0]
            y_pos = getboardpos[0][1]
            start_pos = [0, 1, 2, 3, 4, 5, 6, 7]
            available_pos = []
         
            # A tile can have a spot for a token in any spot from 0 to 7 (inclusive)
            # Server.check_pos checks which positions for the token are valid
            # for the given x_pos and y_pos
            for pos in start_pos:
              valid = Server.check_pos(x_pos, y_pos, pos)
              if(valid == True):
                available_pos.append(pos)
            
            rand_start_pos = random.choice(available_pos)
 
            
            if board.set_player_start_position(Player.getPlayerID(current),x_pos, y_pos, rand_start_pos):
              #Succesfully chose a token 

              # Update players that the current user has chosen their token
              for player in connected_players:
                Player.getPlayerConnection(player).send(tiles.MessageMoveToken(Player.getPlayerID(current), x_pos, y_pos, rand_start_pos).pack())
              
              # check for token movement
              positionupdates, eliminated = board.do_player_movement(player_orders)

              for msg in positionupdates:
                for player in connected_players:
                  try:
                    Player.getPlayerConnection(player).send(msg.pack())
                  except BrokenPipeError:
                    connected_players.remove(player)
                    continue


              if(len(player_orders) < 1 or len(in_game) < 1):
                # Tie game
                #gameFin = True
                return

              # Increment current
              x = current_ind
              y = current_ind
              init_id = Player.getPlayerID(current)
              init_del = False
              while x < len(in_game) + y:
                index_player =  x % len(in_game)
                if Player.getPlayerID(in_game[index_player]) in eliminated:
                  if(Player.getPlayerID(in_game[index_player]) == init_id):
                    init_del = True
                  print("{} got eliminated".format(Player.getPlayerID((in_game[index_player]))))
                  Player.eliminatePlayer(in_game[index_player])
           
              
                  for player in connected_players:
                    Player.getPlayerConnection(player).send(tiles.MessagePlayerEliminated(Player.getPlayerID(in_game[index_player])).pack())

                  player_orders.remove(Player.getPlayerID(in_game[index_player]))
                  #in_game.remove(in_game[index_player])
                  in_game.pop(index_player)
                  if(len(in_game) < 1):
                    return
                    
                  if(current_ind == index_player):
                    if(index_player < len(in_game)):
                      current = in_game[index_player]
                    else:
                      current_ind = 0
                      current = in_game[current_ind]
                else:
                    x += 1
                    if(not init_del):
                      if(y == index_player):
                        current_ind = (current_ind + 1) % len(in_game)
                        current =  in_game[current_ind]
              
              # 1 or less player remains
              if(len(player_orders) < 2 or len(in_game) < 2):
                #gameFin = True
                return

              # Current players round ended
              # Set next player to current
              for player in connected_players:
                try:
                  Player.getPlayerConnection(player).send(tiles.MessagePlayerTurn(Player.getPlayerID(current)).pack())
                except BrokenPipeError:
                  connected_players.remove(player)
                  continue
            

          elif(board.have_player_position(Player.getPlayerID(current))):
            # Get current players previous coordinates
            rand_rotation = random.randint(0,3)
            rand_tile = random.choice(Player.getTilesInHand(current))
            x_pos, y_pos, last_pos = board.get_player_position(Player.getPlayerID(current))
            # Check if the board is on any borders
            if board.set_tile(x_pos, y_pos, rand_tile, rand_rotation, Player.getPlayerID(current)):
              # Add the tile placed to our directory of tiles placed for the Player
              Player.addTilesPlaced(current, [x_pos, y_pos])

              # Notify other player a tile has been placed
              for player in connected_players:
                Player.getPlayerConnection(player).send(tiles.MessagePlaceTile(Player.getPlayerID(current), rand_tile, rand_rotation, x_pos, y_pos).pack())

              #remove the placed tile from the player hands list
              if rand_tile in Player.getTilesInHand(current):
                Player.removeFromHand(current, rand_tile)

              # pickup a new tile
              rtileid = tiles.get_random_tileid()
              Player.addToHand(current, rtileid)
              Player.getPlayerConnection(current).send(tiles.MessageAddTileToHand(rtileid).pack())

              

              # check for token movement
              positionupdates, eliminated = board.do_player_movement(player_orders)
              for msg in positionupdates:         
                for player in connected_players:
                  try:
                    Player.getPlayerConnection(player).send(msg.pack())
                  except BrokenPipeError:
                    connected_players.remove(player)
                    continue
              

              #Tie game
              if(len(player_orders) == 0 or len(in_game) == 0):
                # Tie game
                #gameFin = True
                return

              # Increment current
              x = current_ind
              y = current_ind
              init_id = Player.getPlayerID(current)
              init_del = False
              # Increment current
              # No one can get eliminated in this round
              while x < len(in_game) + y:
                index_player =  x % len(in_game)
                if Player.getPlayerID(in_game[index_player]) in eliminated:
                  if(Player.getPlayerID(in_game[index_player]) == init_id):
                    init_del = True
                  print("{} got eliminated".format(Player.getPlayerID((in_game[index_player]))))
                  Player.eliminatePlayer(in_game[index_player])
             
              
                  for player in connected_players:
                    Player.getPlayerConnection(player).send(tiles.MessagePlayerEliminated(Player.getPlayerID(in_game[index_player])).pack())

                  player_orders.remove(Player.getPlayerID(in_game[index_player]))
                    
                  in_game.pop(index_player)
                  if(len(in_game) < 1):
                    return
                  if(current_ind == index_player):
                    if(index_player < len(in_game)):
                      current = in_game[index_player]
                    else:
                      current_ind = 0
                      current = in_game[current_ind]
                else:
                    x += 1
                    if(not init_del):
                      if(y == index_player):
                        current_ind = (current_ind + 1) % len(in_game)
                        current =  in_game[current_ind]

              # 1 or less player remains
              if(len(player_orders) < 2 or len(in_game) < 2):
                #gameFin = True
                return



              # Current players round ended
              # Set next player to current
              for player in connected_players:
                Player.getPlayerConnection(player).send(tiles.MessagePlayerTurn(Player.getPlayerID(current)).pack())


  def recursive_game():
    # A function that will recursively call itself after every finished game
    global gameFin, gameRunning
    # divide our connection by in_game and wait_list
    # randomly select 4 players
    Server.categorize(connected_players)

    # After categorizing our players a new game will start
    if(not gameRunning):
      gameRunning = True
    
    # assign each player in game a hand of tiles
    # and send msg that the game is starting
    Server.init_game()
    # proceed with main gameplay
    Server.main_gameplay()
    try:     
      print("game has ended \n winner is: {}".format(Player.getPlayerID(in_game[-1])))
      gameFin = True
      gameRunning = False
    except IndexError:
      print("TIE GAME")
      gameFin = True
      gameRunning = False

    # Game has finished
    # clear tiles in hand, and tiles placed for each player
    for player in connected_players:
      Player.clearHand(player)
      Player.clearTilesPlaced(player)

      # Notify each player a countdown for the next game has started
      Player.getPlayerConnection(player).send(tiles.MessageCountdown().pack())

    # Countdown to new game
    # Give players 5 sec until we start a new game
    Server.countdown(5)

    # Send every player connected a message that a new game is about to start
    for player in connected_players:
      Player.getPlayerConnection(player).send(tiles.MessageGameStart().pack())
    # clear the lists so another player can join (depending on the odds, random)
    if(gameFin == True):
      in_game.clear()
      live_idnums.clear() 
      wait_list.clear()
 
    gameRunning = False
    # Call the function again to play a new game, this will run while we have 
    # at least 2 players connected
    if(gameFin == True and len(connected_players) >= 2):
      Server.recursive_game()
    else:
      return


  def countdown(time):
    # Countdown function
    timer_fin = False
    while time > 0:
      print("{} seconds remaining".format(time))
      sleep(1)
      time -= 1
    if(time == 0):
      timer_fin = True
      print("Countdown ended")
    return timer_fin


  def receive_connection():
    # function to accept connections
    global in_game, connected_players
    # create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # listen on all network interfaces
    server_address = ('', 30020)
    try:
      sock.bind(server_address)
    except socket.error as e:
      print(str(e))
      
    print('listening on {}'.format(sock.getsockname()))

    # allow up to 9 queued (but not yet accepted) connections
    # (uncertain about how many spectators are allowed)
    sock.listen(9)

    while True:
      try:
        connection, client_address = sock.accept()
        print("received connection from {}".format(client_address))
        # Append the connected client to our connected_players global list
        Server.client_handler(connection, client_address)

      except socket.error as e:
        print(str(e))


  def start():
    # Function which uses threads to simultaniuosly run 

    # A thread that listens for new connections
    connection_thread = Thread(target=Server.receive_connection)

    # A thread that will continuously run the game
    game_thread = Thread(target=Server.recursive_game)

    # A thread that will continously categorize players, after each game
    player_thread = Thread(target=Server.categorize(connected_players))

    # Start thread to listen for connections
    connection_thread.start()

    # Start countdown, give players 10 seconds to join the game
    # game will start after countdown (10 sec)
    timer_result = Server.countdown(10)


    # if countdown ended, start the other 2 threads if there are enough players
    if timer_result == True:
      if(len(connected_players) >= 2):
        game_thread.start()
        player_thread.start()
      else:
        # wait another 10 seconds for connections
        timer_result2 = Server.countdown(10)
        if(timer_result2 == True):
          if(len(connected_players) < 2):
            return
          else:
            game_thread.start()
            player_thread.start()


# Start the server and the game
Server.start()



 



      
  
  








    

    
    







