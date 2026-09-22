const text = "Your Trusted Platform For Renting Cars, Bikes, Halls, Offices, And Houses!";
const typingSpeed = 100; // Speed in milliseconds
let index = 0;

function typeText() {
  const typedText = document.getElementById("typed-text");
  if (index < text.length) {
    typedText.textContent += text.charAt(index);
    index++;
    setTimeout(typeText, typingSpeed);
  }
}

window.onload = typeText;
