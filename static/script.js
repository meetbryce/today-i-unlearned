// remove/close button for flash messages
try {
  document.getElementById('js-remove-message').addEventListener('click', e => {
    e.preventDefault();
    document.getElementById('js-message').remove();
  });
} catch (e) {
  console.log('No flash message to add listener to');
}

// copy link to clipboard when "share" is pressed and add a query param to the URL for the backend to detect,
// if browser doesn't support copy to clipboard (unlikely: https://caniuse.com/mdn-api_clipboard_writetext) -- don't
document.querySelectorAll('.js-share-lesson')
  .forEach(el => el.addEventListener('click', e => {
    e.preventDefault();
    let href = el.getAttribute('href');
    navigator.clipboard.writeText(window.location.protocol + window.location.host + href)
      .then(() => {
        window.location = `${href}?share=true`;
      }, () => {
        window.location = href;
      });
  }));