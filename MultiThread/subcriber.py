# import socket
import socket

# Inisiasi socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Kirim permintaan koneksi
sock.connect(("127.0.0.1", 7777))
while True :
    # Kirim data ke server
    nama_topik = input('select topic : ')
    requestdata = 'subscriber|{}'.format(nama_topik)
    sock.send(requestdata.encode("ascii"))
    respon = sock.recv(100)
    print(respon.decode("ascii"))
