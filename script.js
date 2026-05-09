const chatBox = document.getElementById("chat-box");

const userInput = document.getElementById("user-input");

/* =========================
   SEND MESSAGE
========================= */

async function sendMessage() {

    const message = userInput.value.trim();

    if(message === "") return;

    addMessage(message, "user");

    userInput.value = "";

    const typing = addTyping();

    try{

        const response = await fetch("/chat", {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                message:message
            })

        });

        const data = await response.json();

        typing.remove();

        typeMessage(
            data.reply,
            "bot"
        );

    }

    catch(error){

        typing.remove();

        addMessage(
            "❌ Error connecting to DARK AI",
            "bot"
        );
    }
}

/* =========================
   NORMAL MESSAGE
========================= */

function addMessage(text, sender){

    const div =
        document.createElement("div");

    div.classList.add(
        "message",
        sender
    );

    // IMAGE PREVIEW

    if(text.includes("https://image.pollinations.ai")){

        const imageUrl =
            text.split("\n\n")[1];

        div.innerHTML = `
            <p>🎨 Image Generated</p>

            <img src="${imageUrl}"
                 style="
                    width:100%;
                    margin-top:10px;
                    border-radius:15px;
                 ">
        `;
    }

    else{

        div.innerHTML = text;
    }

    chatBox.appendChild(div);

    chatBox.scrollTop =
        chatBox.scrollHeight;
}

/* =========================
   TYPE EFFECT
========================= */

function typeMessage(text, sender){

    const div =
        document.createElement("div");

    div.classList.add(
        "message",
        sender
    );

    chatBox.appendChild(div);

    let i = 0;

    const interval = setInterval(()=>{

        div.innerHTML += text.charAt(i);

        i++;

        chatBox.scrollTop =
            chatBox.scrollHeight;

        if(i >= text.length){

            clearInterval(interval);
        }

    },20);
}

/* =========================
   LOADING
========================= */

function addTyping(){

    const div =
        document.createElement("div");

    div.classList.add(
        "message",
        "bot"
    );

    div.innerHTML = "● ● ●";

    chatBox.appendChild(div);

    chatBox.scrollTop =
        chatBox.scrollHeight;

    return div;
}

/* =========================
   ENTER KEY
========================= */

userInput.addEventListener(
    "keypress",
    function(e){

        if(e.key === "Enter"){

            sendMessage();
        }
    }
);

/* =========================
   VOICE INPUT
========================= */

function startVoice(){

    const recognition =
        new webkitSpeechRecognition();

    recognition.lang = "en-US";

    recognition.start();

    recognition.onresult =
        function(event){

        const text =
            event.results[0][0].transcript;

        userInput.value = text;

        sendMessage();
    };
}

/* =========================
   SIDEBAR BUTTONS
========================= */

const buttons =
    document.querySelectorAll(".menu button");

/* DASHBOARD */

buttons[0].onclick = ()=>{

    addMessage(
        "📊 Welcome to DARK AI Dashboard 😎",
        "bot"
    );
};

/* CHATS */

buttons[1].onclick = ()=>{

    addMessage(
        "💬 Chat history feature coming soon 🔥",
        "bot"
    );
};

/* SEARCH */

buttons[2].onclick = ()=>{

    userInput.value =
        "latest AI news";

    userInput.focus();
};

/* IMAGES */

buttons[3].onclick = ()=>{

    userInput.value =
        "create image futuristic dark ai";

    userInput.focus();
};

/* SETTINGS */

buttons[4].onclick = ()=>{

    addMessage(
        "⚙ Settings panel coming soon 😎",
        "bot"
    );
};