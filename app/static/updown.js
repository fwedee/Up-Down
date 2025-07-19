const textInput = document.getElementById('textInput');
const textButton = document.getElementById('textButton');
const someText = document.getElementById('someText');
const formText = document.getElementById('formText');

textButton.addEventListener('click', function(){
    let text = textInput.innerText;
    sendText(text).then(r => updateTextField() )
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

        const newText = document.createElement('p');
        newText.textContent = result.text
        someText.appendChild(newText)
        console.log(result)

    }catch (error){
        console.error('Error', error);
    }
}

async function updateTextField(){

    const newText = document.createElement('p');
    newText.textContent = 'test'
    someText.appendChild(newText)
}

 const socket = io();

    socket.on('connect', () => {
        console.log('Connected to WebSocket server');
        socket.emit('get_files');
    });

    socket.on('files_update', (data) => {
        updateFileList(data.files);
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