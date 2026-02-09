#!/usr/bin/env python3
"""
Generate an Atom feed from GitHub releases.
"""

import os
import requests
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Configuration
FEED_TITLE = "Cormac Auty"
FEED_DESCRIPTION = "new posts from Cormac's blog"
FEED_AUTHOR = "Cormac Auty"
FEED_ICON = "https://cormacauty.com/assets/a49c92ef-5e94-4c17-a4a5-2a949fe2b38f.jpeg"
BLOG_URL = "https://cormacauty.com"

def fetch_releases(repo):
    """Fetch releases from GitHub API."""
    token = os.environ.get('GITHUB_TOKEN')
    headers = {'Authorization': f'token {token}'} if token else {}
    
    url = f'https://api.github.com/repos/{repo}/releases'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json()

def create_atom_feed(releases):
    """Create Atom feed XML from releases."""
    # Create root feed element
    feed = Element('feed', xmlns='http://www.w3.org/2005/Atom')
    
    # Feed metadata
    title = SubElement(feed, 'title')
    title.text = FEED_TITLE
    
    subtitle = SubElement(feed, 'subtitle')
    subtitle.text = FEED_DESCRIPTION
    
    link_self = SubElement(feed, 'link', href=f'{BLOG_URL}/feed.xml', rel='self')
    link_alt = SubElement(feed, 'link', href=BLOG_URL, rel='alternate')
    
    icon = SubElement(feed, 'icon')
    icon.text = FEED_ICON
    
    feed_id = SubElement(feed, 'id')
    feed_id.text = BLOG_URL
    
    # Use the most recent release date as updated time, or now if no releases
    if releases:
        most_recent = max(releases, key=lambda r: r['published_at'])
        updated = SubElement(feed, 'updated')
        updated.text = most_recent['published_at']
    else:
        updated = SubElement(feed, 'updated')
        updated.text = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    author = SubElement(feed, 'author')
    author_name = SubElement(author, 'name')
    author_name.text = FEED_AUTHOR
    
    # Add entries for each release
    for release in releases:
        entry = SubElement(feed, 'entry')
        
        entry_title = SubElement(entry, 'title')
        entry_title.text = release['name'] or release['tag_name']
        
        entry_link = SubElement(entry, 'link', href=release['html_url'])
        
        entry_id = SubElement(entry, 'id')
        entry_id.text = release['html_url']
        
        entry_updated = SubElement(entry, 'updated')
        entry_updated.text = release['published_at']
        
        entry_published = SubElement(entry, 'published')
        entry_published.text = release['published_at']
        
        if release['body']:
            content = SubElement(entry, 'content', type='html')
            content.text = release['body']
        
        entry_author = SubElement(entry, 'author')
        entry_author_name = SubElement(entry_author, 'name')
        entry_author_name.text = FEED_AUTHOR
    
    return feed

def prettify_xml(elem):
    """Return a pretty-printed XML string."""
    rough_string = tostring(elem, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')

def main():
    repo = os.environ.get('REPO')
    if not repo:
        raise ValueError("REPO environment variable not set")
    
    print(f"Fetching releases from {repo}...")
    releases = fetch_releases(repo)
    print(f"Found {len(releases)} releases")
    
    print("Generating Atom feed...")
    feed = create_atom_feed(releases)
    
    xml_string = prettify_xml(feed)
    
    with open('feed.xml', 'w', encoding='utf-8') as f:
        f.write(xml_string)
    
    print("Feed generated successfully: feed.xml")

if __name__ == '__main__':
    main()
