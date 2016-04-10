import subprocess


def sync_with_github():
	subprocess.call(["git", "add", "."])
	subprocess.call(["git", "commit", "-m", "Adding new mp3"])
	subprocess.call(["git", "pull", "origin", "master"])
	subprocess.call(["git", "push", "origin", "master"])


if __name__ == "__main__":
	sync_with_github()