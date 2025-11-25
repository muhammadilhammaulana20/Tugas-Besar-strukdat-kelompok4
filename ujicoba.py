import customtkinter as ctk
from tkinter import messagebox
import random

# ============================================
# BACKEND - DATA STRUCTURES
# ============================================

class Song:
    def __init__(self, id, title, artist, genre, album, year, duration):
        self.id = id
        self.title = title
        self.artist = artist
        self.genre = genre
        self.album = album
        self.year = year
        self.duration = duration
    
    def __str__(self):
        return f"{self.title} - {self.artist}"


class Node:
    def __init__(self, song):
        self.song = song
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def add(self, song):
        new_node = Node(song)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1
        return True
    
    def delete(self, song_id):
        current = self.head
        while current:
            if current.song.id == song_id:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                self.size -= 1
                return True
            current = current.next
        return False
    
    def search(self, keyword):
        results = []
        current = self.head
        keyword = keyword.lower()
        while current:
            if (keyword in current.song.title.lower() or 
                keyword in current.song.artist.lower() or
                keyword in current.song.genre.lower()):
                results.append(current.song)
            current = current.next
        return results
    
    def get_all(self):
        songs = []
        current = self.head
        while current:
            songs.append(current.song)
            current = current.next
        return songs
    
    def find_by_id(self, song_id):
        current = self.head
        while current:
            if current.song.id == song_id:
                return current.song
            current = current.next
        return None


class Queue:
    def __init__(self):
        self.items = []
    
    def enqueue(self, song):
        self.items.append(song)
    
    def dequeue(self):
        return self.items.pop(0) if self.items else None
    
    def get_all(self):
        return self.items.copy()


class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, song):
        if len(self.items) >= 20:
            self.items.pop(0)
        self.items.append(song)
    
    def get_all(self):
        return self.items.copy()


class MusicPlayer:
    def __init__(self):
        self.library = DoublyLinkedList()
        self.playlist = DoublyLinkedList()
        self.queue = Queue()
        self.history = Stack()
        self.favorites = set()
        self.current_song = None
        self.is_playing = False
        self.current_mode = "library"
        self._load_sample_data()
    
    def _load_sample_data(self):
        samples = [
            Song(1, "Bohemian Rhapsody", "Queen", "Rock", "A Night at the Opera", 1975, "5:55"),
            Song(2, "Imagine", "John Lennon", "Pop", "Imagine", 1971, "3:03"),
            Song(3, "Hotel California", "Eagles", "Rock", "Hotel California", 1977, "6:30"),
            Song(4, "Billie Jean", "Michael Jackson", "Pop", "Thriller", 1983, "4:54"),
            Song(5, "Sweet Child O' Mine", "Guns N' Roses", "Rock", "Appetite", 1987, "5:56"),
            Song(6, "Stairway to Heaven", "Led Zeppelin", "Rock", "Led Zeppelin IV", 1971, "8:02"),
        ]
        for song in samples:
            self.library.add(song)
    
    def get_next_id(self):
        songs = self.library.get_all()
        return max([s.id for s in songs], default=0) + 1
    
    def find_similar_song(self, current_song):
        songs = self.library.get_all()
        candidates = [s for s in songs if s.id != current_song.id]
        if not candidates:
            return None
        same_artist = [s for s in candidates if s.artist == current_song.artist]
        if same_artist:
            return same_artist[0]
        same_genre = [s for s in candidates if s.genre == current_song.genre]
        if same_genre:
            return same_genre[0]
        return random.choice(candidates)
    
    def next_song(self):
        if self.current_mode == "playlist":
            songs = self.playlist.get_all()
        else:
            if not self.current_song:
                return None
            return self.find_similar_song(self.current_song)
        
        if not songs or not self.current_song:
            return None
        try:
            idx = next(i for i, s in enumerate(songs) if s.id == self.current_song.id)
            if idx < len(songs) - 1:
                return songs[idx + 1]
        except:
            pass
        return None
    
    def prev_song(self):
        if self.current_mode == "playlist":
            songs = self.playlist.get_all()
        else:
            if not self.current_song:
                return None
            return self.find_similar_song(self.current_song)
        
        if not songs or not self.current_song:
            return None
        try:
            idx = next(i for i, s in enumerate(songs) if s.id == self.current_song.id)
            if idx > 0:
                return songs[idx - 1]
        except:
            pass
        return None
    
