import git

repo = git.Repo()
repo.remotes.origin.pull()