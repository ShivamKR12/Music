# Import necessary modules
import requests
from tkinter import filedialog, Tk, Menu, Listbox, Button, Frame, PhotoImage, END, BOTH, BOTTOM, TOP, X, Label, Scale, HORIZONTAL
import pygame
import os
import sys

# Download the image from the web
def download_image(image_url,file_name):
    response = requests.get(image_url)
    with open(file_name, 'wb') as file:
        file.write(response.content)

# download_image('https://media.geeksforgeeks.org/wp-content/uploads/20240610151925/background.png','background.png')
# download_image('https://media.geeksforgeeks.org/wp-content/uploads/20240610151926/next.png','next.png')
# download_image('https://media.geeksforgeeks.org/wp-content/uploads/20240610151926/pause.png','pause.png')
# download_image('https://media.geeksforgeeks.org/wp-content/uploads/20240610151926/play.png','play.png')
# download_image('https://media.geeksforgeeks.org/wp-content/uploads/20240610151926/previous.png','previous.png')

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class EnhancedMusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title('Music Player with Tkinter and Pygame in Python')
        self.root.geometry("600x400")
        self.root.minsize(500, 300)
        
        pygame.mixer.init()
        
        self.playlist = []
        self.current_song = ""
        self.is_paused = False
        self.directory = ""
        self.is_fullscreen = False
        
        try:
            self.app_icon = PhotoImage(file=get_resource_path('background.png')) 
            self.root.iconphoto(False, self.app_icon)
            
            self.play_img = PhotoImage(file=get_resource_path('play.png'))
            self.pause_img = PhotoImage(file=get_resource_path('pause.png'))
            self.next_img = PhotoImage(file=get_resource_path('next.png'))
            self.prev_img = PhotoImage(file=get_resource_path('previous.png'))
        except Exception as e:
            print("Make sure png files are in the directory.")
            
        self.setup_ui()
        self.check_music_end()

    def setup_ui(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)
        
        add_songs_menu = Menu(menu_bar, tearoff=False)
        add_songs_menu.add_command(label='Select Folder', command=self.load_music)
        menu_bar.add_cascade(label='File', menu=add_songs_menu)
        
        self.status_label = Label(self.root, text="No song playing", font=("Helvetica", 12, "bold"), bg="#1c1c1c", fg="white", pady=10)
        self.status_label.pack(side=TOP, fill=X)

        self.song_listbox = Listbox(self.root, bg="#2c3e50", fg="white", font=("Helvetica", 11), selectbackground="#34495e")
        self.song_listbox.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)
        self.song_listbox.bind("<<ListboxSelect>>", self.play_selected_music)
        
        self.control_frame = Frame(self.root)
        self.control_frame.pack(side=BOTTOM, pady=15)
        
        self.prev_btn = Button(self.control_frame, image=self.prev_img, borderwidth=0, command=self.previous_song)
        self.prev_btn.grid(row=0, column=0, padx=10)
        
        self.play_pause_btn = Button(self.control_frame, image=self.play_img, borderwidth=0, command=self.toggle_play_pause)
        self.play_pause_btn.grid(row=0, column=1, padx=10)
        
        self.next_btn = Button(self.control_frame, image=self.next_img, borderwidth=0, command=self.next_song)
        self.next_btn.grid(row=0, column=2, padx=10)
        
        self.volume_scale = Scale(self.control_frame, from_=0, to=100, orient=HORIZONTAL, command=self.set_volume, length=120, showvalue=0)
        self.volume_scale.set(50)
        self.volume_scale.grid(row=0, column=3, padx=20)
        
        self.fullscreen_btn = Button(self.control_frame, text="Fullscreen", command=self.toggle_fullscreen)
        self.fullscreen_btn.grid(row=0, column=4, padx=10)

    def load_music(self):
        self.directory = filedialog.askdirectory()
        if not self.directory:
            return
            
        self.playlist.clear()
        self.song_listbox.delete(0, END)
        
        for file in os.listdir(self.directory):
            name, ext = os.path.splitext(file)
            if ext.lower() == '.mp3':
                self.playlist.append(file)
                
        for song in self.playlist:
            self.song_listbox.insert(END, song)

    def play_selected_music(self, event=None):
        if not self.playlist:
            return
            
        current_selection = self.song_listbox.curselection()
        if current_selection:
            self.current_song = self.playlist[current_selection[0]]
            self.play_current_song()

    def play_current_song(self):
        if not self.current_song:
            return
            
        pygame.mixer.music.load(os.path.join(self.directory, self.current_song))
        pygame.mixer.music.play()
        self.is_paused = False
        self.play_pause_btn.config(image=self.pause_img)
        self.status_label.config(text=f"Playing: {self.current_song}")

    def toggle_play_pause(self):
        if not self.playlist:
            return
            
        if not pygame.mixer.music.get_busy() and not self.is_paused:
            current_selection = self.song_listbox.curselection()
            if not current_selection:
                self.song_listbox.selection_set(0)
                self.current_song = self.playlist[0]
            else:
                self.current_song = self.playlist[current_selection[0]]
            self.play_current_song()
            return

        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.play_pause_btn.config(image=self.pause_img)
            self.status_label.config(text=f"Playing: {self.current_song}")
        else:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.play_pause_btn.config(image=self.play_img)
            self.status_label.config(text=f"Paused: {self.current_song}")

    def next_song(self):
        if not self.playlist or not self.current_song:
            return
            
        try:
            current_idx = self.playlist.index(self.current_song)
            next_idx = (current_idx + 1) % len(self.playlist)
            
            self.song_listbox.selection_clear(0, END)
            self.song_listbox.selection_set(next_idx)
            self.song_listbox.activate(next_idx)
            
            self.current_song = self.playlist[next_idx]
            self.play_current_song()
        except ValueError:
            pass

    def previous_song(self):
        if not self.playlist or not self.current_song:
            return
            
        try:
            current_idx = self.playlist.index(self.current_song)
            prev_idx = (current_idx - 1) % len(self.playlist)
            
            self.song_listbox.selection_clear(0, END)
            self.song_listbox.selection_set(prev_idx)
            self.song_listbox.activate(prev_idx)
            
            self.current_song = self.playlist[prev_idx]
            self.play_current_song()
        except ValueError:
            pass

    def set_volume(self, val):
        volume = float(val) / 100
        pygame.mixer.music.set_volume(volume)

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
        if self.is_fullscreen:
            self.root.bind("<Escape>", lambda e: self.toggle_fullscreen())
        else:
            self.root.unbind("<Escape>")

    def check_music_end(self):
        if not pygame.mixer.music.get_busy() and not self.is_paused and self.current_song:
            self.next_song()
        self.root.after(100, self.check_music_end)

if __name__ == "__main__":
    app = Tk()
    player = EnhancedMusicPlayer(app)
    app.mainloop()
