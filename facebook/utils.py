import re

id_re = re.compile(r'^[^v]+v.(.{11}).*')
def parse_youtube_id(link): 
    return id_re.sub(r'\1', link)

# deprecated
def iterytlinks(results):
    for r in results:
        attachment = r['attachment']
        media_list = attachment.get('media')
        if media_list:
            for media in media_list:
                href = media.get('href')
                if href and 'youtube' in href:
                    yield parse_youtube_id(href)

def get_youtube_id(post):
    attachment = post['attachment']
    media_list = attachment.get('media')
    if media_list:
        for media in media_list:
            href = media.get('href')
            if href and 'youtube' in href:
                return parse_youtube_id(href)
    return None

def iter_prep_posts(posts):
    for post in posts:
        youtube_id = get_youtube_id(post)
        if youtube_id:
            yield dict(
                youtube_id=youtube_id,
                post_id=post['post_id'],
                permalink=post['permalink']
            )

# def iter_video_posts(posts):
#     for post in posts:
        
