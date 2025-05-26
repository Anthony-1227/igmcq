 function checkAnswer(button, isCorrect) {
      const result = document.getElementById('result');
      if (isCorrect) {
        result.textContent = "Correct!";
        result.style.color = "green";
      } else {
        result.textContent = "Wrong answer. Try again!";
        result.style.color = "red";
      }
    }