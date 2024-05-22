document.getElementById('generate').addEventListener('click', function() {
    const payload = {
        event: document.getElementById('event').value,
        segment: document.getElementById('segment').value,
        creative_image: document.getElementById('creative_image').value,
        project_logo: document.getElementById('project_logo').value,
        phone: document.getElementById('phone').value,
        website: document.getElementById('website').value
    };

    fetch('http://localhost:5000/creatives', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'Success') {
            console.log('Creative generated:', data.data);
            const htmlContent = atob(data.data.creatives_html);
            const blob = new Blob([htmlContent], { type: 'text/html' });
            const url = URL.createObjectURL(blob);
            
            const downloadLink = document.getElementById('download-link');
            downloadLink.href = url;
            downloadLink.style.display = 'inline';
        } else {
            console.error('Error generating creative:', data.data);
            alert('Error generating creative');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error: ' + error);
    });
});
