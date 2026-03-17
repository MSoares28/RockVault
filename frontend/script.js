const downloadBtn = document.getElementById("downloadBtn");
const urlInput = document.getElementById("urlInput");
const statusDiv = document.getElementById("status");
const progressContainer = document.getElementById("progressContainer");
const progressBar = document.getElementById("progressBar");
const fileList = document.getElementById("fileList");

// ===== Download =====
downloadBtn.addEventListener("click", function () {
    const url = urlInput.value.trim();

    if (!url) {
        setStatus("Please paste a YouTube URL first.", "error");
        return;
    }

    downloadBtn.disabled = true;
    downloadBtn.textContent = "Downloading...";
    showProgress();
    setStatus("", "");

    fetch(`${CONFIG.API_BASE_URL}/download`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url })
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(err.detail || "Unknown error");
                });
            }

        // Extract filename from Content-Disposition header
        const disposition = response.headers.get("Content-Disposition");
        let filename = "download.mp3";

        if (disposition) {
            // Try UTF-8 encoded filename first (filename*=UTF-8''...)
            const utf8Match = disposition.match(/filename\*=UTF-8''([^;]+)/i);
            // Fallback to plain filename="..."
            const plainMatch = disposition.match(/filename="?([^";]+)"?/i);

            if (utf8Match) {
                filename = decodeURIComponent(utf8Match[1]);
            } else if (plainMatch) {
                filename = plainMatch[1];
            }
        }

        return response.blob().then(blob => ({ blob, filename }));
    })
        .then(({ blob, filename }) => {
            // Trigger browser download
            const blobUrl = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = blobUrl;
            a.download = filename;
            a.click();
            URL.revokeObjectURL(blobUrl);

            setStatus("✅ Downloaded: " + filename, "success");
            urlInput.value = "";
            loadHistory();
        })
        .catch(error => {
            setStatus("❌ Error: " + error.message, "error");
        })
        .finally(() => {
            downloadBtn.disabled = false;
            downloadBtn.textContent = "Download";~
            hideProgress();
        });
});

// ===== File List =====
function loadHistory() {
    fetch(`${CONFIG.API_BASE_URL}/history`)
        .then(response => response.json())
        .then(data => {
            fileList.innerHTML = "";

            if (data.total === 0) {
                fileList.innerHTML = "<li class='empty'>No downloads yet.</li>";
                return;
            }

            data.history.forEach(record => {
                const li = document.createElement("li");

                const info = document.createElement("div");
                info.className = "file-info";

                const name = document.createElement("span");
                name.textContent = record.title;
                name.className = "file-name";

                const date = document.createElement("span");
                date.textContent = record.downloaded_at;
                date.className = "file-date";

                info.appendChild(name);
                info.appendChild(date);
                li.appendChild(info);
                fileList.appendChild(li);
            });
        })
        .catch(() => {
            fileList.innerHTML = "<li class='empty'>Could not load history.</li>";
        });
}

// Load history on page open
loadHistory();

// ===== Helpers =====
function setStatus(message, type) {
    statusDiv.textContent = message;
    statusDiv.className = type;
}

// Load files on page open
loadFiles();

function showProgress() {
    progressContainer.classList.add("active");
    progressBar.classList.add("indeterminate");
}

function hideProgress() {
    progressContainer.classList.remove("active");
    progressBar.classList.remove("indeterminate");
}