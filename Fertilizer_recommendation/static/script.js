document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('fertilizer-form');
    const resultDiv = document.getElementById('result');
    const themeBtn = document.getElementById('toggle-theme');
    let currentTheme = localStorage.getItem('theme') || "dark";
    document.documentElement.setAttribute('data-theme', currentTheme);

    // Toggle dark/light theme
    themeBtn.addEventListener('click', () => {
        currentTheme = currentTheme === "dark" ? "light" : "dark";
        document.documentElement.setAttribute('data-theme', currentTheme);
        themeBtn.textContent = currentTheme === "dark" ? "🌙 Dark Mode" : "🌞 Light Mode";
        localStorage.setItem('theme', currentTheme);
    });
    themeBtn.textContent = currentTheme === "dark" ? "🌙 Dark Mode" : "🌞 Light Mode";

    // Handle form submit
    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        resultDiv.textContent = "🔍 Predicting best fertilizer...";
        resultDiv.classList.remove("error");
        resultDiv.style.display = "block";

        // Gather form input
        const formData = new FormData(form);
        const data = {};
        for (const [key, value] of formData.entries()) {
            data[key] = isNaN(value) ? value : Number(value);
        }
        try {
            const resp = await fetch("/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });
            const res = await resp.json();
            if (resp.ok) {
                resultDiv.textContent = "✅ Recommended Fertilizer: " + res.predicted_fertilizer;
                resultDiv.classList.remove("error");
            } else {
                resultDiv.textContent = "❌ " + (res.error || "Unknown error.");
                resultDiv.classList.add("error");
            }
        } catch (err) {
            resultDiv.textContent = "❌ Server error or network issue.";
            resultDiv.classList.add("error");
        }
    });
});
