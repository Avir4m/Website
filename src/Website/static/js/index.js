function like(postId) {
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);

    fetch(`/like-post/${postId}/`, {method: 'POST'})
    .then((res) => res.json())
    .then((data) => {
        likeCount.innerHTML = data['likes'];
        if (data['liked'] === true) {
          likeButton.src = "static/images/icons/heart_b.png";
        } else {
          likeButton.src = "static/images/icons/heart.png";
        }
    })
    .catch((e) => alert('Could not like post.'));

}

function save(postId) {
    const saveButton = document.getElementById(`save-button-${postId}`);

    fetch(`/save-post/${postId}/`, {method: 'POST'})
    .then((res) => res.json())
    .then((data) => {
        if (data['saved'] === true) {
          saveButton.src = "static/images/icons/bookmark_b.png";
        } else {
          saveButton.src = "static/images/icons/bookmark.png";
        }
    })
    .catch((e) => alert('Could not like post.'));

}