# CITS3002 2021 Assignment
#
# This module defines essential constants and gameplay logic, which is shared
# by both the client and the server.
#
# This file MUST NOT be modified! The markers may use a different copy of the
# client, which will expect the constants and message definitions to exactly
# match the below.

import struct
from enum import IntEnum
from random import randrange


BOARD_WIDTH = 5  # width of the game board, in tiles
BOARD_HEIGHT = 5 # height of the game board in tiles
HAND_SIZE = 4    # number of tiles in each player's hand
PLAYER_LIMIT = 4 # maximum number of players in a single game
IDNUM_LIMIT = 65536 # player id number limit (used ids should be: 0 <= id < IDNUM_LIMIT)


class MessageType(IntEnum):
  """identify the kinds of messages that can be passed between server and
  client. each message will start with a value from this enumeration, so that
  the reader can determine how to interpret the remaining bytes in the message.
  """
  WELCOME = 1
  PLAYER_JOINED = 2
  PLAYER_LEFT = 3
  COUNTDOWN_STARTED = 4
  GAME_START = 5
  ADD_TILE_TO_HAND = 6
  PLAYER_TURN = 7
  PLACE_TILE = 8
  MOVE_TOKEN = 9
  PLAYER_ELIMINATED = 10


class MessageWelcome():
  """Sent by the server to joining clients, to notify them of their idnum."""

  def __init__(self, idnum: int):
    self.idnum = idnum
  
  def pack(self):
    return struct.pack('!HH', MessageType.WELCOME, self.idnum)
  
  @classmethod
  def unpack(cls, bs: bytearray):
    messagelen = struct.calcsize('!HH')

    if len(bs) >= messagelen:
      _, idnum = struct.unpack_from('!HH', bs, 0)
      return cls(idnum), messagelen
    
    return None, 0
  
  def __str__(self):
    return f"Welcome to the game! your ID is {self.idnum}."  

class MessagePlayerJoined():
  """Sent by the server to all clients, when a new client joins.
  This indicates the name and (unique) idnum for the new client.
  """

  def __init__(self, name: str, idnum: int):
    self.name = name
    self.idnum = idnum
  
  def pack(self):
    return struct.pack('!HHH{}s'.format(len(self.name)),
      MessageType.PLAYER_JOINED, self.idnum,
      len(self.name), bytes(self.name, 'utf-8'))
  
  @classmethod
  def unpack(cls, bs: bytearray):
    headerlen = struct.calcsize('!HHH')

    if len(bs) >= headerlen:
      _, idnum, namelen = struct.unpack_from('!HHH', bs, 0)
      if len(bs) >= headerlen + namelen:
        name, = struct.unpack_from('!{}s'.format(namelen), bs, headerlen)
        return MessagePlayerJoined(name, idnum), headerlen + namelen
    
    return None, 0
  
  def __str__(self):
    return f"Player {self.name} has joined the game!"  

class MessagePlayerLeft():
  """Sent by the server to all remaining clients, when a client leaves."""

  def __init__(self, idnum: int):
    self.idnum = idnum
  
  def pack(self):
    return struct.pack('!HH', MessageType.PLAYER_LEFT, self.idnum)
  
  @classmethod
  def unpack(cls, bs: bytearray):
    messagelen = struct.calcsize('!HH')

    if len(bs) >= messagelen:
      _, idnum = struct.unpack_from('!HH', bs, 0)
      return cls(idnum), messagelen
    
    return None, 0
  
  def __str__(self):
    return f"A player has left the game."  

class MessageCountdown():
  """Sent by the server to all clients, when the countdown for a new game has
  started.
  """

  def pack(self):
    return struct.pack('!H', MessageType.COUNTDOWN_STARTED)


class MessageGameStart():
  """Sent by the server to all clients, when a new game has started."""

  def pack(self):
    return struct.pack('!H', MessageType.GAME_START)


