const form = document.getElementById("upload-form");
const resultSection = document.getElementById("result-section");
const statsBody = document.getElementById("stats-table-body");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById("file-input");
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("/file/new", {
        method: "POST",
        body: formData
    });

    if (!res.ok) {
        alert("Ошибка при загрузке файла.");
        return;
    }

    const data = await res.json();
    const fileId = data.file_id;

    const statsRes = await fetch(`/file?file_id=${fileId}&limit=50&offset=0`);
    const stats = await statsRes.json();

    statsBody.innerHTML = "";

    stats.forEach((row, index) => {
        const tr = document.createElement("tr");

        const numberTd = document.createElement("td");
        numberTd.textContent = index + 1;

        const wordTd = document.createElement("td");
        wordTd.textContent = row.word;

        const tfTd = document.createElement("td");
        tfTd.textContent = row.tf.toFixed(5);

        const idfTd = document.createElement("td");
        idfTd.textContent = row.idf.toFixed(5);

        tr.appendChild(numberTd);
        tr.appendChild(wordTd);
        tr.appendChild(tfTd);
        tr.appendChild(idfTd);

        statsBody.appendChild(tr);
    });

    resultSection.style.display = "block";
});
