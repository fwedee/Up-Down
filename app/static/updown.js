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