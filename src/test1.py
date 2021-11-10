from os import O_TMPFILE
from PIL import Image


def invert_line(img):
  m = img.height // 2         # milieu de l'image
  pixels = img.load()         # tableau des pixels

  for x in range(0, img.width):
    r, g, b = pixels[x, m]  # on récupère les composantes RGB du pixel (x,m)
    r = r ^ 0b11111111      # on les inverse bit à bit avec un XOR
    g = g ^ 0b11111111      # ...
    b = b ^ 0b11111111      # ...
    pixels[x, m] = r, g, b  # on remet les pixels inversés dans le tableau

def invert_half(img):
  m = img.height // 2         # milieu de l'image
  pixels = img.load()         # tableau des pixels

  for line in range(m, img.height):
    for x in range(0, img.width):
      r, g, b = pixels[x, line]  # on récupère les composantes RGB du pixel (x,m)
      r = r ^ 0b11111111      # on les inverse bit à bit avec un XOR
      g = g ^ 0b11111111      # ...
      b = b ^ 0b11111111      # ...
      pixels[x, line] = r, g, b  # on remet les pixels inversés dans le tableau

def hide_message_length(img, messageLength):
  pixels = img.load()
  r, g, b = pixels[0, 0]

  if (messageLength > 511):
    print("error, message will be truncated to 511 bits")

  messageLength = min(messageLength, 511)

  r = (r & 0b11111000) | (messageLength & 0b00000111)
  g = (g & 0b11111000) | ((messageLength & 0b00111000) >> 3)
  b = (b & 0b11111100) | ((messageLength & 0b11000000) >> 6)

  pixels[0, 0] = r, g, b 

def hide_message(img, msg):
  hide_message_length(img, len(msg))

  pixels = img.load()
  width = img.width

  i = 1
  for c in msg:
    col = i % width
    row = i // width
    r, g, b = pixels[col, row]
    r = (r & 0b11111000) | (ord(c) & 0b00000111)
    g = (g & 0b11111000) | ((ord(c) & 0b00111000) >> 3)
    b = (b & 0b11111100) | ((ord(c) & 0b11000000) >> 6)
    pixels[col, row] = r, g, b  # on remet les pixels inversés dans le tableau
    i += 1

def retrieve_hidden_message(img):
  message_length = retrieve_hidden_message_length(img)

  pixels = img.load()
  width = img.width

  message = []

  for i in range(1, message_length+1):
    col = i % width
    row = i // width
    r, g, b = pixels[col, row]
    bits1 = r & 0b0000111
    bits2 = g & 0b0000111
    bits3 = b & 0b0000011

    message.append(chr(int(bits1 + (bits2 << 3) + (bits3 << 6))))

  print(message)

def retrieve_hidden_message_length(img):
  pixels = img.load()

  r, g, b = pixels[0, 0]

  bits1 = r & 0b00000111
  bits2 = g & 0b00000111
  bits3 = b & 0b00000011

  return int(bits1 + (bits2 << 3) + (bits3 << 6))

def main(filename, output):
  img = Image.open(filename)  # ouverture de l'image contenue dans un fichier

  hide_message(img,"fhizpbfuezobuzodqudodfbudqbudqobduofduqogeùhduoôb")
  img.save(output)            # sauvegarde de l'image obtenue dans un autre fichier

  img2 = Image.open("./resources/test_out.png")
  retrieve_hidden_message(img2)