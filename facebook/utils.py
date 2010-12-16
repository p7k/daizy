import uuid
from time import mktime
from datetime import datetime
from socialregistration.forms import UserForm
from django.contrib.auth import login

def now_timestamp():
    return mktime(datetime.now().timetuple())

def fb_account_setup(request, user, facebook_profile):
    form = UserForm(user, facebook_profile)
    if form.is_valid():
        form.save(request=request)
        user = form.profile.authenticate()
        login(request, user)
    else:
        # Generate user and profile
        user.username = str(uuid.uuid4())[:30]
        user.save()

        facebook_profile.user = user
        facebook_profile.save()

        # Authenticate and login
        user = facebook_profile.authenticate()
        login(request, user)

def fql_query(timestamp, source_id='me()', limit=50):
    # TODO look into filtering (WHERE filter_key="nf")
    return 'SELECT %(stream_fields)s FROM stream WHERE source_id IN (SELECT target_id FROM connection WHERE source_id = %(source_id)s) AND is_hidden = 0 AND created_time < %(timestamp)s LIMIT %(limit)s' % {
        'stream_fields': 'post_id, actor_id, source_id, message, attachment.media, created_time, permalink, comments',
        'source_id': source_id,
        'timestamp': int(timestamp),
        'limit': int(limit)
    }

_accepted_sources = ('youtube.com', 'fbcdn.net')
def skinny_video_post(post):
    attachment = post['attachment']
    media_list = attachment.get('media')
    if media_list:
        for media in media_list:
            video = media.get('video')
            if video:
                source_url = video.get('source_url')
                if any((_ in source_url for _ in _accepted_sources)):
                    return {
                        'post_id': post.get('post_id', ''),
                        'message': post.get('message', ''),
                        'source_id': post.get('source_id', ''),
                        'actor_id': post.get('actor_id', ''),
                        'permalink': post.get('permalink', ''),
                        'comments': post.get('comments', ''),
                        'created_time': post.get('created_time', ''),
                        'img_src': media.get('src', ''),
                        'vid_src': source_url,
                    }
