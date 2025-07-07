function startTranslation() {
    const input = document.getElementById('inputText').value;
    const loading = document.getElementById('loading');
    const resultDiv = document.getElementById('translatedResult');
    const timeSpan = document.getElementById('timeStat');
    const tokenSpan = document.getElementById('tokenStat');

    if (!input) {
        alert('请输入要翻译的内容');
        return;
    }

    loading.style.display = 'block';
    resultDiv.innerHTML = '';

    fetch('/api/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: input })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        resultDiv.textContent = data.translated;
        timeSpan.textContent = `用时：${data.elapsed.toFixed(2)}s`;
        tokenSpan.textContent = `Tokens：${data.tokens}`;
    })
    .catch(error => {
        console.error('Error:', error);
        resultDiv.textContent = `翻译出错：${error.message}`;
    })
    .finally(() => {
        loading.style.display = 'none';
    });
}
