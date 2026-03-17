document.getElementById("downloadBtn").addEventListener("click", function() {
    // 1. Pega a URL que o usuário digitou
    const url = document.getElementById("urlInput").value;

    // 2. Atualiza o status na tela
    document.getElementById("status").innerText = "Downloading...";

    // 3. Faz a requisição POST para o backend
    fetch("http://192.168.1.119:8000/download", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url })
    })
    // 4. Converte a resposta para JSON
    .then(response => response.json())

    // 5. Usa o resultado
    .then(data => {
        if (data.status === "success") {
            document.getElementById("status").innerText = "✅ Downloaded: " + data.file;
        } else {
            document.getElementById("status").innerText = "❌ Error: " + data.detail;
        }
    })

    // 6. Captura erros de rede
    .catch(error => {
        document.getElementById("status").innerText = "❌ Network error: " + error;
    });
});