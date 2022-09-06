# CITS3002 2021 Assignment
#
# This file implements the game client. You do not need to understand this code,
# but you may like to inspect it to understand how the client expects to
# interact with the server.
#
# If you are going to modify this code (e.g. to add additional information to
# help you debug your servers), you should make a copy of the original code
# first, and ensure that your final server works with the original code
# before submission.

from tkinter import *
from tkinter.ttk import *
import tiles
import random
import socket
import sys
import threading
import select

class Application(Frame):
  TILE_PX = 80 # pixels
  BORDER_PX = 50 # pixels
  HAND_SPACING_PX = 10 # pixels

  BOARD_WIDTH = tiles.BOARD_WIDTH
  BOARD_HEIGHT = tiles.BOARD_HEIGHT
  HAND_SIZE = tiles.HAND_SIZE

  BOARD_WIDTH_PX = TILE_PX * BOARD_WIDTH
  BOARD_HEIGHT_PX = TILE_PX * BOARD_HEIGHT
  HAND_WIDTH_PX = TILE_PX * HAND_SIZE + HAND_SPACING_PX * (HAND_SIZE - 1)

  CANVAS_WIDTH_PX = max(BOARD_WIDTH_PX, HAND_WIDTH_PX) + 2 * BORDER_PX
  CANVAS_HEIGHT_PX = BOARD_HEIGHT_PX + TILE_PX + 3 * BORDER_PX

  def __init__(self, parent=None):
    super().__init__(parent)
    self.parent = parent
    self.pack()

    self.sock = None

    self.infolock = threading.Lock()
    self.idnum = None
    self.playernames = {} # idnum -> player name

    self.handlock = threading.Lock()
    self.hand_offset = tiles.Point(
      (Application.CANVAS_WIDTH_PX - Application.HAND_WIDTH_PX) / 2,
      2 * Application.BORDER_PX + Application.BOARD_HEIGHT_PX)
    self.hand = [None] * Application.HAND_SIZE
    self.handrotations = [0] * Application.HAND_SIZE

    self.boardlock = threading.Lock()
    self.board = tiles.Board()
    self.board.tile_size_px = Application.TILE_PX
    self.lasttilelocation = None
    self.location = None
    self.playernums = {} # idnum -> player number (turn order)
    self.playerlist = []
    self.playerlistvar = StringVar(value=self.playerlist)
    self.eliminatedlist = []
    self.currentplayerid = None

    self.boardoffset = tiles.Point(Application.BORDER_PX, Application.BORDER_PX)

    self.selected_hand = 0
    self.handrects = [None] * Application.HAND_SIZE

    self.bind('<<ClearBoard>>', lambda ev: self.clear_board())
    self.bind('<<RedrawBoard>>', lambda ev: self.draw_board())
    self.bind('<<RedrawHand>>', lambda ev: self.draw_hand())
    self.bind('<<RedrawTokens>>', lambda ev: self.draw_tokens())
    self.bind('<<RedrawTurn>>', lambda ev: self.draw_turn())
    self.bind('<<CloseConnection>>', lambda ev: on_quit())

    self.create_widgets()
  
  def create_widgets(self):
    frame = Frame(self, width=Application.CANVAS_WIDTH_PX + 200, height=Application.CANVAS_HEIGHT_PX)
    frame.grid(column=0, row=0)

    self.canvas = Canvas(frame, width=Application.CANVAS_WIDTH_PX,
      height=Application.CANVAS_HEIGHT_PX, bg="white")

    self.board.draw_squares(self.canvas, self.boardoffset, self.play_tile)

    message_x = Application.CANVAS_WIDTH_PX / 2
    message_y = Application.BORDER_PX / 2

    self.your_turn_text = self.canvas.create_text(message_x, message_y, anchor='center', text='Your turn!', fill='black', state='hidden')
    self.eliminated_text = self.canvas.create_text(message_x, message_y, anchor='center', text='You were eliminated!', fill='black', state='hidden')
    self.you_won_text = self.canvas.create_text(message_x, message_y, anchor='center', text='You won!', fill='black', state='hidden')

    hand_offset = self.hand_offset
    
    for i in range(len(self.hand)):
      cid = self.canvas.create_rectangle(hand_offset.x + (Application.TILE_PX + Application.HAND_SPACING_PX) * i,
        hand_offset.y,
        hand_offset.x + (Application.TILE_PX + Application.HAND_SPACING_PX) * i + Application.TILE_PX,
        hand_offset.y + Application.TILE_PX,
        fill='#bbb', outline='#000', width=2,
        tags=('hand_rect', 'hand_rect_{}'.format(i)))
      
      self.handrects[i] = cid

      self.canvas.tag_bind(cid, "<Button-1>", lambda ev, i=i: self.rotate_hand_tile(ev, i))
    
    self.set_selected_hand(0)
    
    self.board.draw_tiles(self.canvas, self.boardoffset)

    self.canvas.grid(column=0, row=0, columnspan=1, rowspan=2)

    self.quit = Button(frame, text="QUIT", command=on_quit)
    self.quit.grid(column=1, row=0, sticky='n')

    self.playerlistbox = Listbox(frame, listvariable=self.playerlistvar)
    self.playerlistbox.grid(column=1, row=1, sticky='s')

  def set_selected_hand(self, index):
    self.canvas.itemconfigure('hand_rect', fill='#bbb', outline='#000', width=2)

    self.selected_hand = index
    self.canvas.itemconfigure('hand_rect_{}'.format(index), fill='#fff', outline='#bbb', width=4)

  def play_tile(self, x, y):
    if self.lasttilelocation != None and self.location == None:
      return
    
    print('play tile at {}, {}'.format(x, y))

    if self.sock:
      with self.infolock:
        idnum = self.idnum
        if idnum != None:
          with self.handlock:
            tileid = self.hand[self.selected_hand]
            rotation = self.handrotations[self.selected_hand]
            if tileid != None:
              self.sock.send(tiles.MessagePlaceTile(idnum, tileid, rotation, x, y).pack())

  def rotate_hand_tile(self, ev, hand_index):
    if hand_index == self.selected_hand:
      with self.handlock:
        self.handrotations[hand_index] = (self.handrotations[hand_index] + 1) % 4
      self.draw_hand()
    else:
      self.set_selected_hand(hand_index)
  
  def choose_starting_token(self, position):
    with self.boardlock:
      if self.lasttilelocation and not self.location:
        x, y = self.lasttilelocation
        print('start at {},{}:{}'.format(x, y, position))
        self.sock.send(tiles.MessageMoveToken(self.idnum, x, y, position).pack())
  
  def clear_board(self):
    self.canvas.configure(bg='white')
    self.canvas.itemconfigure('board_square', fill="#bbb", activefill="#fff")
    self.canvas.delete('board_tile')
    self.canvas.delete('selection_token')
    self.canvas.delete('token')
  
  def draw_board(self):
    self.board.draw_tiles(self.canvas, self.boardoffset)
  
  def draw_hand(self):
    hand_offset = self.hand_offset

    self.canvas.delete('handtile')

    with self.handlock:
      for i in range(len(self.hand)):
        if self.hand[i] != None:
          drawpoint = tiles.Point(hand_offset.x + (Application.TILE_PX + 10) * i, hand_offset.y)
          tile = tiles.ALL_TILES[self.hand[i]]
          tile.draw(self.canvas, Application.TILE_PX, drawpoint, self.handrotations[i], ('handtile'))
  
  def draw_tokens(self):
    with self.boardlock:
      if self.lasttilelocation and not self.location:
        x, y = self.lasttilelocation
        self.board.draw_selection_tokens(self.canvas, self.boardoffset, self.playernums, x, y, self.choose_starting_token)
      else:
        self.canvas.delete('selection_token')
      
      self.board.draw_tokens(self.canvas, self.boardoffset, self.playernums, self.eliminatedlist)
  
  def draw_turn(self):
    self.canvas.itemconfigure(self.you_won_text, state='hidden')
    self.canvas.itemconfigure(self.eliminated_text, state='hidden')
    self.canvas.itemconfigure(self.your_turn_text, state='hidden')

    if self.idnum in self.playernums:
      if self.idnum in self.eliminatedlist:
        self.canvas.itemconfigure(self.eliminated_text, state='normal')
      elif self.eliminatedlist and len(self.playerlist) == 1:
        self.canvas.itemconfigure(self.you_won_text, state='normal')
      elif self.currentplayerid == self.idnum:
        self.canvas.itemconfigure(self.your_turn_text, state='normal')
      
      playernum = self.playernums[self.idnum]
      playercolour = tiles.PLAYER_COLOURS[playernum]
      self.canvas.configure(bg=playercolour)
      

