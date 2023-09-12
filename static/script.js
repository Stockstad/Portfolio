let letter = 0;
var interval;

function begin(){
   
    interval = setInterval(welcome_message, 15);
    
    
}


function welcome_message() {
    let text = "Welcome to my website! Here you can find a little bit about me and my projects. Please check out my socials down below! ;)";
    const message = text.split("")
    document.getElementById('mess').innerHTML += message[letter];
    letter+=1;
    if (letter === message.length) {
        clearInterval(interval);
    }
}