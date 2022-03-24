function like(postId) {
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);

    fetch(`/like-post/${postId}/`, {method: 'POST'})
    .then((res) => res.json())
    .then((data) => {
        likeCount.innerHTML = data['likes'];
        if (data['liked'] === true) {
          likeButton.src = "/static/images/icons/heart_b.png";
        } else {
          likeButton.src = "/static/images/icons/heart.png";
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
          saveButton.src = "/static/images/icons/bookmark_b.png";
        } else {
          saveButton.src = "/static/images/icons/bookmark.png";
        }
    })
    .catch((e) => alert('Could not like post.'));

}

function showPassword(number) {
  if (number === 0) {
    var input = document.getElementById(`password`);
    var img = document.getElementById(`icon-eye`)
  } else {
    var input = document.getElementById(`password${number}`);
    var img = document.getElementById(`icon-eye${number}`)
  }
  if (input.type === "password") {
    input.type = "text";
    img.src = "/static/images/icons/eye.png";
  } else {
    input.type = "password";
    img.src = "/static/images/icons/eye-crossed.png";
  }
}

function copyPostLink(url, author) {
  link = location.protocol + '//' + location.host + '/post/'+ author +'/'+ url;
  navigator.clipboard.writeText(link);
}