class MessageAddTileToHand():
  """Sent by the server to a single client, to add a new tile to that client's
  hand.
  """

  def __init__(self, tileid):
    self.tileid = tileid
  
  def pack(self):
    return struct.pack('!HH', MessageType.ADD_TILE_TO_HAND, self.tileid)
  
  @classmethod
  def unpack(cls, bs: bytearray):
    messagelen = struct.calcsize('!HH')

    if len(bs) >= messagelen:
      _, tileid = struct.unpack_from('!HH', bs, 0)
      return MessageAddTileToHand(tileid), messagelen
    
    return None, 0
  
  def __str__(self):
    return "Tiles are now added to your hand!"

class MessagePlayerTurn():
  """Sent by the server to all clients to indicate that a new turn has
  started.
  """

  def __init__(self, idnum: int):
    self.idnum = idnum
  
  def pack(self):
    return struct.pack('!HH', MessageType.PLAYER_TURN, self.idnum)
  
  @classmethod
  def unpack(cls, bs: bytearray):
    messagelen = struct.calcsize('!HH')

    if len(bs) >= messagelen:
      _, idnum = struct.unpack_from('!HH', bs, 0)
      return cls(idnum), messagelen
    
    return None, 0
  
  def __str__(self):
    return "A new turn has started!"  

class MessagePlaceTile():
  """Sent by the current player to the server to indicate that they want to
  place a tile from their hand in a particular location on the board.

  Sent by the server to all players to indicate that a player placed a tile onto
  the board.
  """

  def __init__(self, idnum: int, tileid: int, rotation: int, x: int, y: int):
    self.idnum = idnum
    self.tileid = tileid
    self.rotation = rotation
    self.x = x
    self.y = y
  
  def pack(self):
    return struct.pack('!HHHHHH', MessageType.PLACE_TILE, self.idnum,
      self.tileid, self.rotation, self.x, self.y)
  
  @classmethod
  def unpack(cls, bs: bytearray):
    messagelen = struct.calcsize('!HHHHHH')

    if len(bs) >= messagelen:
      _, idnum, tileid, rotation, x, y = struct.unpack_from('!HHHHHH', bs, 0)
      return MessagePlaceTile(idnum, tileid, rotation, x, y), messagelen
    
    return None, 0
  
  def __str__(self):
    return "A player placed his/her tile!"  

class MessageMoveToken():
  """Sent by the current player to the server on turn 2, to indicate which
  starting location they choose for their token.

  Sent by the server to all players to indicate the updated location of a
  player's token (either when they select the start location, or when a placed
  tile causes their token to move).
  """

  def __init__(self, idnum: int, x: int, y: int, position: int):
    self.idnum = idnum
    self.x = x
    self.y = y
    self.position = position
  
  def pack(self):
    return struct.pack('!HHHHH', MessageType.MOVE_TOKEN, self.idnum,
      self.x, self.y, self.position)
  
  @classmethod
  def unpack(cls, bs: bytearray):
    messagelen = struct.calcsize('!HHHHH')

    if len(bs) >= messagelen:
      _, idnum, x, y, position = struct.unpack_from('!HHHHH', bs, 0)
      return cls(idnum, x, y, position), messagelen
    
    return None, 0
  
  def __str__(self):
    return "Player has decided its starting position!"  

class MessagePlayerEliminated():
  """Sent by the server to all clients when a player is eliminated from the
  current game (either because their token left the board, or because the
  client disconnected).
  """

  def __init__(self, idnum: int):
    self.idnum = idnum
  
  def pack(self):
    return struct.pack('!HH', MessageType.PLAYER_ELIMINATED, self.idnum)
  
  @classmethod
  def unpack(cls, bs: bytearray):
    messagelen = struct.calcsize('!HH')

    if len(bs) >= messagelen:
      _, idnum = struct.unpack_from('!HH', bs, 0)
      return cls(idnum), messagelen
    
    return None, 0
  
  def __str__(self):
    return "A player has been eliminated!"  


