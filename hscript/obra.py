from bs4 import BeautifulSoup
import requests
import os

# Function to find MediaFire and Google Drive links on an episode page
def find_links(episode_url):
    response = requests.get(episode_url)
    soup = BeautifulSoup(response.content, "html.parser")
    mediafire_links = soup.find_all("a", href=lambda href: href and "mediafire.com" in href)
    drive_links = soup.find_all("a", href=lambda href: href and "drive.google.com" in href)
    return mediafire_links, drive_links

# Function to download the video file from the link
def download_video(link, episode_title, directory):
    if "mediafire.com" in link:
        # Make an HTTP request to the provided URL
        response = requests.get(link)

        # Check if the request was successful
        if response.status_code == 200:
            # Extract the HTML content from the response
            html = response.text

            # Use BeautifulSoup to parse the HTML
            soup = BeautifulSoup(html, 'html.parser')

            # Find the direct download link
            download_link = soup.find('a', class_='input popsok')['href']

            # Define the file name from the episode title
            file_name = f"{episode_title}.mp4"

            # Define the full path to save the file
            file_path = os.path.join(directory, file_name)

            # Create the destination directory if it does not exist
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Download the file
            with open(file_path, 'wb') as file:
                response = requests.get(download_link)
                file.write(response.content)

            print('File successfully downloaded:', file_path)
        else:
            print("Failed to get the page content. Status code:", response.status_code)
    elif "drive.google.com" in link:
        # If it's a Google Drive link, just print the link and notify in the console
        print("Google Drive link found:", link)
        print("Please download the file manually.")
    else:
        print("Unsupported link:", link)

# Main page link with the list of episodes
main_url = input("Enter the series link: ")

# Extract relevant part of the main URL for the folder name
folder_name = main_url.split("/")[-2][:45]

response_main = requests.get(main_url)
soup_main = BeautifulSoup(response_main.content, "html.parser")
episodes_section = soup_main.find("div", class_="pagAniListaContainer")
episodes_links = episodes_section.find_all("a")

# Destination directory to save the files
directory = folder_name

# Iterate over episode links
for episode_link in episodes_links:
    episode_title = episode_link.get_text()
    episode_url = episode_link["href"]

    # Find MediaFire and Google Drive links for the current episode
    mediafire_links, drive_links = find_links(episode_url)

    print("Episode:", episode_title)
    print("Link:", episode_url)

    # Download files from MediaFire
    for mediafire_link in mediafire_links:
        download_video(mediafire_link['href'], episode_title, directory)

    # Save Google Drive links in a txt file
    if drive_links:
        # Create the destination directory if it does not exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Define the full path to save the txt file
        txt_file_path = os.path.join(directory, f"{episode_title}_google_drive_links.txt")

        # Write the links to the txt file
        with open(txt_file_path, 'w') as txt_file:
            for link in drive_links:
                txt_file.write(link['href'] + '\n')

        print(f"The Google Drive links for episode {episode_title} have been saved in: {txt_file_path}\n")
    else:
        print("No Google Drive links found.\n")
