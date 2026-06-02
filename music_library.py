# music_library.py

class Song:
    def __init__(self, title, artist, duration):
        self.title = title
        self.artist = artist
        self.duration = duration  # in seconds

    def __str__(self):
        mins = self.duration // 60
        secs = self.duration % 60
        return f"{self.title} by {self.artist} ({mins}:{secs:02d})"

    def is_long(self):
        return self.duration > 300  # longer than 5 mins


class Album:
    def __init__(self, title, artist, year):
        self.title = title
        self.artist = artist
        self.year = year
        self.songs = []

    def __str__(self):
        return f"{self.title} by {self.artist} ({self.year})"

    def add_song(self, song):
        self.songs.append(song)

    def total_duration(self):
        total = 0
        for song in self.songs:
            total += song.duration
        mins = total // 60
        secs = total % 60
        return f"{mins}:{secs:02d}"

    def longest_song(self):
        return max(self.songs, key=lambda s: s.duration)


class Library:
    def __init__(self, name):
        self.name = name
        self.albums = []

    def add_album(self, album):
        self.albums.append(album)

    def all_songs(self):
        songs = []
        for album in self.albums:
            for song in album.songs:
                songs.append(song)
        return songs

    def search(self, query):
        results = []
        for song in self.all_songs():
            if query.lower() in song.title.lower():
                results.append(song)
        return results

    def report(self):
        print(f"=== {self.name} ===")
        print(f"Albums: {len(self.albums)}")
        print(f"Total songs: {len(self.all_songs())}")
        print()
        for album in self.albums:
            print(f"  {album}")
            for song in album.songs:
                print(f"    - {song}")
            print(f"    Total duration: {album.total_duration()}")
            print(f"    Longest: {album.longest_song().title}")
            print()


# --- build the library ---

album1 = Album("Dark Side of the Moon", "Pink Floyd", 1973)
album1.add_song(Song("Speak to Me", "Pink Floyd", 68))
album1.add_song(Song("Breathe", "Pink Floyd", 163))
album1.add_song(Song("Time", "Pink Floyd", 413))
album1.add_song(Song("Money", "Pink Floyd", 382))

album2 = Album("Thriller", "Michael Jackson", 1982)
album2.add_song(Song("Thriller", "Michael Jackson", 358))
album2.add_song(Song("Billie Jean", "Michael Jackson", 294))
album2.add_song(Song("Beat It", "Michael Jackson", 258))

lib = Library("Viyan's Music Library")
lib.add_album(album1)
lib.add_album(album2)

lib.report()

print("=== Search: 'time' ===")
results = lib.search("time")
for r in results:
    print(f"  {r}")

print()
print("=== Long songs (5+ mins) ===")
for song in lib.all_songs():
    if song.is_long():
        print(f"  {song}")