def read_message_from_bytearray(bs: bytearray):
  """Attempts to read and unpack a single message from the beginning of the
  provided bytearray. If successful, it returns (msg, number_of_bytes_consumed).
  If unable to read a message (because there are insufficient bytes), it returns
  (None, 0).
  """

  msg = None
  consumed = 0

  typesize = struct.calcsize('!H')

  if len(bs) >= typesize:
    typeint, = struct.unpack_from('!H', bs, 0)

    if typeint == MessageType.WELCOME:
      msg, consumed = MessageWelcome.unpack(bs)
    
    elif typeint == MessageType.PLAYER_JOINED:
      msg, consumed = MessagePlayerJoined.unpack(bs)
    
    elif typeint == MessageType.PLAYER_LEFT:
      msg, consumed = MessagePlayerLeft.unpack(bs)

    elif typeint == MessageType.COUNTDOWN_STARTED:
      msg, consumed = MessageCountdown(), typesize
    
    elif typeint == MessageType.GAME_START:
      msg, consumed = MessageGameStart(), typesize
    
    elif typeint == MessageType.ADD_TILE_TO_HAND:
      msg, consumed = MessageAddTileToHand.unpack(bs)
    
    elif typeint == MessageType.PLAYER_TURN:
      msg, consumed = MessagePlayerTurn.unpack(bs)
    
    elif typeint == MessageType.PLACE_TILE:
      msg, consumed = MessagePlaceTile.unpack(bs)
    
    elif typeint == MessageType.MOVE_TOKEN:
      msg, consumed = MessageMoveToken.unpack(bs)
    
    elif typeint == MessageType.PLAYER_ELIMINATED:
      msg, consumed = MessagePlayerEliminated.unpack(bs)
  #print("MESSAGE@@@@@@@@@", msg, type(msg))
  return msg, consumed


def get_random_tileid():
  """Get a random, valid tileid."""
  return randrange(0, len(ALL_TILES))


