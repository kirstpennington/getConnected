# these objects only store info that the user updates manually-info that is not constantly being updates
# class with user profile info

# class with user privacy info
class Privacy:
    def __init__(self, bio, connections, country, name, pic, c, f):
        self.bio = bio
        self.connections = connections
        self.country = country
        self.name = name
        self.pic = pic
        self.courses = c
        self.forums = f
