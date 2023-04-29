import time
import os
import pandas as pd
from bs4 import BeautifulSoup


def scroll_to_page_end(driver):
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, arguments[0]);", last_height)
        time.sleep(1.5)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height


def extract_comments_data(soup):
    comment_elements = soup.find_all('ytd-comment-thread-renderer')
    comments_data = []

    for comment_data in comment_elements:
        user_info = comment_data.find('ytd-comment-renderer').find('a', {'id': 'author-text'})
        name_commenter = user_info.text.strip()
        thumbnail_link = comment_data.find('img', {'class': 'style-scope yt-img-shadow'}).get('src')
        comment_period = comment_data.find('a', {'class': 'yt-simple-endpoint style-scope yt-formatted-string'}).text
        total_likes = comment_data.find(
            'span', {'class': 'style-scope ytd-comment-action-buttons-renderer'}
        ).text.strip()
        comment_contents = comment_data.find('yt-formatted-string', {'class': 'style-scope ytd-comment-renderer'}).text

        comments_data.append([name_commenter, thumbnail_link, comment_period, total_likes, comment_contents])

    return comments_data


def page_directory(page_url):
    channel_name = page_url.split("/")[-2].replace('@', '')
    channel_dir = os.path.join(os.getcwd(), channel_name)
    if not os.path.exists(channel_dir):
        os.mkdir(channel_dir)

    return channel_dir


def extract_all_video_links(soup):
    video_links = []
    for video in soup.find_all('ytd-rich-grid-media'):
        video_url = 'https://www.youtube.com' + video.find('a', {'id': 'video-title-link'}).get('href')
        video_links.append(video_url)

    return video_links


def extract_video_comments_info(video_link, channel_dir, driver):
    driver.get(video_link)

    time.sleep(5)

    scroll_to_page_end(driver)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    comments_data = extract_comments_data(soup)

    video_name = soup.title.string.split(" - YouTube")[0]
    video_title = video_name.replace('/', '-')

    file_name = video_title + '.csv'
    file_path = os.path.join(channel_dir, file_name)
    data_frame = pd.DataFrame(comments_data, columns=[
        "username", "user's_thumbnail_URL", "comment_period", "total_likes", "comment_contents"
    ])
    data_frame.to_csv(file_path, index=False)
    print(f"Extract Comments of video {video_title} |saved to CSV file| {file_name}")


def extracting_channel_videos(page_url, driver):
    page_url += "/videos"
    driver.get(page_url)

    time.sleep(5)

    scroll_to_page_end(driver)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    channel_dir = page_directory(page_url)
    video_links = extract_all_video_links(soup)

    for video_link in video_links:
        extract_video_comments_info(video_link, channel_dir, driver)

    print("Extracted data save to CSV file")