class Board:
  """Stores the state of the board for a single game, and implements much of the
  game logic as far as token movement, valid tile placement, etc.
  """

  def __init__(self):
    self.width = BOARD_WIDTH
    self.height = BOARD_HEIGHT
    self.tileids = [None] * (BOARD_WIDTH * BOARD_HEIGHT)
    self.tilerotations = [None] * (BOARD_WIDTH * BOARD_HEIGHT)
    self.tileplaceids = [None] * (BOARD_WIDTH * BOARD_HEIGHT)
    self.tilerects = [None] * (BOARD_WIDTH * BOARD_HEIGHT)
    self.playerpositions = {}
    self.tile_size_px = 100

  def reset(self):
    """Reset the board to be empty, with no tiles or player tokens."""
    for i in range(len(self.tileids)):
      self.tileids[i] = None
      self.tilerotations[i] = None
      self.tileplaceids[i] = None
    
    self.playerpositions = {}

  def get_tile(self, x: int, y: int):
    """Get (tile id, rotation, placer id) for location x, y."""
    if x < 0 or x >= self.width:
      raise Exception('invalid x value')
    if y < 0 or y >= self.height:
      raise Exception('invalid y value')
    
    idx = self.tile_index(x, y)

    return self.tileids[idx], self.tilerotations[idx], self.tileplaceids[idx]
  
  def set_tile(self, x: int, y: int, tileid: int, rotation: int, idnum: int):
    """Attempt to place the given tile at position x,y.
    rotation: the rotation of the tile.
    idnum: id of the player that is placing the tile.

    If the tile cannot be placed, returns False, otherwise returns True.

    Note that this does not update the token positions.
    """

    if idnum in self.playerpositions:
      playerx, playery, _ = self.playerpositions[idnum]
      if x != playerx or y != playery:
        return False
    elif x != 0 and x != self.width - 1 and y != 0 and y != self.height - 1:
      return False
    
    idx = self.tile_index(x, y)

    if self.tileids[idx] != None:
      return False
    
    self.tileids[idx] = tileid
    self.tilerotations[idx] = rotation
    self.tileplaceids[idx] = idnum
    return True

  def have_player_position(self, idnum):
    """Check if the given player (by idnum) has a token on the board."""
    return idnum in self.playerpositions
  
  def get_player_position(self, idnum):
    """The given player (idnum) must have a token on the board before calling
    this method.
    
    Returns the player token's location as: x, y, position."""
    return self.playerpositions[idnum]
  
  def set_player_start_position(self, idnum, x: int, y: int, position: int):
    """Attempt to set the starting position for a player token.

    idnum: the player
    x, y: the square of the board
    position: position on the chosen square (0..7)

    If the player's token is already on the board, or the player did not place
    the tile at the given x,y location, or the chosen position does not touch
    the edge of the game board, then this method will return False and not
    change the state of the game board.

    Otherwise the player's token will be set to the given location, and the
    method will return True.
    """
    if self.have_player_position(idnum):
      return False
    
    # does the tile exist?
    idx = self.tile_index(x, y)
    if self.tileids[idx] == None:
      return False
    
    # does the player own the tile?
    if self.tileplaceids[idx] != idnum:
      return False

    # is position in tile valid?
    if (position == 0 or position == 1) and y != BOARD_HEIGHT - 1:
      return False
    if (position == 2 or position == 3) and x != BOARD_WIDTH - 1:
      return False
    if (position == 4 or position == 5) and y != 0:
      return False
    if (position == 6 or position == 7) and x != 0:
      return False

    self.update_player_position(idnum, x, y, position)

    return True
  
  def do_player_movement(self, live_idnums):
    """For all of the player ids in the live_idnums list, this method will move
    their player tokens if it is possible for them to move.

    That means that if the token is on a square that has a tile placed on it,
    the token will move across the connector to another edge of the tile, and
    then into the neighbouring square. If the neighbouring square also has a
    tile, the movement will continue in the same fashion. This process stops
    when the player's token reaches an empty square, or the edge of the game
    board.

    A tuple of two lists is returned: positionupdates, eliminated.

    positionupdates contains MessageMoveToken messages describing all of the
    updated token positions.

    eliminated contains a list of player ids that have been eliminated from the
    game by this movement phase (i.e. their token has just been moved to the
    edge of the game board).
    """
    positionupdates = []
    eliminated = []

    for idnum, playerposition in self.playerpositions.items():
      # don't keep moving expired players around
      if not idnum in live_idnums:
        continue

      x, y, position = playerposition
      idx = self.tile_index(x, y)
      moved = False

      while self.tileids[idx] != None:
        moved = True
        tileid = self.tileids[idx]
        rotation = self.tilerotations[idx]
        tile = ALL_TILES[tileid]
        exitposition = tile.getmovement(rotation, position)

        # determine next square to move into from this exit position
        dx, dy, dposition = CONNECTION_NEIGHBOURS[exitposition]
        nx = x + dx
        ny = y + dy

        # if that square would be off the board, we're eliminated
        if nx < 0 or nx >= BOARD_WIDTH or ny < 0 or ny >= BOARD_HEIGHT:
          position = exitposition
          eliminated.append(idnum)
          break
        
        # otherwise move into that square and continue the loop (if a tile is in the square)
        x, y, position = nx, ny, dposition
        idx = self.tile_index(x, y)
      
      if moved:
        self.update_player_position(idnum, x, y, position)
        positionupdates.append(MessageMoveToken(idnum, x, y, position))
    
    return positionupdates, eliminated

  # 
  # METHODS BELOW HERE ARE PRIVATE OR ONLY NEEDED BY THE CLIENT
  # -----------------------------------------------------------

  def tile_index(self, x: int, y :int):
    return x + y*self.width

  def update_player_position(self, idnum, x: int, y: int, position: int):
    self.playerpositions[idnum] = (x, y, position)
  
  def draw_squares(self, canvas, offset, onclick):
    for x in range(self.width):
      xpix = offset.x + x*self.tile_size_px
      for y in range(self.height):
        ypix = offset.y + y*self.tile_size_px
        tidx = self.tile_index(x, y)
        if not self.tilerects[tidx]:
          tid = canvas.create_rectangle(xpix, ypix,
            xpix+self.tile_size_px, ypix+self.tile_size_px, fill="#bbb", activefill="#fff",
            tags=('board_square', 'board_square_{}_{}'.format(x, y)))
          
          self.tilerects[tidx] = tid

          canvas.tag_bind(tid, "<Button-1>", lambda ev, x=x, y=y: onclick(x, y))
  
  def draw_tiles(self, canvas, offset):
    canvas.delete('board_tile')

    for x in range(self.width):
      xpix = offset.x + x*self.tile_size_px
      for y in range(self.height):
        ypix = offset.y + y*self.tile_size_px

        idx = self.tile_index(x, y)
        tileid = self.tileids[idx]

        if tileid != None:
          tile = ALL_TILES[tileid]
          rotation = self.tilerotations[idx]
          
          tile.draw(canvas, self.tile_size_px, Point(xpix, ypix), rotation,
            tags=('board_tile', 'board_tile_{}_{}'.format(x, y)))
          
          trect = self.tilerects[idx]
          if trect:
            canvas.itemconfigure(trect, fill="#bbb", activefill="#bbb")
    
    canvas.lift('selection_token')
  
  def draw_tokens(self, canvas, offset, playernums, eliminated):
    canvas.delete('token')

    for idnum, playerposition in self.playerpositions.items():
      x, y, position = playerposition

      xpix = offset.x + x*self.tile_size_px
      ypix = offset.y + y*self.tile_size_px

      playernum = playernums[idnum]
      playercol = PLAYER_COLOURS[playernum]

      if idnum in eliminated:
        playercol = '#ddd'

      delta = CONNECTION_LOCATIONS[position]

      cx = xpix + int(delta.x * self.tile_size_px)
      cy = ypix + int(delta.y * self.tile_size_px)

      canvas.create_oval(cx - 10, cy - 10, cx + 10, cy + 10,
        fill=playercol, outline='black', tags=('token'))

  def draw_selection_token(self, canvas, playernum, xpix: int, ypix: int, connector: int, callback):
    delta = CONNECTION_LOCATIONS[connector]

    cx = xpix + int(delta.x * self.tile_size_px)
    cy = ypix + int(delta.y * self.tile_size_px)

    playercol = PLAYER_COLOURS[playernum]

    tokenid = canvas.create_oval(cx - 10, cy - 10, cx + 10, cy + 10,
      fill=playercol, activefill="#fff", outline='black',
      tags=('selection_token'))
    
    canvas.tag_bind(tokenid, "<Button-1>", lambda ev: callback(connector))
  
  def draw_selection_tokens(self, canvas, offset, playernums, x: int, y: int, callback):
    idx = self.tile_index(x, y)
    tileid = self.tileids[idx]
    if tileid == None:
      print('no tileid at selection token location {}, {}!'.format(x, y))
      return
    
    playerid = self.tileplaceids[idx]
    playernum = playernums[playerid]

    xpix = offset.x + x*self.tile_size_px
    ypix = offset.y + y*self.tile_size_px

    if y == self.height - 1:
      print(' select bottom')
      self.draw_selection_token(canvas, playernum, xpix, ypix, 0, callback)
      self.draw_selection_token(canvas, playernum, xpix, ypix, 1, callback)
    if x == self.width - 1:
      print(' select right')
      self.draw_selection_token(canvas, playernum, xpix, ypix, 2, callback)
      self.draw_selection_token(canvas, playernum, xpix, ypix, 3, callback)
    if y == 0:
      print(' select top')
      self.draw_selection_token(canvas, playernum, xpix, ypix, 4, callback)
      self.draw_selection_token(canvas, playernum, xpix, ypix, 5, callback)
    if x == 0:
      print(' select left')
      self.draw_selection_token(canvas, playernum, xpix, ypix, 6, callback)
      self.draw_selection_token(canvas, playernum, xpix, ypix, 7, callback)


