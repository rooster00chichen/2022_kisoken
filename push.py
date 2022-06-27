import socket
import time
import sys
from csv import reader

HOST = '127.0.0.1'  # 当日メッセージを送りたいPC
PORT = 50007  # 任意のport
i = 0
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
with open('干渉波形.csv', 'r') as csv_file:
    csv_reader = reader(csv_file)
    # Passing the cav_reader object to list() to get a list of lists
    list_num = list(csv_reader)

while True:
    try:
        text = str(list_num[i % 5001][1]).encode("utf-8")
        print(text)
        client.sendto(text, (HOST, PORT))
        i += 1
        time.sleep(10*10**-3)
    except KeyboardInterrupt:  # 終了時の処理
        sys.exit()
