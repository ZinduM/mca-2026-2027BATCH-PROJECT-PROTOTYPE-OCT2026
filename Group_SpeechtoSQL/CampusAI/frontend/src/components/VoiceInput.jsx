import { useState, useRef, useCallback } from 'react';
import { Mic, MicOff, Square, Send, Edit3, Volume2 } from 'lucide-react';
import { useVoice } from '../hooks/useVoice';
import Alert from './Alert';

export default function VoiceInput({ onSubmit, placeholder = 'Ask anything about campus data…', isLoading = false }) {
  const [text, setText] = useState('');
  const inputRef = useRef(null);

  // Directly sync transcribed voice into the textarea
  const handleTranscript = useCallback((spokenText) => {
    setText(spokenText);
  }, []);

  const { isListening, transcript, error, startListening, stopListening, clearTranscript } = useVoice(handleTranscript);

  const handleSubmit = () => {
    const query = text.trim();
    if (!query || isLoading) return;
    onSubmit(query);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const toggleListen = () => {
    if (isListening) {
      stopListening();
    } else {
      clearTranscript();
      startListening();
    }
  };

  const displayError = error && !error.toLowerCase().includes('no-speech') && !error.toLowerCase().includes('aborted')
    ? error
    : null;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      {/* Big microphone button */}
      <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 8 }}>
        <div style={{ position: 'relative' }}>
          {isListening && (
            <>
              <div style={{
                position: 'absolute', inset: -12, borderRadius: '50%',
                background: 'rgba(13,148,136,0.15)',
                animation: 'pulse-ring 1.5s cubic-bezier(0.215,0.61,0.355,1) infinite',
              }} />
              <div style={{
                position: 'absolute', inset: -24, borderRadius: '50%',
                background: 'rgba(13,148,136,0.08)',
                animation: 'pulse-ring 1.5s cubic-bezier(0.215,0.61,0.355,1) infinite 0.2s',
              }} />
            </>
          )}
          <button
            id="voice-mic-btn"
            type="button"
            onClick={toggleListen}
            disabled={isLoading}
            style={{
              width: 72, height: 72,
              borderRadius: '50%',
              border: 'none',
              cursor: isLoading ? 'not-allowed' : 'pointer',
              background: isListening
                ? 'linear-gradient(135deg, #ef4444, #dc2626)'
                : 'linear-gradient(135deg, var(--teal-dark), var(--teal-light))',
              color: 'white',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              boxShadow: isListening
                ? '0 8px 25px rgba(239,68,68,0.45)'
                : '0 8px 25px rgba(13,148,136,0.45)',
              transition: 'all 0.3s ease',
              transform: isListening ? 'scale(1.05)' : 'scale(1)',
              position: 'relative',
              zIndex: 1,
            }}
          >
            {isListening
              ? <Square size={28} fill="white" />
              : <Mic size={28} />
            }
          </button>
        </div>
      </div>

      {/* Listening indicator */}
      {isListening && (
        <div style={{
          display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8,
          color: '#ef4444', fontWeight: 600, fontSize: 14,
        }}>
          <Volume2 size={16} />
          <span>Listening… speak now</span>
          {[0, 1, 2].map((i) => (
            <span
              key={i}
              style={{
                width: 6, height: 6, borderRadius: '50%', background: '#ef4444',
                animation: `bounce-dots 0.8s ease ${i * 0.15}s infinite`,
                display: 'inline-block',
              }}
            />
          ))}
        </div>
      )}

      {/* Text input row */}
      <div style={{ display: 'flex', gap: 10 }}>
        <div style={{ flex: 1, position: 'relative' }}>
          <textarea
            id="query-input"
            ref={inputRef}
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            rows={2}
            className="input"
            style={{ resize: 'none', paddingRight: 40, lineHeight: 1.5 }}
          />
          {text && (
            <button
              type="button"
              onClick={() => setText('')}
              style={{
                position: 'absolute', top: 10, right: 10,
                background: 'none', border: 'none', cursor: 'pointer',
                color: 'var(--text-muted)',
              }}
              title="Clear"
            >
              <MicOff size={16} />
            </button>
          )}
        </div>
        <button
          id="query-submit-btn"
          type="button"
          className="btn btn-primary"
          onClick={handleSubmit}
          disabled={!text.trim() || isLoading}
          style={{ alignSelf: 'flex-end', padding: '11px 20px' }}
        >
          {isLoading ? (
            <span style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
              <span className="spinner" style={{ width: 16, height: 16 }} />
              Processing…
            </span>
          ) : (
            <>
              <Send size={16} />
              Ask AI
            </>
          )}
        </button>
      </div>

      {displayError && <Alert type="error" message={displayError} />}

      <p style={{ fontSize: 12, color: 'var(--text-muted)', textAlign: 'center' }}>
        <Edit3 size={12} style={{ marginRight: 4, verticalAlign: 'middle' }} />
        Click the mic to speak, or type your query and press Enter
      </p>
    </div>
  );
}