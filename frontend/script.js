const generateButton = document.getElementById('generateBtn');
const promptInput = document.getElementById('promptInput');
const videoContainer = document.getElementById('videoContainer'); // Make sure you have this in HTML!

generateButton.addEventListener('click', async () => {
    const prompt = promptInput.value.trim();
    if (!prompt) {
        alert('Please enter a prompt!');
        return;
    }

    try {
        // 1. Show a loading state on the button so you know it's working
        generateButton.innerText = "Generating Video (takes 10-20 seconds)...";
        generateButton.disabled = true;

        // 2. Send the prompt to your FastAPI backend
        const response = await fetch('http://127.0.0.1:8000/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt }),
        });

        // 3. Wait for the backend to reply with the video URL
        const data = await response.json();
        
        if (data.video_url) {
            // 4. Inject an HTML5 Video Player into your webpage playing the AI video URL
            videoContainer.innerHTML = `
                <video controls autoplay loop width="100%" style="border-radius: 8px; margin-top: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                    <source src="${data.video_url}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            `;
        } else {
            alert("Could not get a video URL back from the AI model.");
        }
        
    } catch (error) {
        console.error('Error:', error);
        alert("An error occurred while communicating with your AI backend.");
    } finally {
        // 5. Reset the button back to normal
        generateButton.innerText = "Generate Video";
        generateButton.disabled = false;
    }
});
