async function analyzeText() {
    const textElement = document.getElementById("inputText");
    const resultElement = document.getElementById("result");

    if (!textElement || !resultElement) {
        console.warn("inputText or result element not found on page.");
        return;
    }

    const text = textElement.value;

    try {
        const response = await fetch("http://127.0.0.1:8000/api/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        resultElement.innerText = JSON.stringify(data, null, 2);
    } catch (err) {
        console.error("Error analyzing text:", err);
        resultElement.innerText = "Error analyzing text: " + err.message;
    }
}
