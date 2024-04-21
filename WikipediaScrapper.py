#Libraries
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
import time
import threading
from queue import Queue
import multiprocessing
import csv
import os, os.path
import numpy as np



# "producer"- web scraping method

def Scraper(url,q):
    """
    Scrapes the given URL for links and puts them into the queue.

    Args:
        url (str): The URL to scrape.
        q (Queue): The queue to put the scraped links into.
    """
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    for link in soup.find_all('a'):
        q.put(link.get('href'))


def multiScraper(queue,filtered):
    """
    Multi-threaded version of the Scraper function.

    Args:
        queue (Queue): The queue of URLs to scrape.
        filtered (Queue): The queue of filtered URLs.
    """
    if __name__ == "__main__":

        for i in set(filtered.queue):
            url = str(i)

            scraping = threading.Thread(target=Scraper,args=(url,queue))
            scraping.start()

        scraping.join()


# "consumer" - checks if URL contain the word "malware"
def Filter(q,filtered):
    """
    Filters URLs based on the presence of the word "malware" in their content.

    Args:
        q (Queue): The queue of URLs to filter.
        filtered (Queue): The queue to put filtered URLs into.
    """
    mask = ["malware","Malware"]
    while(q.qsize() != 0):
        try:
            link = q.get()
            html = requests.get(link).text
            soup = BeautifulSoup(html)
            if len(list(set(mask) & set(soup.get_text().split()[0:100]))) > 0:
                filtered.put(link)
        except:
            pass



def multiFilter(queue,filtered):  
    """
    Multi-threaded version of the Filter function.

    Args:
        queue (Queue): The queue of URLs to filter.
        filtered (Queue): The queue to put filtered URLs into.
    """
    while(queue.qsize() != 0):
        filtering = threading.Thread(target=Filter,args=(queue,filtered))
        filtering.start()
    filtering.join()


def is_ascii(s):
    """
    Checks if a string contains only ASCII characters.

    Args:
        s (str): The string to check.

    Returns:
        bool: True if all characters are ASCII, False otherwise.
    """
    return all(ord(c) < 128 for c in s)


def mask(soup,link,title, visited):
    """
    Masks URLs based on certain criteria.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML.
        link (str): The URL of the page.
        title (str): The title of the page.
        visited (Queue): The queue of visited URLs.

    Returns:
        bool: True if the URL passes the masking criteria, False otherwise.
    """
    #list of key terms to filter
    keyWords = ["malware"]  #"flubot", "cabassous",
    badWords = ["Template"]
    
    linkCheck = link not in visited.queue
    if linkCheck == False:
        return False
    
    asciiCheck = is_ascii(title)
    if asciiCheck == False:
        return False
    
    text = soup.get_text().split()[0:200]
    text = (map(lambda x: x.lower(), text))
    
    wordCheck = len(list(set(keyWords) & set(text))) > 0
    badWordCheck = len(list(set(badWords) & set(title.replace(':',' ').split()))) <= 0
    
    return wordCheck & badWordCheck


#takes in current url and queue of urls visited before
def filterScrapeWrite(url, visited):
    """
    Filters, scrapes, and writes URLs to CSV and text files.

    Args:
        url (str): The URL to filter, scrape, and write.
        visited (Queue): The queue of visited URLs.
    """
    #get all urls from page
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    #iterate over all urls found
    
    for element in soup.find_all('a'):
        try:
            #get first 100 words from page
            link = element.get('href')
            base = "https://attack.mitre.org/"
            link = urljoin(base, link)
            reqs = requests.get(link)
            
            soup2 = BeautifulSoup(reqs.text, 'html.parser')
            #iterate over all urls found
            for title in soup2.find_all('title'):
                title = title.get_text()
            html = requests.get(link).text
            soup3 = BeautifulSoup(html, features="html.parser")
            #check to make sure the text contains key words and was not visited before
            
            if mask(soup3,link,title,visited):
                #add to visited queue and write to csv
                visited.put(link)
                
                f = open("text/" + str(title) + ".txt","w")
                f.write(soup3.get_text())
                
                with open('urls.csv', 'a') as f:
                    csv_writer_lock = threading.Lock()
                    writer = csv.writer(f)
                    with csv_writer_lock:
                        writer.writerow([str(title) + ":" + str(link)])
                    
        except:
            pass

# Function to remove a file if it exists
def remove_file(file_path):
    """
    Removes a file if it exists.

    Args:
        file_path (str): The path to the file to remove.
    """
    try:
        os.remove(file_path)
    except OSError:
        pass

# Function to remove a directory if it exists
def remove_directory(directory_path):
    """
    Removes a directory if it exists.

    Args:
        directory_path (str): The path to the directory to remove.
    """
    try:
        os.rmdir(directory_path)
    except OSError:
        pass

# Remove previous CSV file and create a directory for text files
remove_file('urls.csv')
remove_directory('text')
os.mkdir('text')

t1 = time.time()
visited = Queue()
done = Queue()
url = "https://attack.mitre.org/techniques/T1587/001/"
filterScrapeWrite(url, visited)
t2 = time.time()
print("Generation: 0")
print(t2-t1)
#print("# urls = " + str(visited.qsize()))
generations = 10

for i in range(0,generations):
    
    if __name__ == "__main__":
            t3 = time.time()
            for n in list(set(visited.queue) - set(done.queue)):
                done.put(n)
                url = str(n)

                scraping = threading.Thread(target=filterScrapeWrite,args=(url,visited))
                scraping.start()
             
            scraping.join()
            t4 = time.time()
            print("Generation: " + str(i+1))
            print(t4-t3)
            #print("# urls = " + str(visited.qsize()))