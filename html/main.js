function checkAnswer(button, isCorrect) {
  const result = document.getElementById('result');

  // Reset all buttons (optional)
  document.querySelectorAll('.answers button').forEach(btn => {
    btn.style.backgroundColor = ''; // Clear previous styles
  });

  // Set color based on correctness
  if (isCorrect) {
    button.style.backgroundColor = 'lightgreen';
    result.textContent = "Correct!";
    result.style.color = "green";
  } else {
    button.style.backgroundColor = 'lightcoral';
    result.textContent = "Wrong. Try again!";
    result.style.color = "red";
  }
}