# ============================================
# FRONTEND - MODERN UI
# ============================================

class MusicPlayerGUI:
    def __init__(self):
        self.player = MusicPlayer()
        self.current_user = None
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.window = ctk.CTk()
        self.window.title("Groovy Music Player")
        self.window.geometry("1200x700")
        self.window.configure(fg_color="#0a0a0a")
        
        self.show_login()
        
    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()
    
    def show_login(self):
        self.clear_window()
        
        bg = ctk.CTkFrame(self.window, fg_color="#0a0a0a")
        bg.pack(fill="both", expand=True)
        
        frame = ctk.CTkFrame(bg, width=350, height=250, corner_radius=20, fg_color="#1a1a1a")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(frame, text="🎵 Groovy", font=("Arial", 36, "bold"),
                    text_color="#6366f1").pack(pady=(30, 5))
        ctk.CTkLabel(frame, text="Music Player", font=("Arial", 14),
                    text_color="#94a3b8").pack(pady=(0, 30))
        
        ctk.CTkButton(frame, text="Admin", width=220, height=42, font=("Arial", 15),
                     corner_radius=8, fg_color="#6366f1", hover_color="#4f46e5",
                     command=lambda: self.login("admin")).pack(pady=8)
        
        ctk.CTkButton(frame, text="User", width=220, height=42, font=("Arial", 15),
                     corner_radius=8, fg_color="#1e293b", hover_color="#334155",
                     command=lambda: self.login("user")).pack(pady=8)
    
    def login(self, role):
        self.current_user = role
        if role == "admin":
            self.show_admin_page()
        else:
            self.show_user_page()
    
    def show_admin_page(self):
        self.clear_window()
        
        # Sidebar
        sidebar = ctk.CTkFrame(self.window, width=200, corner_radius=0, fg_color="#0f0f0f")
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        ctk.CTkLabel(sidebar, text="⚡ Groovy", font=("Arial", 20, "bold"),
                    text_color="#6366f1").pack(pady=(30, 50))
        
        menus = [("📚 Library", self.admin_view_songs), ("➕ Add Song", self.admin_add_song),
                 ("🚪 Logout", self.show_login)]
        
        for text, cmd in menus:
            ctk.CTkButton(sidebar, text=text, width=170, height=38, font=("Arial", 13),
                         corner_radius=8, fg_color="transparent", hover_color="#1e293b",
                         anchor="w", command=cmd).pack(pady=4, padx=15)
        
        # Content
        self.content = ctk.CTkFrame(self.window, fg_color="#0a0a0a")
        self.content.pack(side="right", fill="both", expand=True, padx=25, pady=25)
        
        self.admin_view_songs()
    
    def admin_view_songs(self):
        for w in self.content.winfo_children():
            w.destroy()
        
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(header, text="Library", font=("Arial", 32, "bold"),
                    text_color="#ffffff").pack(side="left")
        
        # Table
        table = ctk.CTkFrame(self.content, fg_color="#0f0f0f", corner_radius=12)
        table.pack(fill="both", expand=True)
        
        # Header
        thead = ctk.CTkFrame(table, fg_color="transparent", height=45)
        thead.pack(fill="x", padx=15, pady=(15, 5))
        
        cols = [("#", 0.06), ("Title", 0.25), ("Artist", 0.22), ("Genre", 0.15), ("Album", 0.22)]
        x = 0
        for text, w in cols:
            ctk.CTkLabel(thead, text=text, font=("Arial", 11, "bold"), text_color="#64748b",
                        anchor="w").place(relx=x, rely=0.5, anchor="w")
            x += w
        
        # Body
        scroll = ctk.CTkScrollableFrame(table, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        for song in self.player.library.get_all():
            row = ctk.CTkFrame(scroll, fg_color="#1a1a1a", height=50, corner_radius=8)
            row.pack(fill="x", pady=2)
            
            data = [(str(song.id), 0.06), (song.title[:22], 0.25), (song.artist[:18], 0.22),
                    (song.genre, 0.15), (song.album[:18], 0.22)]
            x = 0.02
            for val, w in data:
                ctk.CTkLabel(row, text=val, font=("Arial", 11), text_color="#e2e8f0",
                            anchor="w").place(relx=x, rely=0.5, anchor="w")
                x += w
            
            ctk.CTkButton(row, text="Delete", width=70, height=32, font=("Arial", 10),
                         fg_color="#ef4444", hover_color="#dc2626",
                         command=lambda s=song: self.admin_delete(s.id)).place(relx=0.94, rely=0.5, anchor="center")
    
    def admin_add_song(self):
        for w in self.content.winfo_children():
            w.destroy()
        
        ctk.CTkLabel(self.content, text="Add New Song", font=("Arial", 32, "bold"),
                    text_color="#ffffff").pack(pady=(0, 25))
        
        form = ctk.CTkFrame(self.content, fg_color="#0f0f0f", corner_radius=12)
        form.pack(fill="both", expand=True, padx=50)
        
        entries = {}
        fields = [("Title", "Song title"), ("Artist", "Artist name"), ("Genre", "Genre"),
                  ("Album", "Album name"), ("Year", "2020"), ("Duration", "3:30")]
        
        for lbl, ph in fields:
            ctk.CTkLabel(form, text=lbl, font=("Arial", 13), text_color="#94a3b8",
                        anchor="w").pack(anchor="w", padx=30, pady=(15, 3))
            e = ctk.CTkEntry(form, width=400, height=40, placeholder_text=ph, font=("Arial", 12),
                            corner_radius=8, fg_color="#1a1a1a", border_color="#334155")
            e.pack(padx=30, pady=(0, 5))
            entries[lbl.lower()] = e
        
        def save():
            try:
                song = Song(self.player.get_next_id(), entries['title'].get(), entries['artist'].get(),
                           entries['genre'].get(), entries['album'].get(), int(entries['year'].get()),
                           entries['duration'].get())
                self.player.library.add(song)
                messagebox.showinfo("Success", "Song added!")
                self.admin_view_songs()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ctk.CTkButton(form, text="Save Song", width=180, height=42, font=("Arial", 14),
                     fg_color="#6366f1", hover_color="#4f46e5", command=save).pack(pady=25)
    
    def admin_delete(self, song_id):
        if messagebox.askyesno("Confirm", "Delete this song?"):
            self.player.library.delete(song_id)
            self.player.playlist.delete(song_id)
            self.admin_view_songs()
    
    def show_user_page(self):
        self.clear_window()
        
        # Sidebar
        sidebar = ctk.CTkFrame(self.window, width=200, corner_radius=0, fg_color="#0f0f0f")
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        ctk.CTkLabel(sidebar, text="⚡ Groovy", font=("Arial", 20, "bold"),
                    text_color="#6366f1").pack(pady=(30, 10))
        
        ctk.CTkLabel(sidebar, text="MENU", font=("Arial", 10, "bold"),
                    text_color="#64748b").pack(pady=(20, 10), padx=20, anchor="w")
        
        menus = [("🏠 Home", self.user_home), ("🔍 Search", self.user_search),
                 ("📝 Playlist", self.user_playlist), ("⭐ Favorites", self.user_favorites),
                 ("📜 History", self.user_history)]
        
        for text, cmd in menus:
            ctk.CTkButton(sidebar, text=text, width=170, height=38, font=("Arial", 13),
                         corner_radius=8, fg_color="transparent", hover_color="#1e293b",
                         anchor="w", command=cmd).pack(pady=3, padx=15)
        
        ctk.CTkLabel(sidebar, text="PLAYLIST", font=("Arial", 10, "bold"),
                    text_color="#64748b").pack(pady=(30, 10), padx=20, anchor="w")
        
        ctk.CTkButton(sidebar, text="🚪 Logout", width=170, height=38, font=("Arial", 13),
                     corner_radius=8, fg_color="transparent", hover_color="#1e293b",
                     anchor="w", command=self.show_login).pack(side="bottom", pady=20, padx=15)
        
        # Main content
        self.main_content = ctk.CTkFrame(self.window, fg_color="#0a0a0a")
        self.main_content.pack(side="top", fill="both", expand=True)
        
        # Top bar
        topbar = ctk.CTkFrame(self.main_content, height=60, fg_color="transparent")
        topbar.pack(fill="x", padx=25, pady=(15, 0))
        
        search = ctk.CTkEntry(topbar, width=350, height=38, placeholder_text="🔍 Search songs...",
                             font=("Arial", 12), corner_radius=20, fg_color="#1a1a1a", border_width=0)
        search.pack(side="left")
        
        user_btn = ctk.CTkButton(topbar, text="👤 User", width=100, height=38,
                                font=("Arial", 12), corner_radius=20, fg_color="#1a1a1a")
        user_btn.pack(side="right")
        
        # Content area
        self.content = ctk.CTkScrollableFrame(self.main_content, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=25, pady=(10, 90))
        
        # Bottom player
        self.create_player_bottom()
        
        self.user_home()
    
    def create_player_bottom(self):
        player = ctk.CTkFrame(self.window, height=90, fg_color="#0f0f0f")
        player.place(relx=0, rely=1, anchor="sw", relwidth=1)
        
        # Song info
        info = ctk.CTkFrame(player, fg_color="transparent")
        info.place(relx=0.22, rely=0.5, anchor="w")
        
        self.now_playing = ctk.CTkLabel(info, text="No song playing", font=("Arial", 13, "bold"),
                                       text_color="#ffffff")
        self.now_playing.pack(anchor="w")
        
        self.now_artist = ctk.CTkLabel(info, text="", font=("Arial", 11), text_color="#94a3b8")
        self.now_artist.pack(anchor="w")
        
        # Controls
        controls = ctk.CTkFrame(player, fg_color="transparent")
        controls.place(relx=0.5, rely=0.5, anchor="center")
        
        btns = [("⏮", self.play_prev), ("▶", self.play_current),
                ("⏸", self.stop_current), ("⏭", self.play_next)]
        
        for icon, cmd in btns:
            ctk.CTkButton(controls, text=icon, width=45, height=45, font=("Arial", 16),
                         corner_radius=25, fg_color="#6366f1" if icon == "▶" else "#1e293b",
                         hover_color="#4f46e5", command=cmd).pack(side="left", padx=4)
    
    def create_song_card(self, parent, song):
        card = ctk.CTkFrame(parent, fg_color="#1a1a1a", corner_radius=8, height=70)
        card.pack(fill="x", pady=3)
        
        # Info
        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        
        ctk.CTkLabel(info, text=song.title, font=("Arial", 13, "bold"),
                    text_color="#ffffff", anchor="w").pack(anchor="w")
        ctk.CTkLabel(info, text=f"{song.artist} • {song.genre}", font=("Arial", 10),
                    text_color="#94a3b8", anchor="w").pack(anchor="w")
        
        # Buttons
        btns = ctk.CTkFrame(card, fg_color="transparent")
        btns.pack(side="right", padx=10)
        
        fav_text = "⭐" if song.id in self.player.favorites else "☆"
        ctk.CTkButton(btns, text=fav_text, width=35, height=35, font=("Arial", 14),
                     fg_color="transparent", hover_color="#6366f1",
                     command=lambda: self.toggle_fav(song)).pack(side="left", padx=2)
        
        ctk.CTkButton(btns, text="▶", width=35, height=35, font=("Arial", 12),
                     fg_color="#6366f1", hover_color="#4f46e5",
                     command=lambda: self.play_song(song, "library")).pack(side="left", padx=2)
        
        ctk.CTkButton(btns, text="+", width=35, height=35, font=("Arial", 14),
                     fg_color="#1e293b", hover_color="#334155",
                     command=lambda: self.add_playlist(song)).pack(side="left", padx=2)
    
    def user_home(self):
        for w in self.content.winfo_children():
            w.destroy()
        
        ctk.CTkLabel(self.content, text="Trending Now", font=("Arial", 28, "bold"),
                    text_color="#ffffff").pack(anchor="w", pady=(10, 20))
        
        for song in self.player.library.get_all()[:6]:
            self.create_song_card(self.content, song)
    
    def user_search(self):
        for w in self.content.winfo_children():
            w.destroy()
        
        ctk.CTkLabel(self.content, text="Search", font=("Arial", 28, "bold"),
                    text_color="#ffffff").pack(anchor="w", pady=(10, 15))
        
        search_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        search_frame.pack(fill="x", pady=10)
        
        entry = ctk.CTkEntry(search_frame, width=400, height=40, placeholder_text="Search...",
                            font=("Arial", 12), corner_radius=8, fg_color="#1a1a1a")
        entry.pack(side="left", padx=(0, 10))
        
        result = ctk.CTkFrame(self.content, fg_color="transparent")
        result.pack(fill="both", expand=True, pady=10)
        
        def search():
            for w in result.winfo_children():
                w.destroy()
            keyword = entry.get()
            if keyword:
                songs = self.player.library.search(keyword)
                for song in songs:
                    self.create_song_card(result, song)
        
        ctk.CTkButton(search_frame, text="Search", width=100, height=40, fg_color="#6366f1",
                     hover_color="#4f46e5", command=search).pack(side="left")
    
    def user_playlist(self):
        for w in self.content.winfo_children():
            w.destroy()
        
        ctk.CTkLabel(self.content, text="My Playlist", font=("Arial", 28, "bold"),
                    text_color="#ffffff").pack(anchor="w", pady=(10, 20))
        
        songs = self.player.playlist.get_all()
        if not songs:
            ctk.CTkLabel(self.content, text="Playlist is empty", font=("Arial", 13),
                        text_color="#64748b").pack(pady=30)
        else:
            for song in songs:
                self.create_song_card(self.content, song)
    
    def user_favorites(self):
        for w in self.content.winfo_children():
            w.destroy()
        
        ctk.CTkLabel(self.content, text="Favorites", font=("Arial", 28, "bold"),
                    text_color="#ffffff").pack(anchor="w", pady=(10, 20))
        
        favs = [s for s in self.player.library.get_all() if s.id in self.player.favorites]
        if not favs:
            ctk.CTkLabel(self.content, text="No favorites yet", font=("Arial", 13),
                        text_color="#64748b").pack(pady=30)
        else:
            for song in favs:
                self.create_song_card(self.content, song)
    
    def user_history(self):
        for w in self.content.winfo_children():
            w.destroy()
        
        ctk.CTkLabel(self.content, text="Recently Played", font=("Arial", 28, "bold"),
                    text_color="#ffffff").pack(anchor="w", pady=(10, 20))
        
        history = self.player.history.get_all()
        if not history:
            ctk.CTkLabel(self.content, text="No history yet", font=("Arial", 13),
                        text_color="#64748b").pack(pady=30)
        else:
            for song in reversed(history):
                self.create_song_card(self.content, song)
    
    def toggle_fav(self, song):
        if song.id in self.player.favorites:
            self.player.favorites.remove(song.id)
        else:
            self.player.favorites.add(song.id)
        self.user_home()
    
    def play_song(self, song, mode):
        self.player.current_song = song
        self.player.is_playing = True
        self.player.current_mode = mode
        self.player.history.push(song)
        self.now_playing.configure(text=song.title)
        self.now_artist.configure(text=song.artist)
    
    def play_prev(self):
        prev = self.player.prev_song()
        if prev:
            self.play_song(prev, self.player.current_mode)
    
    def play_next(self):
        next_s = self.player.next_song()
        if next_s:
            self.play_song(next_s, self.player.current_mode)
    
    def play_current(self):
        if self.player.current_song:
            self.player.is_playing = True
            self.now_playing.configure(text=self.player.current_song.title)
    
    def stop_current(self):
        self.player.is_playing = False
    
    def add_playlist(self, song):
        self.player.playlist.add(song)
        messagebox.showinfo("Success", f"'{song.title}' added to playlist!")
    
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = MusicPlayerGUI()
    app.run()