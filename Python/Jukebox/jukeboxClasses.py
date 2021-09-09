class Database:

    def __init__(self, csv):
        self.csv = csv
        self.data = []
        for index, row in self.csv.iterrows():
            self.data.append(Song(row['Title'], row['Artist']))
    def getData(self):
        return self.data
class Song:
    def __init__(self, title='Title',artist='Artist' ):
        self._title = title
        self._artist = artist

    def getTitle(self):
        return self._title
    def getArtist(self):
        return self._artist
    def play(self):
        print('Playing "',self._title,'" from', self._artist)

class Album:
    def __init__(self,albumTitle='AlbumName',songs=[], titles=[]):
        self._songs = songs
        self._songTitles = titles
        self.albumTitle = albumTitle
        if self._songTitles == []:
            for song in songs:
                self._songTitles.append(song.getTitle())


    def getAlbumTitle(self):
        return self.albumTitle
    def addSong2Album(self, song):
        self._songs.append(song)
        self._songTitles.append(song.getTitle())

    def getTitles(self):
        return self._songTitles
    def getSong(self, song):
        if self._songTitles.count(song) != 0:
            return self._songs[self._songTitles.index(song)]
        else:
            print('There is no song with this name')
            return None


class Library:
    def __init__(self, libraryName='LibraryName', albums=[], albumTitles=[]):
        self.librayName = libraryName
        self._albums = albums
        self._albumTitles = albumTitles

        if self._albumTitles == []:
            for album in albums:
                self._albumTitles.append(album.getAlbumTitle())

    def getAlbum(self, album):
        if self._albumTitles.count(album) != 0:
            return self._albums[self._albumTitles.index(album)]
        else:
            print('There is no album with this name')
            return None

    def getTitles(self):
        return self._albumTitles

    def createLib(self, csv):
        self._csv = csv
        self._data = []
        self._artists = set(csv['Artist'])
        

        for index, row in self.csv.iterrows():
            for x in self._artists:
                if row['Artist'] == x:
                    self.data.append(Song(row['Title'], row['Artist']))


    #colocar para pegar de datbase valores unicos da lista e montar os albuns

class Queue:
    def __init__(self, playlist=[]):
        self._playlist = playlist



    def addSong(self, song, id):
        self._playlist.append([song, id])
        self.showPlaylist()
    def getNextSong(self):
        return self._playlist.pop()
    def showPlaylist(self):
        print("==== PlayList ====")
        for row in self._playlist:
            print('Song:    ',row[0].getTitle(),'      User ID    ',row[1])

        print("++++++++++++++++++")
    def removeSong(self, song):
        for row in self._playlist:
            if row[0].getTitle() == song:
                self._playlist.remove(row)
                self.showPlaylist()
                break

class User:
    def __init__(self, name, id):
        self._name = name
        self._id = id
    def getID(self):
        return self._id

class Admin:
    def __init__(self, id):
        self._id = id
    def gettID(self):
        return self._id
    def createUser(self, name, id):
        return User(name,id)
    def manageQueue(self):
        pass

class Menu():
    def __init__(self):
        self.header()
        option = input('Select a option ')





    def header(self):
        print('~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~')
        print('============JUKEBOX==============')
        print('~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~')
        print('1 - Add a song')
        print('2 - Hear the playlist')

    def selectSongMenu(self):
        option = input('Select a option:')
        print('1 - Search for an Album')
        print('2 - See all songs')