Tcl().eval('set tcl_platform(threaded)')

exited = False

root = Tk()

def on_quit():
  global exited
  exited = True
  root.destroy()

root.protocol("WM_DELETE_WINDOW", on_quit)

app = Application(parent=root)
app.parent.title("Client")

def reset_game_state():
  print('resetting game state')

  with app.handlock:
    for i in range(len(app.hand)):
      app.hand[i] = None
      app.handrotations[i] = 0
  
  app.event_generate("<<RedrawHand>>")

  with app.boardlock:
    app.board.reset()
    app.lasttilelocation = None
    app.location = None
    app.playernums = {}
    app.playerlist.clear()
    app.eliminatedlist.clear()
    app.currentplayerid = None
  
  app.event_generate("<<ClearBoard>>")
  app.event_generate("<<RedrawBoard>>")
  app.event_generate("<<RedrawTurn>>")

def set_player_turn(idnum):
  with app.boardlock:
    if not idnum in app.playernums:
      playernum = len(app.playernums)
      app.playernums[idnum] = playernum

      with app.infolock:
        playername = app.playernames[idnum]
        app.playerlist.append(playername)
      
      app.playerlistvar.set(app.playerlist)
    
    app.currentplayerid = idnum

  app.event_generate("<<RedrawTurn>>")

