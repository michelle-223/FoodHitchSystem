// chat/static/chat/chat_room.js

document.addEventListener('DOMContentLoaded', function () {
    const chatRoomId = JSON.parse(document.getElementById('chat-room-id').textContent); // Accessing the ID safely

    // WebSocket connection
    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + chatRoomId + '/'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const messageElement = document.createElement('div');
        messageElement.textContent = data.message;
        document.querySelector('#messages').appendChild(messageElement);
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    // Handle sending messages
    document.querySelector('#send-button').onclick = function(e) {
        const messageInput = document.querySelector('#message-input');
        const message = messageInput.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInput.value = '';
    };
});
