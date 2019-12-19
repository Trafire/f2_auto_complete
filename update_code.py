import git
import os

repo = git.Repo(os.path.dirname(os.path.realpath(__file__)))
repo.remotes.origin.pull()
print()