from vidstream import *
import tkinter as tk
import  socket
import threading

local_ip = socket.gethostbyname(socket.gethostname())

server = StreamingServer(local_ip, 7777)
receiver = AudioReceiver(local_ip, 6666)
camera_client = 0
screen_client = 0
audio_sender = 0

def start_listening():
    t1 = threading.Thread(target=server.start_server)
    t2 = threading.Thread(target=receiver.start_server)

    t1.start()
    t2.start()

def start_camera_stream():
    camera_client = CameraClient(text_target_ip.get(1.0, 'end-1c'), 9999)
    t3 = threading.Thread(target=camera_client.start_stream)
    t3.start()


def start_screen_sharing():
    screen_client = ScreenShareClient(text_target_ip.get(1.0, 'end-1c'), 9999)
    t4 = threading.Thread(target=screen_client.start_stream)
    t4.start()

def start_audio_stream():
    audio_sender = AudioSender(text_target_ip.get(1.0, 'end-1c'), 8888)
    t5 = threading.Thread(target=audio_sender.start_stream)
    t5.start()

def stop_connection():
    server.stop_server()
    receiver.stop_server()

    if camera_client != 0 :
        camera_client.storm_stream()

    if screen_client != 0:
        screen_client.storm_stream()

    if audio_sender != 0:
        audio_sender.storm_stream()

    window.destroy()

#GUI

window = tk.Tk()
window.title("Hayks zoom 0.1")
window.geometry('300x300')

label_target_ip = tk.Label(window, text="Target IP:")
label_target_ip.pack()

text_target_ip = tk.Text(window, height=1)
text_target_ip.pack()

btn_listen = tk.Button(window, text="Start listening", width=50, command=start_listening)
btn_listen.pack(anchor=tk.CENTER, expand=True)

btn_camera = tk.Button(window, text="Start camera stream", width=50, command=start_camera_stream)
btn_camera.pack(anchor=tk.CENTER, expand=True)

btn_screen = tk.Button(window, text="Start screen sharing", width=50, command=start_screen_sharing)
btn_screen.pack(anchor=tk.CENTER, expand=True)

btn_audio = tk.Button(window, text="Start audio stream", width=50, command=start_audio_stream)
btn_audio.pack(anchor=tk.CENTER, expand=True)


btn_stop = tk.Button(window, text="Stop connection", width=50, command=stop_connection)
btn_stop.pack(anchor=tk.CENTER, expand=True)

window.protocol("WM_DELETE_WINDOW", stop_connection)
window.mainloop()