const e = React.createElement;

function Chatbot() {
  const [messages, setMessages] = React.useState([
    { sender: 'bot', text: 'Hello! Ask me about weather, crops, pests, or soil.' }
  ]);
  const [input, setInput] = React.useState('');
  const [loading, setLoading] = React.useState(false);
  const messagesEndRef = React.useRef(null);

  React.useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);
    try {
      const res = await fetch('http://localhost:5500/api/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      });
      const data = await res.json();
      if (res.ok) {
        setMessages(prev => [...prev, { sender: 'bot', text: data.reply }]);
      } else {
        setMessages(prev => [...prev, { sender: 'bot', text: data.error || "Something went wrong" }]);
      }
    } catch {
      setMessages(prev => [...prev, { sender: 'bot', text: 'Error connecting to server.' }]);
    }
    setLoading(false);
  };

  const onKeyPress = (event) => {
    if (event.key === 'Enter') {
      sendMessage();
    }
  };

  return e(
    'div',
    null,
    e(
      'div',
      { className: 'chat-window' },
      messages.map((msg, i) =>
        e(
          'div',
          { key: i, className: `message ${msg.sender}` },
          (msg.sender === 'user' ? 'You: ' : 'Bot: ') + msg.text
        )
      ),
      e('div', { ref: messagesEndRef })
    ),
    e(
      'div',
      { className: 'input-row' },
      e('input', {
        type: 'text',
        placeholder: 'Type your message...',
        value: input,
        onChange: (e) => setInput(e.target.value),
        onKeyPress: onKeyPress,
        disabled: loading
      }),
      e(
        'button',
        { onClick: sendMessage, disabled: loading },
        loading ? 'Loading...' : 'Send'
      )
    )
  );
}

const container = document.getElementById('root');
const root = ReactDOM.createRoot(container);
root.render(e(Chatbot));
