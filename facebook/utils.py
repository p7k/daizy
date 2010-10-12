import re

id_re = re.compile(r'^[^v]+v.(.{11}).*')
def parse_youtube_id(link): 
    return id_re.sub(r'\1', link)

def iterytlinks(results):
    for r in results:
        attachment = r['attachment']
        media_list = attachment.get('media')
        if media_list:
            for media in media_list:
                href = media.get('href')
                if href and 'youtube' in href:
                    yield parse_youtube_id(href)

