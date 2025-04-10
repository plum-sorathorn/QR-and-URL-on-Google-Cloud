const form = document.getElementById('urlForm');
const longUrlInput = document.getElementById('longUrl');
const resultDiv = document.getElementById('result');
const shortUrlLink = document.getElementById('shortUrlLink');
const qrImage = document.getElementById('qrImage');
const errorDiv = document.getElementById('error');

// POST to shorten to retrieve qr and url
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  resultDiv.classList.add('hidden');
  errorDiv.classList.add('hidden');

  const longUrl = longUrlInput.value;

  try {
    const response = await fetch('/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url: longUrl })
    });

    const data = await response.json();

    if (response.ok) {
      // shortened url
      shortUrlLink.href = data.short_url;
      shortUrlLink.textContent = data.short_url;

      // qr code
      qrImage.src = data.qr_url;
      qrImage.classList.remove('hidden');

      resultDiv.classList.remove('hidden');
    } else {
      errorDiv.textContent = data.error || 'An error occurred';
      errorDiv.classList.remove('hidden');
    }
  } catch (err) {
    errorDiv.textContent = 'Could not connect to the server.';
    errorDiv.classList.remove('hidden');
  }
});
