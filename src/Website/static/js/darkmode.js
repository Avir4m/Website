let darkMode = localStorage.getItem('darkMode'); 

const darkModeToggle = document.querySelector('#dark-mode-toggle');

const enableDarkMode = () => {
  document.getElementById('darkModeCss').href = "/static/css/darkmode.css"
  localStorage.setItem('darkMode', 'enabled');
}

const disableDarkMode = () => {
  document.getElementById('darkModeCss').href = "/static/css/lightmode.css"
  localStorage.setItem('darkMode', 'disabled');
}

if (darkMode === 'enabled') {
  enableDarkMode();
}


darkModeToggle.addEventListener('click', () => {
  darkMode = localStorage.getItem('darkMode'); 
  if (darkMode !== 'enabled') {
    enableDarkMode();
  } 
  else {  
    disableDarkMode(); 
  }});