import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

def find_broken_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)  # Find all <a> tags with an href attribute
    broken_links = []

    for link in links:
        link_url = urljoin(url, link['href'])  # Resolve relative URLs
        print(f"Checking link: {link_url} on page: {url}\n")  # Print the link URL and page

        try:
            link_response = requests.get(link_url)
            if link_response.status_code == 404:  # If the link leads to a 404 (Not Found)
                broken_links.append((link_url, url))
                print(f"Broken link: {link_url} found on page: {url}")
        except requests.exceptions.RequestException as e:
            print(f"Error accessing {link_url}: {e}")
            broken_links.append((link_url, url))

    return broken_links

def save_broken_links_to_csv(broken_links, file_name="broken_links.csv"):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Broken Link", "Found On Page"])  # Two columns: broken link, and the page it was found on
        for link, page in broken_links:
            writer.writerow([link, page])

def main(url):
    broken_links = find_broken_links(url)
    if broken_links:
        print(f"Found {len(broken_links)} broken links.")
        save_broken_links_to_csv(broken_links)
        print(f"Broken links saved to 'broken_links.csv'.")
    else:
        print("No broken links found.")

if __name__ == "__main__":
    # Example usage: Pass the website URL as a parameter
    website_url = input("Enter the website URL to check for broken links: ")
    main(website_url)