def set_player_eliminated(idnum):
  with app.boardlock:
    with app.infolock:
      if idnum in app.playernames:
        playername = app.playernames[idnum]
        app.playerlist.remove(playername)
      else:
        print('Unknown player eliminated: {}'.format(idnum))
    app.playerlistvar.set(app.playerlist)

    if not idnum in app.eliminatedlist:
      app.eliminatedlist.append(idnum)
  
  app.event_generate("<<RedrawTokens>>")
  app.event_generate("<<RedrawTurn>>")

def tile_placed(msg):
  print('tile {} at {}, {} : {} from {}'.format(msg.tileid, msg.x, msg.y, msg.rotation, msg.idnum))

  with app.boardlock:
    # we don't use board.set_tile() here, because we trust the server, and we're
    # not worried if it sends a tile placement that looks illegal. this might
    # legitimately happen when, e.g. we join an existing game and the server
    # is catching us up on the current game state
    idx = app.board.tile_index(msg.x, msg.y)
    app.board.tileids[idx] = msg.tileid
    app.board.tilerotations[idx] = msg.rotation
    app.board.tileplaceids[idx] = msg.idnum
  
  app.event_generate("<<RedrawBoard>>")

  with app.infolock:
    if app.idnum == msg.idnum:
      with app.handlock:
        selected = app.selected_hand

        if app.hand[selected] != msg.tileid:
          try:
            selected = app.hand.index(msg.tileid)
          except ValueError:
            return
        
        app.hand[selected] = None
        app.handrotations[selected] = 0
      
      app.event_generate("<<RedrawHand>>")

      redrawtokens = False

      with app.boardlock:
        app.lasttilelocation = (msg.x, msg.y)
        if app.location == None:
          redrawtokens = True
      
      if redrawtokens:
        app.event_generate("<<RedrawTokens>>")

def token_moved(msg):
  with app.boardlock:
    if msg.idnum == app.idnum:
      print('Setting own location')
      app.location = (msg.x, msg.y, msg.position)
    app.board.update_player_position(msg.idnum, msg.x, msg.y, msg.position)
  
  app.event_generate("<<RedrawTokens>>")

