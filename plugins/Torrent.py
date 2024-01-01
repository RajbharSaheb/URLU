import os
import aiohttp
import json
from pyrogram import Client, filters, emoji
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import bs4

@Client.on_message(filters.command(["torrent", "tor"]))
def torrent_search(query):
  """
  Searches for torrents using the 1337x website.

  Args:
    query: The search query.

  Returns:
    A list of dictionaries containing the following information about each torrent:
      - name: The name of the torrent.
      - size: The size of the torrent in gigabytes.
      - seeds: The number of seeds for the torrent.
      - leeches: The number of leeches for the torrent.
      - magnet_link: The magnet link for the torrent.
  """

  # Build the search URL.
  search_url = "https://1337x.to/search/" + query + "/1/"

  # Send a GET request to the search URL.
  response = requests.get(search_url)

  # Parse the HTML response.
  soup = bs4.BeautifulSoup(response.text, "html.parser")

  # Find all of the torrent results.
  results = soup.find_all("tr", class_="torrent")

  # Extract the information about each torrent.
  torrents = []
  for result in results:
    name = result.find("td", class_="name").text
    size = result.find("td", class_="size").text
    seeds = result.find("td", class_="seeds").text
    leeches = result.find("td", class_="leeches").text
    magnet_link = result.find("a", class_="magnet")["href"]

    # Convert the size from megabytes to gigabytes.
    size = float(size[:-1]) / 1024

    # Create a dictionary containing the information about the torrent.
    torrent = {
      "name": name,
      "size": size,
      "seeds": seeds,
      "leeches": leeches,
      "magnet_link": magnet_link,
    }

    # Add the torrent to the list of torrents.
    torrents.append(torrent)

  # Return the list of torrents.
  return torrents


if __name__ == "__main__":
  # Get the search query from the user.
  query = input("Enter a search query: ")

  # Search for torrents using the search query.
  torrents = torrent_search(query)

  # Print the information about each torrent.
  for torrent in torrents:
    print("Name:", torrent["name"])
    print("Size:", torrent["size"], "GB")
    print("Seeds:", torrent["seeds"])
    print("Leeches:", torrent["leeches"])
    print("Magnet link:", torrent["magnet_link"])
    print()
