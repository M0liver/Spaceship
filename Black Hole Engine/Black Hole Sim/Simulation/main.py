import signal
import sys
import GravityGenNewt
import Data
import struct
import time
import zmq


# Globals
#     A single character 'A'
#     Three integers: 1, 2, 3
#     Fourteen double precision floats: 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.1, 11.1, 12.1, 13.1, 14.1
sensor_data = (b'A', 1, 2, 3, 0.0, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.1, 11.1, 12.1)
sensor_data_format = '<ciiidddddddddddd'
sample_binary = struct.pack(sensor_data_format, *sensor_data)
black_hole_data = .2
black_hole_data_format = '<f'


def signal_handler(sig, frame):
    print('Shutdown signal received. Exiting...')
    sys.exit(0)


def create_send_socket(context, port):
    socket = context.socket(zmq.PUSH)
    socket.bind(f"tcp://*:{port}")
    return socket


def create_receive_socket(context, port):
    socket = context.socket(zmq.PULL)
    socket.connect(f"tcp://localhost:{port}")
    return socket


def send_data(socket, data):
    packed_data = struct.pack(black_hole_data_format, *data)
    socket.send(packed_data, zmq.NOBLOCK)


def receive_data(socket):
    try:
        packed_data = socket.recv(zmq.NOBLOCK)
        data = struct.unpack(black_hole_data_format, packed_data)
        return data
    except zmq.Again as e:
        # No message received yet
        return None


# The sim is waiting until it receives a struct.  This struct is the "sensor".
# The struct will need some sort of ID so that the sim knows what sensor it is and what information it needs.
# Once the struct is received the ml (main loop) will determine which sensor it received and then calculate
# the relevant data.
# The ML will then send back the information to the sensor and wait until it receives another struct
# The "information packet" should be a generic struct as there will be a lot of shared data amongst the sensors
# ML will exit upon receiving a shutdown signal
def main():
    # Create the context
    context = zmq.Context
    # Set the signal handler for SIGINT
    signal.signal(signal.SIGINT, signal_handler)

    # Create send and receive sockets
    send_socket = create_send_socket(context, 5555)
    receive_socket = create_receive_socket(context, 5555)

    print("Starting loop. Press Ctrl+C to exit.")

    # Infinite loop until sig   nal received
    while True:
        # TODO: Throw in a wait so that it's not doing this as fast as possible
        bin_data = Data.Data(sample_binary)
        match bin_data.sensorID:
            case b'A':
                pv = GravityGenNewt.PointVector(bin_data.xCo, bin_data.yCo, bin_data.zCo, bin_data.sensVect)
                fv = GravityGenNewt.calculate_gravitational_force(pv)
            case _:
                print("Unknown Sensor")
                sys.exit(1)

        print(f"Force vector: {fv}")
        send_data(send_socket, black_hole_data)
        updated_black_hole_info = receive_data(receive_socket)
        if updated_black_hole_info:
            print(f"New black hole info: {updated_black_hole_info}")
        time.sleep(1)


if __name__ == "__main__":
    main()
