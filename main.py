import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_links_from_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            # Check if href is not None and it starts with http or https (to skip internal links)
            if href and (href.startswith('http://') or href.startswith('https://')):
                links.append(href)
            # If it's a relative link, convert it to absolute link
            elif href and not href.startswith('#'):
                absolute_link = urljoin(url, href)
                links.append(absolute_link)
        return links
    except Exception as e:
        print("Error:", e)
        return []

def scrape_single_title(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            titles = soup.find_all('title')
            title_texts = [title.get_text() for title in titles]
            return title_texts[0]
        else:
            return None
    except Exception as e:
        print("An error occurred while scraping", url, ":", str(e))
        return None



def scrape_recursive(url, depth=1):
    if depth == 0:
        return
    links = get_links_from_page(url)
    print("Links found on", url)
    for link in links:
        text=scrape_single_title(link)

        if text:
            

            trimmed_link=link.replace("https://", "")

            file=open("output.txt","a")
            
            try:
                file.write(f"link:  {trimmed_link}   title: {text} \n")
            except UnicodeEncodeError as error:
                print("couldnt encode emojis"+str(error))
            
            file.close()
        else:
            print("none found")
        
        scrape_recursive(link, depth - 1)

def main():
    url = input("Enter the URL to scrape: ")
    scrape_recursive(url)

if __name__ == "__main__":
    main()
