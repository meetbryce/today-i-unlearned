// remove/close button for flash messages
document.getElementById('js-remove-message').addEventListener('click', e => {
  e.preventDefault();
  document.getElementById('js-message').remove();
});