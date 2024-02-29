from Posts import TextPost, ImagePost, SalePost

class Notification:
    def __init__(self, message, type):
        self.message = message
        self.type = type

class Users:
    def __init__(self, username, password):
        if not self.is_valid(password):
            raise ValueError("Password must be between 4 and 8 characters long. Please choose valid password.")
        self.username = username
        self.password = password
        self.connecting_status = True
        self.followers = []
        self.following = []
        self.posts = []
        self.notifications = []

    def is_valid(self, password):         # Check if the username and password is good
        if len(password) > 8 or len(password) < 4:
            return False
        return True


    def follow(self, user):             # add new follower to the list
        if user not in self.following:
            self.following.append(user)
            user.followers.append(self)
            print(f"{self.username} started following {user.username}")

    def unfollow(self, user):    # remove follower to the list
        if user in self.following:
            self.following.remove(user)
            user.followers.remove(self)
            print(f"{self.username} unfollowed {user.username}")


    def disconnect(self):       # change to disconnect
        self.connecting_status = False

    def connect(self):          # change to connect
        self.connecting_status = True


    def add_notify(self, notification):
        self.notifications.append(notification)

    def publish_post(self, post_type, *args):
        if not self.connecting_status:
            print("User is not connected. Cannot publish post.")
            return None
        if post_type == "Text":
            post = TextPost(self, *args)
        elif post_type == "Image":
            post = ImagePost(self, *args)
            print(f"{self.username} posted a picture\n")
            print()
        elif post_type == "Sale":
            post = SalePost(self, *args)
        else:
            print(f"Invalid post type: {post_type}")
            return None

        post._author = self
        self.posts.append(post)
        for follower in self.followers:
            follower.add_notify(f"{self.username} has a new post")  # Fixed typo here
        if post_type != "Image":
            post.display()
        return post

    def __str__(self):
        names = self.username
        num_posts = len(self.posts)
        num_followers = len(self.followers)
        return f"User name: {names}, Number of posts: {num_posts}, Number of followers: {num_followers}"

    def print_notifications(self):
        if self.connecting_status:
            print(f"{self.username}'s notifications:")
            for notification in self.notifications:
                if notification is not None:
                    print(f"{notification}")
