document.addEventListener('DOMContentLoaded', () => {
    const fields = ['work_type', 'number', 'date_needed', 'duration', 'village', 'taluka'];
    const inputs = fields.map(id => document.getElementById(id));
    const postBtn = document.getElementById('postBtn');

    inputs.forEach(i => i.addEventListener('input', () => {
        postBtn.disabled = inputs.some(inp => !inp.value.trim());
    }));

    postBtn.addEventListener('click', async () => {
        const data = Object.fromEntries(inputs.map(i => [i.id, i.value.trim()]));
        const res = await fetch('/post-labour', {
            method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data)
        });
        if (res.ok) loadLabourPosts();
        inputs.forEach(i => i.value = '');
        postBtn.disabled = true;
    });

    async function loadLabourPosts() {
        const posts = await (await fetch('/labour-posts')).json();
        const container = document.getElementById('postsContainer');
        container.innerHTML = '';
        posts.reverse().forEach(p => {
            const div = document.createElement('div');
            div.className = 'card';
            div.innerHTML = `<strong>${p.work_type}</strong> — ${p.number} ppl — ${p.duration} days<br>
        <small>${p.village}, ${p.taluka} on ${p.date_needed} • ${p.timestamp}</small>`;
            container.appendChild(div);
        });
    }
    loadLabourPosts();

    fetch('/alerts')
        .then(res => res.json())
        .then(alerts => {
            const ul = document.getElementById('alertsList');
            ul.innerHTML = alerts?.length
                ? alerts.map(a => `<li>${a}</li>`).join('')
                : '<li>No alerts available.</li>';
        })
        .catch(() => {
            document.getElementById('alertsList').innerHTML = '<li>Error loading alerts.</li>';
        });

    // News
    fetch('/news')
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById('newsList');
            list.innerHTML = '';

            // Knowivate returns an 'articles' array
            const items = data.articles ?? data.results ?? [];
            if (!items.length) {
                list.innerHTML = '<li>No agriculture news found.</li>';
                return;
            }

            items.slice(0, 5).forEach(n => {
                const title = n.title || 'No Title';
                const link = n.url || n.link || '#';
                list.innerHTML += `<li><a href="${link}" target="_blank">${title}</a></li>`;
            });
        })
        .catch(() => {
            document.getElementById('newsList').innerHTML = '<li>Error loading news.</li>';
        });

    window.toggleTheme = () => document.body.classList.toggle('dark-mode');
});
