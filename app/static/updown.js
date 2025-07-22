const textInput = document.getElementById('textInput');
const textButton = document.getElementById('textButton');
const someText = document.getElementById('someText');
const formText = document.getElementById('formText');


document.getElementById('formText').addEventListener('submit', function (event){
    event.preventDefault();
    let text = textInput.value;
    sendText(text)
})

async function sendText(text){
    const url = formText.action;
    const data = {
        text: text
    };
    try{
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        // const newText = document.createElement('p');
        // newText.textContent = result.text
        // someText.appendChild(newText)
        // console.log(result)
    }catch (error){
        console.error('Error', error);
    }
}


async function updateTextField(texts) {
  const someText = document.getElementById("someText"); // Ensure this element exists
  someText.innerHTML = ''; // Clear existing content

  texts.forEach(text => {
    const fileItemDiv = document.createElement("div");
    fileItemDiv.className = "file-item";

    const p = document.createElement("p");
    p.textContent = text.content;
    p.style.cursor = "pointer";
    p.classList.add("truncate");

    fileItemDiv.addEventListener("click", () => {
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text.content)
          .then(() => {
           alert("Copied to clipboard!");
      })
      .catch(() => {
        fallbackCopyTextToClipboard(text.content);
      });
  } else {
    fallbackCopyTextToClipboard(text.content);
  }
});

    fileItemDiv.appendChild(p);
    someText.appendChild(fileItemDiv);
  });
}


const socket = io();

socket.on('connect', () => {
    console.log('Connected to WebSocket server');
    socket.emit('get_files');
    socket.emit('get_texts')
});

socket.on('files_update', (data) => {
    updateFileList(data.files);
});

socket.on('texts_update', (data) =>{
  updateTextField(data.texts)
});

function updateFileList(files) {
    const container = document.getElementById('files-container');
    container.innerHTML = files.map(file => `
        <div class="file-item">
            <span>${file.name}</span>
            <a href="${file.url}" class="btn">Download</a>
        </div>
    `).join('');
}

// Theme toggle functionality
document.querySelector('.theme-toggle').addEventListener('click', function() {
    document.body.style.filter = document.body.style.filter ? '' : 'invert(1)';
    this.textContent = this.textContent === '🌙' ? '☀️' : '🌙';
});

function fallbackCopyTextToClipboard(text) {
  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.style.position = "fixed";  // avoid scrolling
  textarea.style.opacity = "0";
  document.body.appendChild(textarea);
  textarea.focus();
  textarea.select();

  try {
    const successful = document.execCommand("copy");
    alert(successful ? "Copied to clipboard!" : "Copy failed.");
  } catch (err) {
    alert("Copy failed.");
  }

  document.body.removeChild(textarea);
}
