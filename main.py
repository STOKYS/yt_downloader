import os
from os.path import expanduser
import re
import subprocess
from pytube import YouTube
from pytube import Playlist
import tkinter as tk


def gui():
    # init tkinter
    root = tk.Tk()
    root.title("GUI")
    root.geometry("800x600")

    # init label
    label = tk.Label(root, text="Hello World!")
    label.grid()

    # init button
    button = tk.Button(root, text="Click Me!", command=lambda: download_pytube(str(entry.get())))
    button.grid(column=1, row=1)

    # init entry
    entry = tk.Entry(root, width=100)
    entry.grid(column=0, row=1)

    # init listbox
    listbox = tk.Listbox(root)
    listbox.grid()
    # listbox.insert(tk.END, "Hello")
    # listbox.insert(tk.END, "World")
    # listbox.insert(tk.END, "!")

    # init tkinter
    root.mainloop()


def download_pytube(url):
    home = expanduser("~/Music")
    # url = input("Paste URL of the audio you want to download: ")
    if url.find('list=') != -1:
        print("Downloading playlist...")
        download_playlist(url, home)
    else:
        print("Downloading audio...")
        download_audio(url, home)


def reformat_title(title):
    new_title = re.sub('[^a-zA-Z0-9-_()\\[\\] ]', '', title)
    print(f"{title} > {new_title}")
    return new_title


def download_audio(url, home):
    subprocess_run(home, url)


def download_playlist(url, home):
    yt = Playlist(url)
    home = f'{home}/{yt.title}'
    os.mkdir(home)
    for x in yt:
        subprocess_run(home, x)


def subprocess_run(home, x):
    x = YouTube(x)
    print(f"\nYou're about to download: \n"
          f"{x.title}\n"
          f"by: {x.author}\n")
    print(f"Downloading: {x.title}")
    x_streams = x.streams.get_audio_only()
    x.title = reformat_title(x.title)
    x_streams.download(home)
    subprocess.run([
        'ffmpeg',
        '-i', os.path.join(home, f"{x.title}.mp4"),
        os.path.join(home, f"{x.title}.mp3")
    ], stdout=subprocess.DEVNULL)
    subprocess.run(['rm', f'{home}/{x.title}.mp4'], stdout=subprocess.DEVNULL)


def main():
    gui()
    download_pytube()


if __name__ == '__main__':
    main()
