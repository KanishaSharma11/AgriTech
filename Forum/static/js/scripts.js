document.addEventListener('DOMContentLoaded', () => {
  const nameInput = document.getElementById('nameInput');
  const messageInput = document.getElementById('messageInput');
  const postButton = document.getElementById('postButton');
  const inputs = [nameInput, messageInput];

  const toggleButton = () => {
    postButton.disabled = inputs.some(input => !input.value.trim());
  };

  inputs.forEach(input => input.addEventListener('input', toggleButton));

  postButton.addEventListener('click', () => {
    if (postButton.disabled) return;
    const payload = {
      name: nameInput.value.trim(),
      message: messageInput.value.trim()
    };
    fetch('/forum', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
      .then(res => res.ok ? res.json() : Promise.reject())
      .then(() => {
        inputs.forEach(i => i.value = '');
        postButton.disabled = true;
        loadPosts();
      })
      .catch(() => alert('Failed to post'));
  });

  const loadPosts = () => {
    fetch('/forum')
      .then(res => res.json())
      .then(posts => {
        const container = document.getElementById('postsContainer');
        container.innerHTML = '';
        posts.forEach(post => {
          const el = document.createElement('div');
          el.className = 'post';
          el.innerHTML = `<strong>${post.name}</strong><span>${post.timestamp}</span><p>${post.message}</p>`;
          container.appendChild(el);
        });
      })
      .catch(console.error);
  };

  loadPosts();
});
