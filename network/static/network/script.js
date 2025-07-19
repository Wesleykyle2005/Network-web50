document.addEventListener('DOMContentLoaded', function() {
    // Función para obtener el CSRF token
    function getCSRFToken() {
        return window.csrfToken || '';
    }

    // Función para mostrar mensajes de error
    function showError(message) {
        console.error('Error:', message);
        alert('Error: ' + message);
    }

    const followBtn = document.getElementById('follow_btn');
    if (followBtn) {
        followBtn.addEventListener('click', function() {
            let userId = this.value;
            fetch(`/follow/${userId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ user_id: userId })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(result => {
                if (result.error) {
                    showError(result.error);
                    return;
                }
                followBtn.innerHTML = result.following ? 'Unfollow' : 'Follow';
                const followersCountElement = document.getElementById('followers_count');
                const followingCountElement = document.getElementById('following_count');
                if (followersCountElement) {
                    followersCountElement.innerHTML = result.followers_count;
                }
                if (followingCountElement) {
                    followingCountElement.innerHTML = result.following_count;
                }
                const followersModalBody = document.getElementById('FollowersModalBody');
                if (followersModalBody && result.followers_this) {
                    let followersHTML = '<ul>';
                    if (result.followers_this.length > 0) {
                        result.followers_this.forEach(function(follower) {
                            followersHTML += `<li><a href="/viewprofile/${follower.id}">${follower.username}</a></li>`;
                        });
                    } else {
                        followersHTML += '<li>No followers yet.</li>';
                    }
                    followersHTML += '</ul>';
                    followersModalBody.innerHTML = followersHTML;
                }
                const followingModalBody = document.getElementById('followingModalBody');
                if (followingModalBody && result.following_this) {
                    let followingHTML = '<ul>';
                    if (result.following_this.length > 0) {
                        result.following_this.forEach(function(followingUser) {
                            followingHTML += `<li><a href="/viewprofile/${followingUser.id}">${followingUser.username}</a></li>`;
                        });
                    } else {
                        followingHTML += '<li>Not following anyone.</li>';
                    }
                    followingHTML += '</ul>';
                    followingModalBody.innerHTML = followingHTML;
                }
            })
            .catch(error => {
                showError('Error al procesar la solicitud de follow');
            });
        });
    }
    
    document.querySelectorAll('.like_btn').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.value;
            fetch(`/like/${postId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ post_id: postId })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(result => {
                if (result.error) {
                    showError(result.error);
                    return;
                }
                const badge = this.querySelector('.badge');
                if (badge) {
                    badge.innerText = result.likes_count;
                }
                if (result.liked) {
                    this.classList.add('liked');
                } else {
                    this.classList.remove('liked');
                }
            })
            .catch(error => {
                showError('Error al procesar el like');
            });
        });
    });

    const editModalElement = document.getElementById('editPostModal');
    let editModal;
    if (editModalElement) {
        editModal = new bootstrap.Modal(editModalElement);
    }
    
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.dataset.postId;
            let postContent;
            try {
                postContent = JSON.parse('"' + this.dataset.postContent + '"');
            } catch(e) {
                postContent = this.dataset.postContent || "";
            }
            if (editModalElement) {
                const editPostIdInput = document.getElementById('edit-post-id');
                const editPostContentInput = document.getElementById('edit-post-content');
                if (editPostIdInput && editPostContentInput) {
                    editPostIdInput.value = postId;
                    editPostContentInput.value = postContent;
                }
                if (editModal) {
                    editModal.show();
                }
            }
        });
    });
    
    const editForm = document.querySelector('#editPostModal form');
    if (editForm) {
        editForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(editForm);
            fetch(editForm.action, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const contentElement = document.getElementById(`post-content-${data.post_id}`);
                    if (contentElement) {
                        contentElement.innerText = data.new_content;
                    }
                    if (editModal) {
                        editModal.hide();
                    }
                }
            })
            .catch(error => {});
        });
    }
});
