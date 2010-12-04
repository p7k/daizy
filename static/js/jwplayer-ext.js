function PlaylistHelper(player, fetch_url) {
    this.new_items = [];
    this.addPlaylistItem = function (new_item) {
        return this.new_items.push(new_item);
    };
    this.addPlaylistItemFromPost = function (post) {
        return this.addPlaylistItem({
            file: post.vid_src,
            image: post.img_src,
            fb_post: post,              // monkey patch?!
        });
    };
    this.reloadPlaylist = function () {
        if (this.new_items.length > 0) {
            var newPlaylist = player.getPlaylist().concat(this.new_items);
            player.load(newPlaylist);
            this.new_items = [];
        }
    };
    this.itemsAwaiting = function () {
        return this.new_items.length > 0;
    };
    this.fetchVideoPosts = function (do_reload) {
        var _this = this;
        $.getJSON(fetch_url, function (posts) {
            $.each(posts, function (i, post) {
                _this.addPlaylistItemFromPost(post);
            });
            if (do_reload) _this.reloadPlaylist();
        });
    };
}

function wirePlayer(player, fetch_url, update_func) {
    var playlist_helper = new PlaylistHelper(player, fetch_url);

    var next_index = 0;
    var playlist_reloading = false;
    var last_item = false;

    player.onReady(function () {
        playlist_helper.fetchVideoPosts(true);
    }).onComplete(function () {
        if (!playlist_reloading) this.playlistNext();
    }).onPlaylistItem(function (data) {
        var pl_length = this.getPlaylist().length;
        last_item = data.index == (pl_length - 1);
        if (playlist_reloading) {
            this.stop();
        } else {
            update_func(this.getPlaylist()[data.index].fb_post);
            if (data.index > (pl_length - 3)) playlist_helper.fetchVideoPosts();
        }
    }).onPlaylist(function (data) {
        playlist_reloading = false;
        this.playlistItem(next_index);
    }).onIdle(function (data) {
        var in_middle = (this.getPosition() > 0) && ((this.getDuration() - this.getPosition()) > 1);
        if (last_item && !playlist_reloading && playlist_helper.itemsAwaiting() && !in_middle) {
            playlist_reloading = true;
            next_index = this.getPlaylist().length;
            playlist_helper.reloadPlaylist();
        }
    });
}