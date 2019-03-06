import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("0.0.0.0", 7777))
sock.listen(100)
list_publisher = []


class Publisher:
    def __init__(self, topic, conn):
        self.Topic = topic
        self.connection = conn
        self.data_list = []

    def publish(self):
        if len(self.data_list) == 0:
            return 'publisher have not set any data'
        else:
            data = ''
            i = 0
            for x in self.data_list:
                i = i + 1
                data += '{}.\t {} \n'.format(i, x)
            return data


def ascii_decoder(encoded_data):
    return encoded_data.decode('ascii')


def ascii_encoder(decoded_data):
    return decoded_data.encode('ascii')


def client_type(request_string):
    tipe = request_string.split('|')
    if tipe[0] == 'publisher':
        return True
    else:
        return False


def create_publisher(connection, topic):
    return Publisher(topic,connection)


def is_topic_exist(topic, publisher_list):
    exist = False
    for x in publisher_list:
        if x.Topic == topic:
            exist = True
    return exist


def find_topic(topic, publisher_list):
    obj = {}
    for x in publisher_list:
        print(x.Topic)
        if x.Topic == topic:
            obj = x
    return obj


def handler(connection):
    while True:
        try:
            data = connection.recv(100)
            decoded_data = ascii_decoder(data)
            if client_type(decoded_data):
                request_data = decoded_data.split('|')
                if request_data[1] == '__init__':
                    if is_topic_exist(request_data[2], list_publisher):
                        connection.send(ascii_encoder('False'))
                    else:
                        list_publisher.append(create_publisher(connection, request_data[2]))
                        connection.send(ascii_encoder('you are publisher now create some data for subscriber'))
                else:
                    publisher = find_topic(request_data[1],list_publisher)
                    publisher.data_list.append(request_data[2])
                    connection.send(ascii_encoder('Ok'))

            else:
                request_data = decoded_data.split('|')
                if is_topic_exist(request_data[1], list_publisher):
                    publisher = find_topic(request_data[1], list_publisher)
                    response = publisher.publish()
                    connection.send(ascii_encoder(response))
                else:
                    response = 'Topic not found'
                    connection.send(ascii_encoder(response))

        except socket.error:
            connection.close()
            break


def main():
    while True:
        connection, client_address = sock.accept()
        thread = threading.Thread(target=handler, args=(connection,))
        thread.start()


main()