def add_tile_to_hand(tileid):
  with app.handlock:
    for i in range(len(app.hand)):
      if app.hand[i] == None:
        app.hand[i] = tileid
        app.handrotations[i] = 0
        break
  app.event_generate("<<RedrawHand>>")

def communication_thread(sock):
  buffer = bytearray()

  while True:
    try:
      chunk = sock.recv(4096)
      if chunk:
        # Read a chunk from the socket, and add it to the end of our buffer
        # (in case we had a partial message in the buffer from a previous
        # chunk, and we need the new chunk to complete it)
        buffer.extend(chunk)

        # Unpack as many messages as we can from the buffer.
        while True:
          msg, consumed = tiles.read_message_from_bytearray(buffer)
          
          if consumed:
            buffer = buffer[consumed:]

            if isinstance(msg, tiles.MessageWelcome):
              print('Welcome!')
              with app.infolock:
                app.idnum = msg.idnum
                app.playernames[app.idnum] = 'Me!'
            
            elif isinstance(msg, tiles.MessagePlayerJoined):
              print('Player {} joined, id {}'.format(msg.name, msg.idnum))
              with app.infolock:
                app.playernames[msg.idnum] = msg.name
            
            elif isinstance(msg, tiles.MessagePlayerLeft):
              print('Player id {} left'.format(msg.idnum))
              with app.infolock:
                if msg.idnum in app.playernames:
                  del app.playernames[msg.idnum]
                else:
                  print("...I didn't know they were a player!")
            
            elif isinstance(msg, tiles.MessageCountdown):
              print('Countdown starting...')
            
            elif isinstance(msg, tiles.MessageGameStart):
              print('Game starting...')
              reset_game_state()
            
            elif isinstance(msg, tiles.MessageAddTileToHand):
              print('Add tile {} to hand'.format(msg.tileid))
              tileid = msg.tileid
              
              if tileid < 0 or tileid >= len(tiles.ALL_TILES):
                raise RuntimeError('Unknown tile index {}'.format(tileid))
              
              add_tile_to_hand(tileid)
            
            elif isinstance(msg, tiles.MessagePlayerTurn):
              print('Player turn: {}'.format(msg))

              with app.infolock:
                if msg.idnum not in app.playernames:
                  raise RuntimeError('Unknown playerid {}'.format(msg.idnum))
              
              set_player_turn(msg.idnum)
            
            elif isinstance(msg, tiles.MessagePlaceTile):
              print('Place tile: {}'.format(msg))

              with app.infolock:
                if msg.idnum not in app.playernames:
                  raise RuntimeError('Unknown playerid {}'.format(msg.idnum))
              
              tile_placed(msg)
            
            elif isinstance(msg, tiles.MessageMoveToken):
              print('Move token: {}'.format(msg))

              with app.infolock:
                if msg.idnum not in app.playernames:
                  raise RuntimeError('Unknown playerid {}'.format(msg.idnum))
              
              token_moved(msg)
            
            elif isinstance(msg, tiles.MessagePlayerEliminated):
              print('Player eliminated: {}'.format(msg))

              with app.infolock:
                if msg.idnum not in app.playernames:
                  raise RuntimeError('Unknown playerid {}'.format(msg.idnum))
              
              set_player_eliminated(msg.idnum)
            
            else:
              print('Unknown message: {}'.format(msg))
          else:
            break
      else:
        break
    except Exception as e:
      print('Error: {}'.format(e))
      break
  
  print('Server closed connection')

  if not exited:
    app.event_generate('<<CloseConnection>>')


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_host = 'localhost'
if len(sys.argv) > 2:
  server_host = sys.argv[1]

print('Using server hostname {}'.format(server_host))

server_address = (server_host, 30020)
sock.connect(server_address)

sock.setblocking(True)

comthread = threading.Thread(target=communication_thread, args=[sock])
comthread.start()

try:
  app.sock = sock
  app.mainloop()
finally:
  print('closing sock')
  sock.shutdown(socket.SHUT_WR)
  sock.close()

comthread.join()
