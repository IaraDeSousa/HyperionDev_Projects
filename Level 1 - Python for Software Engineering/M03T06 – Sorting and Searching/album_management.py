class Album:
    def __init__(self, album_name, number_of_songs, album_artist):
        self.album_name = album_name
        self.number_of_songs = number_of_songs
        self.album_artist = album_artist

    def __str__(self):
        album_summary = f"({self.album_name}, {self.album_artist}, {self.number_of_songs})"
        print(album_summary)


# Populating the album class with 5 albums.
def populate_albums1():
    album1 = Album("Lahai", 10, "Sampha")
    album2 = Album("Currents", 15, "Tame Impala")
    album3 = Album("Magdalene", 8, "FKA Twigs")
    album4 = Album("Empathogen", 12, "Willow")
    album5 = Album("Bird's Eye", 20, "Ravyn Lanae")
    albums1.append(album1)
    albums1.append(album2)
    albums1.append(album3)
    albums1.append(album4)
    albums1.append(album5)


# Initialise an empty list outside the class to store the album objects.
albums1: list[Album] = []


# Call the populate_albums function
populate_albums1()

# Function to view album list


def view_albums(albums):
    for album in albums:
        album.__str__()


# Call function to view unsorted albums
view_albums(albums1)

# Sort albums
albums1 = sorted(albums1, key=lambda album: album.number_of_songs)

# Call function to view sorted albums
view_albums(albums1)

# Assign temporary variables to index 0 and 1 to swap album indexes.
x = albums1[0]
y = albums1[1]

# Swapping and printing these albums
albums1[0] = y
albums1[0].__str__()
albums1[1] = x
albums1[1].__str__()

# Populating the album class with 5 albums.


def populate_albums2():
    album1 = Album("The Art of Loving", 5, "Olivia Dean")
    album2 = Album("Man's Best Friend", 18, "Sabrina Carpenter")
    album3 = Album("Time Flies", 7, "OASIS")
    album4 = Album("Brat", 14, "Charli XCX")
    album5 = Album("Hit Me Hard and Soft", 19, "Billie Eilish")
    albums2.append(album1)
    albums2.append(album2)
    albums2.append(album3)
    albums2.append(album4)
    albums2.append(album5)


# Initialise an empty list outside the class to store the album objects.
albums2: list[Album] = []


# Call the populate_albums function
populate_albums2()


# Call function to view unsorted albums in albums2
view_albums(albums2)


# Function to copy albums from albums1 to album2
def copy_albums():
    for album in albums1:
        albums2.append(album)


# Call function to view new albums2 list
copy_albums()
view_albums(albums2)


# Add two new albums to albums2
albums2.append(Album("Dark Side of the Moon", "Pink Floyd", 9))
albums2.append(Album("Oops!... I Did It Again", "Britney Spears", 16))


# Sort albums2 aphabetically
albums2 = sorted(albums2, key=lambda album: album.album_name)
view_albums(albums2)


# Search for a specific album and print the index of this album (using Linear Search)
def find_title(albums: list[Album], album_title):
    for i in range(0, len(albums)):
        if (albums[i].album_name == album_title):
            return i


print(find_title(albums2, "Dark Side of the Moon"))
