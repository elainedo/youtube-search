import os
import re
import sys
import csv

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = ""
YOUTUBE_API_VERSION = ""


def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
  infoList = []
  next_page_token = ''
  pageCount = 4 #Limit the page count
  while next_page_token is not None and pageCount != 0:
      #search on Youtube
      search_response = youtube.search().list(
        q=options.q,
        part="id,snippet",
        maxResults=options.max_results,
        pageToken=next_page_token
      ).execute()

      #save results to infoList
      for search_result in search_response.get("items", []):
        info = [search_result["snippet"]["title"], search_result["id"]["kind"]]
        infoList.append(info)

      #reset pageToken and reduce pageCount
      next_page_token = search_response.get('nextPageToken', None)
      pageCount = pageCount - 1
  return infoList

def savefile(infoList):
    #save to a file that is in the same location of this file
    location = os.path.realpath(
      os.path.join(os.getcwd(), os.path.dirname(__file__)))
    file = os.path.join(location, 'youtubedocument.csv');
    writer = csv.writer(open(file, 'w'), delimiter =',')
    writer.writerow(["Title", "Kind"])
    for info in infoList:
        writer.writerow(info)

if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="AA speaker")
  argparser.add_argument("--max-results", help="Max results", default=25)
  args = argparser.parse_args()

  try:
    youtubeInfoList = youtube_search(args)
    savefile(youtubeInfoList)
  except (HttpError, e):
    print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
