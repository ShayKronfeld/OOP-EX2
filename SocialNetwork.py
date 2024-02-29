from Users import Users

class SocialNetwork():
    _network = False

    def __init__(self, name):  # Singleton Design Pattern
        if SocialNetwork._network:
            raise RuntimeError("SocialNetwork is already opened")
        self.users = []
        self.posts = []
        self.name = name
        SocialNetwork._network = True
        print(f"The social network {self.name} was created!")

    def sign_up(self, username, password):
        if any(user.username == username for user in self.users):
            print(f"Username '{username}' is already taken. Please choose a different username.")
            return None

        new_user = Users(username, password)  # Create a new user
        if new_user.is_valid(new_user.password):  # check if the password is valid
            self.users.append(new_user)
            #print(f"User '{username}' has been successfully registered!")
            return new_user
        else:
            print(
                "The password must be at least 4 characters long and not more than 8 characters long. Please try again.")
            return None

    def log_in(self, username, password):
        user = None
        for u in self.users:
            if u.username == username and u.password == password:
                user = u
                break
        if user:
            user.connect()
            print(f"{username} connected")
        else:
            print(f"{username} not found in the social network.")

    def log_out(self, username):
        user = None
        for u in self.users:
            if u.username == username:
                user = u
                break
        if user:
            if user.connecting_status:
                user.disconnect()
                print(f"{username} disconnected")
            else:
                print(f"{username} is already logged out.")
        else:
            print(f"{username} not found in the social network.")

    def add_post(self, post):
        self.posts.append(post)

    def __str__(self):
        print(f"{self.name} social network:")
        return f"{self.display() or ''}"

    def display(self):
        for user in self.users:
            print(user)

    def print_values_users(self):
        for user in self.users:
            print(f"User name: {user.username}, Number of posts: {len(user.posts)}, Number of followers: {len(user.followers)}")
