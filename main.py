import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite_operations as sql

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
        print("Try checking your internet connection")
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



def scrape_recursive(url:str,save_option:int, depth=1):
    save_option
    if depth == 0:
        return
    links = get_links_from_page(url)
    for link in links:
        text=scrape_single_title(link)
        if text:
            trimmed_link=link.replace("https://", "")
            
            if save_option==1:
                file=open("output.txt","a")
                try:
                    file.write(f"link:  {trimmed_link}   title: {text} \n")
                except UnicodeEncodeError as error:
                    print("couldnt encode emojis"+str(error))
            
                file.close()
            elif save_option==2:
                sql.add_entry(conn,trimmed_link,text)


        else:
            print("none found")
        
        scrape_recursive(link,save_option, depth - 1)

def main():
    url = input("Enter the URL to scrape: ")

    save_option=input("1- to file \n 2- to local db")
    i_save_option=int(save_option)

    if i_save_option==1:
        file=open("output.txt","a")
        file.write(f"scraping for: {url}\n")
        file.close()
    
    if i_save_option==2:
        sql.init_database()
        global conn
        conn=sql.create_conn()
        
    scrape_recursive(url,i_save_option)


    if i_save_option==2:
        conn.close()

if __name__ == "__main__":
    main()
