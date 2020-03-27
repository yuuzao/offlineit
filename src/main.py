from src.blog import Blog
from src.cmd import cmd

if __name__ == "__main__":
    url = cmd()
    blog = Blog(url)

    print(blog.content())