#
# EVERYTHING BELOW HERE IS PRIVATE OR ONLY NEEDED BY THE CLIENT
# -------------------------------------------------------------

class Tile:
  def __init__(self, connections):
    if len(connections) != 4:
      raise RuntimeError("Tile must have exactly 8 connections")
    
    self.nextpoint = [None] * 8

    for i in range(4):
      a, b = connections[i]
      if a == b:
        raise RuntimeError("Connection must not loop back to itself")
      if a < 0 or a >= 8 or b < 0 or b >= 8:
        raise RuntimeError("Invalid connection ports {}, {}".format(a, b))
      if self.nextpoint[a] != None:
        raise RuntimeError("Connection port {} set multiple times".format(a))
      if self.nextpoint[b] != None:
        raise RuntimeError("Connection port {} set multiple times".format(b))
      self.nextpoint[a] = b
      self.nextpoint[b] = a
    
    self.connections = connections
  
  def getmovement(self, rotation, fromposition):
    unrotated = ((fromposition-2*rotation)+8)%8
    nextposition = self.nextpoint[unrotated]
    nextposition = (nextposition+2*rotation)%8
    return nextposition
  
  def draw(self, canvas, size_px, basepoint, rotation, tags):
    for i in range(4):
      a, b = self.connections[i]

      apos = CONNECTION_LOCATIONS[(a+2*rotation)%8]
      bpos = CONNECTION_LOCATIONS[(b+2*rotation)%8]

      ax = basepoint.x + int(apos.x * size_px)
      ay = basepoint.y + int(apos.y * size_px)

      bx = basepoint.x + int(bpos.x * size_px)
      by = basepoint.y + int(bpos.y * size_px)

      canvas.create_line(ax, ay, bx, by, width=3,
        fill="#000000", activefill="#66ccee", tags=tags)


