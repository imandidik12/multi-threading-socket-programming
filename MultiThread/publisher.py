import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 7777))
topic = ''


def init_publisher():
    global topic
    nama_topik = input('input topic name : ')
    requestdata = 'publisher|__init__|{}'.format(nama_topik)
    sock.send(requestdata.encode("ascii"))
    respon = sock.recv(100)
    topic = nama_topik
    return respon.decode("ascii")


def serving_data():
    kirimdata = input('sent data to subscriber : ')
    request = "publisher|{}|{}".format(str(topic), str(kirimdata))
    sock.send(request.encode("ascii"))
    respon = sock.recv(100)
    print(respon.decode("ascii"))

    interaksi = input("Add more data ? y/n ")
    if interaksi == 'y':
        return True
    elif interaksi == 'n':
        print('thank u')
        return False
    else:
        print('provide only "y / n"')
        return False


def main():
    if init_publisher() != 'False':
        while True:
            if not serving_data():
                break
    else:
        print('Topic already exist')
        main()


main()
