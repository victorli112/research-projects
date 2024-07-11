# import requests
from bs4 import BeautifulSoup

def get_names():
  # URL of the webpage containing the list of books
  # url = 'https://damore-mckim.northeastern.edu/group/marketing/members/?keyword=&view=all'

  # # Send a GET request to the webpage
  # response = requests.get(url)
  # print(response.text)
  html = open('marketing_prof_site.html', 'r')
  # Create a BeautifulSoup object to parse the HTML content
  soup = BeautifulSoup(html, 'html.parser')

  # Find all the book titles using the appropriate HTML tags and attributes
  all_names = soup.find_all('a', class_='person-line-name-link')
  names = []
  # Extract and print the titles
  for name in all_names:
      print(name.text.strip())
      names.append(name.text.strip())
  print(names)
  print(len(names))
      
get_names()