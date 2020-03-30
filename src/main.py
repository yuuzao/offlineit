from pathlib import Path
from src.blog import Blog
from src.cmd import cmd

if __name__ == "__main__":
    cmd = cmd()
    if cmd['config'] is None:
        config = Path.home().joinpath('.config/offlineit.toml')
    else:
        config = cmd['config']
    url = cmd['url']
    blog = Blog(url, config)

    print(blog.content())