ALL_TILES = [Tile(x) for x in [
  [(0, 5), (1, 2), (3, 6), (4, 7)],
  [(0, 5), (1, 4), (2, 6), (3, 7)],
  [(0, 7), (1, 2), (3, 4), (5, 6)],
  [(0, 5), (1, 4), (2, 7), (3, 6)],

  [(0, 7), (1, 6), (2, 5), (3, 4)],
  [(0, 2), (1, 3), (4, 6), (5, 7)],
  [(0, 4), (1, 5), (2, 6), (3, 7)],
  [(0, 7), (1, 2), (3, 5), (4, 6)],

  [(0, 5), (1, 7), (2, 4), (3, 6)],
  [(0, 4), (1, 2), (3, 6), (5, 7)],
  [(0, 2), (1, 5), (3, 6), (4, 7)]
]]

PLAYER_COLOURS = [
  '#4477AA', # blue
  '#EE6677', # red
  '#228833', # green
  '#CCBB44'  # yellow
]

if PLAYER_LIMIT > len(PLAYER_COLOURS):
  raise Exception('Need to define more player colours!')

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

CONNECTION_LOCATIONS = [
  Point( 0.25, 1.0),
  Point( 0.75, 1.0),
  Point( 1.0,  0.75),
  Point( 1.0,  0.25),
  Point( 0.75, 0.0),
  Point( 0.25, 0.0),
  Point( 0.0,  0.25),
  Point( 0.0,  0.75)
]

CONNECTION_NEIGHBOURS = [
  # dx, dy, position
  ( 0,  1,  5),
  ( 0,  1,  4),
  ( 1,  0,  7),
  ( 1,  0,  6),
  ( 0, -1,  1),
  ( 0, -1,  0),
  (-1,  0,  3),
  (-1,  0,  2)
]
