import time


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
    extracting_data = []

    for comments_data in comment_elements:
        user_info = comments_data.find('ytd-comment-renderer').find('a', {'id': 'author-text'})
        name_commenter = user_info.text.strip()
        comment_period = comments_data.find('a', {'class': 'yt-simple-endpoint style-scope yt-formatted-string'}).text
        comment_contents = comments_data.find('yt-formatted-string', {'class': 'style-scope ytd-comment-renderer'}).text
        thumbnail_link = comments_data.find('img', {'class': 'style-scope yt-img-shadow'}).get('src')
        total_likes = comments_data.find(
                    'span', {'class': 'style-scope ytd-comment-action-buttons-renderer'}
                ).text.strip()
        comments_data = {
            "username": name_commenter,
            "user's_thumbnail_URL": thumbnail_link,
            "comment_period": comment_period,
            "total_likes": total_likes,
            "comment_contents": comment_contents,

        }
        extracting_data.append(comments_data)
    return extracting_data
