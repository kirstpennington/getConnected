# these objects only store info that the user updates manually-info that is not constantly being updates
# class with user profile info


class User:
    def __init__(self, name, bio, numConn, numForum, numCourse, em, pa, country, profPic, bPic, id, courseList, forumList, topics):
        self.username = name
        self.bio = bio
        self.numConnections = numConn
        self.numForums = numForum
        self.numCourses = numCourse
        self.email = em
        self.password = pa
        self.country = country
        self.profilePic = profPic
        self.backgroundPic = bPic
        self.uid = id
        self.coursesInfoList = courseList
        self.forumsInfoList = forumList
        self.topicsList = topics
