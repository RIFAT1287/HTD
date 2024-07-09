import os

print("Welcome to Hentais Tube Downloader")
print("\nThis script was created by e42b, visit the project repository at https://github.com/e43b/HentaisTube-Downloader")

print("\nTo download multiple episodes of a series, type 1")
print("To download a specific episode, type 2")

option = input("\nEnter your option: ")

if option == "1":
    # Execute script to download all episodes of a series
    os.system("python series.py")
elif option == "2":
    # Execute script to download a specific episode
    os.system("python episode.py")
else:
    print("Invalid option. Please choose 1 or 2.")
