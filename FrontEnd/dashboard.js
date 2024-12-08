document.addEventListener('DOMContentLoaded', () => {
    // Get all save buttons for saving prompts
    const saveButtons = document.querySelectorAll('.save-prompt');

    // Loop through each save button and add an event listener
    saveButtons.forEach(button => {
        button.addEventListener('click', async (event) => {
            // Get the relevant agent card for this button
            const agentCard = event.target.closest('.agent-card');
            
            // Get the message (prompt) and the agent's ID from the card
            const promptText = agentCard.querySelector('.prompt-input').value;
            const agentId = agentCard.getAttribute('data-id');
            
            // Validate that both message and assistant_id are present
            if (!promptText || !agentId) {
                alert('Please enter a prompt and select an assistant.');
                return;
            }
            
            try {
                // Send the POST request with the prompt and assistant_id
                const response = await fetch('http://127.0.0.1:5000/api/prompt', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: promptText, // Send the message (prompt)
                        assistant_id: agentId, // Send the assistant's ID
                    }),
                });

                // Handle the response from the server
                const data = await response.json();
                
                if (response.ok) {
                    // Success - display message from server
                    console.log('Prompt saved successfully:', data.message);
                    alert(data.message);
                } else {
                    // Error - display error message from server
                    console.error('Error saving prompt:', data.error);
                    alert(`Error: ${data.error}`);
                }
            } catch (error) {
                console.error('Error during request:', error);
                alert('There was an error processing your request.');
            }
        });
    });

    // Modal functionality
    const modal = document.getElementById('create-agent-modal');
    const openModalButton = document.getElementById('create-agent-button');
    const closeButton = document.querySelector('.close-button');
 
    // Open modal
    openModalButton.addEventListener('click', () => {
        modal.style.display = 'flex';
    });
 
    // Close modal
    closeButton.addEventListener('click', () => {
        modal.style.display = 'none';
    });
 
    // Close modal when clicking outside the modal content
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
 
    // Form submission inside the modal for creating a new agent
    const createAgentForm = modal.querySelector('form');
    createAgentForm.addEventListener('submit', async (event) => {
        event.preventDefault();
 
        const agentName = document.getElementById('agent-name').value.trim();
        const agentUrl = document.getElementById('agent-url').value.trim();
 
        if (!agentName || !agentUrl) {
            alert('Please fill in all fields.');
            return;
        }
 
        try {
            // Send POST request to create the new agent
            const response = await fetch('http://127.0.0.1:5000/api/assistants', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: agentName,
                    image_url: agentUrl,
                }),
            });

            // Handle the response from the server
            const data = await response.json();

            if (response.ok) {
                // Success - display message from server
                console.log('Agent created successfully:', data.message);
                alert(data.message);

                // Optionally add the new agent to the UI
                const agentsSection = document.querySelector('.agents');
                const newAgentCard = `
                    <div class="agent-card" data-id="${data.assistant.id}">
                        <img src="${data.assistant.image_url || 'https://via.placeholder.com/70'}" alt="${data.assistant.name}" class="agent-pic">
                        <h3>${data.assistant.name}</h3>
                        <span class="status ${data.assistant.status ? 'active' : 'inactive'}">${data.assistant.status ? 'Active' : 'Inactive'}</span>
                        <textarea class="prompt-input" placeholder="Enter a prompt for ${data.assistant.name}"></textarea>
                        <button class="btn btn-secondary save-prompt">Save</button>
                    </div>
                `;
                agentsSection.insertAdjacentHTML('beforeend', newAgentCard);

                // Close the modal
                modal.style.display = 'none';
                createAgentForm.reset();
            } else {
                // Error - display error message from server
                console.error('Error creating agent:', data.error);
                alert(`Error: ${data.error}`);
            }
        } catch (error) {
            console.error('Error during request:', error);
            alert('There was an error creating the agent.');
        }
    });
 
    // Chatbot functionality
    const chatHistory = document.getElementById('chat-history');
    const chatInput = document.getElementById('chat-message');
    const sendChatButton = document.getElementById('send-chat');
  
    // Add event listener to send message
    sendChatButton.addEventListener('click', async () => {
        const userMessage = chatInput.value.trim();
  
        if (!userMessage) {
            alert('Please enter a message.');
            return;
        }
  
        // Display user message in chat history
        const userChat = document.createElement('p');
        userChat.innerHTML = `<b>You:</b> ${userMessage}`;
        chatHistory.appendChild(userChat);
        chatInput.value = '';
  
        try {
            // Send user message to chatbot API
            const response = await fetch('http://127.0.0.1:5000/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage }),
            });
  
            // Handle response from chatbot API
            const data = await response.json();
            const botMessage = document.createElement('p');

            if (response.ok) {
                const botReply = data.bot_message || "Sorry, I couldn't understand that.";
                botMessage.innerHTML = `<b>Bot:</b> ${botReply}`;
            } else {
                console.error('Error in chatbot response:', data.error);
                botMessage.innerHTML = `<b>Bot:</b> Sorry, there was an error processing your request.`;
            }
            chatHistory.appendChild(botMessage);
        } catch (error) {
            console.error('Error during chatbot request:', error);
            const errorMessage = document.createElement('p');
            errorMessage.innerHTML = `<b>Bot:</b> Unable to connect to the chatbot service.`;
            chatHistory.appendChild(errorMessage);
        }
    });
});
