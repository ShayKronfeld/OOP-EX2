from abc import ABC, abstractmethod
from PIL import Image
import matplotlib.pyplot as plt

# here we use in factory design
class Posts(ABC):
    def __init__(self, name, post_type):
        self._name = name  # the name of the owner
        self.type_post = post_type
        self.likes = []
        self.comments = []

    @abstractmethod
    def display(self):
        pass

    def like(self, user):
        try:
            self.likes.append(user)
            if user.username != self._name.username:
                print(f"Notification to {self._name.username}: {user.username} liked your post")
                self._name.add_notify(f"{user.username} liked your post")
        except Exception:
            pass

    def comment(self, user, text):
        try:
            self.comments.append('username:' + user.username + 'text:' + text)
            if user.username != self._name.username:
                print(f"Notification to {self._name.username}: {user.username} commented on your post: {text}")
                self._name.add_notify(f"{user.username} commented on your post")
        except Exception:
            pass

    def __str__(self):
        if self.type_post == "Image":
            return f"{self._name.username} posted a picture\n"
        else:
            return f"{self.display() or ''}"

# this is the post with only text
class TextPost(Posts):
    def __init__(self, name, text):
        super().__init__(name, "Text")
        self.text = text

    def display(self):
        print(f"{self._name.username} published a post:\n\"{self.text}\"\n")


# this is the post of sale products
class SalePost(Posts):
    def __init__(self, name, object, cost, location):
        super().__init__(name, "Sale")
        self.object = object
        self.cost = cost
        self.location = location
        self.someone_buy = False

    def sold(self, password):
        if self._name.password == password:  # if the password it's of the owner
            self.someone_buy = True
            print(f"{self._name.username}'s product is sold")

    def discount(self, precent, password):
        if self._name.password == password and not self.someone_buy:
            update = self.cost * (precent / 100)
            self.cost = self.cost - update
            print(f"Discount on {self._name.username} product! the new price is: {self.cost}")

    def display(self):
        if not self.someone_buy:
            print(f"{self._name.username} posted a product for sale:\nFor sale! {self.object}, price: {self.cost}, pickup from: {self.location}")
            print()
        else:
            print(f"{self._name.username} posted a product for sale:")
            print(f"Sold! {self.object}, price: {self.cost}, pickup from: {self.location}")


# this is the post with images
class ImagePost(Posts):
    def __init__(self, name, image_location):
        super().__init__(name, "Image")
        self.location_image = image_location

    def display(self):
        print("Shows picture")
        try:
            img_matplotlib = plt.imread(self.location_image)
            plt.imshow(img_matplotlib)
            plt.axis('off')  # Turn off axis labels
            plt.show()

            # Using Pillow to display the image
            img_pillow = Image.open(self.location_image)
            img_pillow.show()

            return "Displayed an image."
        except FileNotFoundError:
            return "Failed to display image."

# Define the post factory
class PostFactory:
    @staticmethod
    def create_post(post_type, name, **kwargs):
        if post_type == "Text":
            return TextPost(name, **kwargs)
        elif post_type == "Sale":
            return SalePost(name, **kwargs)
        elif post_type == "Image":
            return ImagePost(name, **kwargs)
        else:
            raise ValueError(f"Invalid post type: {post_type}")