import signal
import sys
import GravityGenNewt
import Data
import struct


# Globals
#     A single character 'A'
#     Three integers: 1, 2, 3
#     Fourteen double precision floats: 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.1, 11.1, 12.1, 13.1, 14.1
data = (b'A', 1, 2, 3, 0.0, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.1, 11.1, 12.1)
sample_binary = struct.pack('<ciiidddddddddddd', *data)


def signal_handler(sig, frame):
    print('Shutdown signal received. Exiting...')
    sys.exit(0)


# The sim is waiting until it receives a struct.  This struct is the "sensor".
# The struct will need some sort of ID so that the sim knows what sensor it is and what information it needs.
# Once the struct is received the ml (main loop) will determine which sensor it received and then calculate
# the relevant data.
# The ML will then send back the information to the sensor and wait until it receives another struct
# The "information packet" should be a generic struct as there will be a lot of shared data amongst the sensors
# ML will exit upon receiving a shutdown signal
def main():
    # Set the signal handler for SIGINT
    signal.signal(signal.SIGINT, signal_handler)

    print("Starting loop. Press Ctrl+C to exit.")

    # Infinite loop until signal received
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


if __name__ == "__main__":
    main()
