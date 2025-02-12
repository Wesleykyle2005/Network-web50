document.addEventListener('DOMContentLoaded', function() {
    const followBtn = document.getElementById('follow_btn');
    if (followBtn) {
        followBtn.addEventListener('click', function() {
            let userId = this.value;
            
            fetch(`/follow/${userId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_id: userId })
            })
            .then(response => response.json())
            .then(result => {
                followBtn.innerHTML = result.following ? 'Unfollow' : 'Follow';
                document.getElementById('followers_count').innerHTML = result.followers_count;
                document.getElementById('following_count').innerHTML = result.following_count;
                
                let followersHTML = '<ul>';
                if (result.followers_this && result.followers_this.length > 0) {
                    result.followers_this.forEach(function(follower) {
                        followersHTML += `<li><a href="/viewprofile/${follower.id}">${follower.username}</a></li>`;
                    });
                } else {
                    followersHTML += '<li>No followers yet.</li>';
                }
                followersHTML += '</ul>';
                document.getElementById('FollowersModalBody').innerHTML = followersHTML;
                
                let followingHTML = '<ul>';
                if (result.following_this && result.following_this.length > 0) {
                    result.following_this.forEach(function(followingUser) {
                        followingHTML += `<li><a href="/viewprofile/${followingUser.id}">${followingUser.username}</a></li>`;
                    });
                } else {
                    followingHTML += '<li>Not following anyone.</li>';
                }
                followingHTML += '</ul>';
                document.getElementById('followingModalBody').innerHTML = followingHTML;
            })
            .catch(error => console.log(error));
        });
    }
    
    document.querySelectorAll('.like_btn').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.value;
            fetch(`/like/${postId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ post_id: postId })
            })
            .then(response => response.json())
            .then(result => {
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
            .catch(error => console.log(error));
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
                console.log("Error al parsear el contenido del post:", e);
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
            } else {
                console.log("El elemento del modal de edición no existe.");
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
                    console.log(contentElement);
                    if (contentElement) {
                        contentElement.innerText = data.new_content;
                    }
                    if (editModal) {
                        editModal.hide();
                    }
                } else {
                    console.error("Error al editar el post:", data.error);
                }
            })
            .catch(error => console.error("Error en la petición:", error));
        });
    }
});
