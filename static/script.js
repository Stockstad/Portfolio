"use strict";

const tech_buttons = document.querySelectorAll(".p-button");
const selected_techs = [];
const apply_button = document.getElementById("apply-button");
const add_tech_button = document.getElementById("add-tech");
const tech_box = document.getElementById("tech-box");
let tech_to_add = [];

tech_buttons.forEach(button => {
  button.addEventListener("click", () => {
    const value = button.value;
    if (!selected_techs.includes(value)) {
      button.style.opacity = "50%";
      selected_techs.push(value);

      updateTechButtons();
      
    }
    else {
      button.style.opacity = "100%";
      selected_techs.pop(value);
      updateTechButtons();
    }

  });
});

function updateTechButtons() {
  document.getElementById('debug').innerHTML = selected_techs;

}

function sendData(st) {
  $.ajax({
      url: '/process',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(st),
      success: function(response) {
          console.log(response);
          location.reload();
          selected_techs = [];_
      }, 
      error: function(error) {
          console.log(error);
      }
  });
}

apply_button.addEventListener("click", () => {
  sendData(selected_techs);
});




