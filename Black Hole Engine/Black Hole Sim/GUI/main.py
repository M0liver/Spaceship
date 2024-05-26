import tkinter as tk
from tkinter import messagebox
import zmq
import struct
import sys


class ZMQTkinterApp:
    def __init__(self, r):
        self.close_button = None
        self.submit_button = None
        self.entry = None
        self.label = None
        self.root = root
        self.root.title("Input Validation Example")

        self.context = zmq.Context()
        self.receive_socket = self.context.socket(zmq.PULL)
        self.receive_socket.bind("tcp://*:5555")
        self.send_socket = self.context.socket(zmq.PUSH)
        self.send_socket.connect("tcp://localhost:5556")

        self.data_format = 'f'
        self.valid_number = None

        self.create_entry_widget_with_validation()
        self.create_close_button()
        self.create_display_label()

        self.root.after(100, self.check_for_updates)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_entry_widget_with_validation(self):
        def is_valid_number(number_str):
            try:
                number = float(number_str)
                if 1 < number < sys.float_info.max:
                    return True, number
                else:
                    return False, None
            except ValueError:
                return False, None

        def submit_text():
            entered_text = self.entry.get()
            is_valid, number = is_valid_number(entered_text)
            if is_valid:
                print(f"Valid entered number: {number}")
                self.valid_number = number
            else:
                messagebox.showerror("Invalid Input",
                                     f"Please enter a valid positive number between 1 and {sys.float_info.max}")

        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack(pady=10)

        self.submit_button = tk.Button(self.root, text="Enter", command=submit_text)
        self.submit_button.pack(pady=10)

    def create_close_button(self):
        def on_closing():
            self.context.term()
            self.root.destroy()

        self.close_button = tk.Button(self.root, text="Close", command=on_closing)
        self.close_button.pack(pady=10)

    def create_display_label(self):
        self.label = tk.Label(self.root, text="Waiting for data...")
        self.label.pack(pady=20)

    def receive_data(self, socket):
        try:
            packed_data = socket.recv(zmq.NOBLOCK)
            data = struct.unpack(self.data_format, packed_data)
            return data
        except zmq.Again:
            return None

    def send_data(self, socket, data):
        packed_data = struct.pack(self.data_format, *data)
        socket.send(packed_data, zmq.NOBLOCK)

    def update_gui_with_data(self, data):
        self.label.config(text=f"Received data: {data}")

    def check_for_updates(self):
        received_data = self.receive_data(self.receive_socket)
        if received_data:
            print(f"Received data: {received_data}")
            self.update_gui_with_data(received_data)

            updated_data = (received_data[0] + 1, received_data[1] + 1, received_data[2] + 1.0)
            self.send_data(self.send_socket, updated_data)
            print(f"Sent updated data: {updated_data}")

        if self.valid_number is not None:
            self.send_data(self.send_socket, (self.valid_number,))
            print(f"Sent valid number: {self.valid_number}")
            self.valid_number = None

        self.root.after(100, self.check_for_updates)

    def on_closing(self):
        self.context.term()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ZMQTkinterApp(root)
    root.mainloop()
