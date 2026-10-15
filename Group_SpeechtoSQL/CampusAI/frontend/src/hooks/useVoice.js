import { useState, useRef, useCallback, useEffect } from 'react';

export function useVoice(onTranscript) {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState(null);
  const recognitionRef = useRef(null);
  const callbackRef = useRef(onTranscript);

  // Keep callback reference up to date without triggering re-binds
  useEffect(() => {
    callbackRef.current = onTranscript;
  }, [onTranscript]);

  const startListening = useCallback(() => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setError('Speech recognition is not supported in this browser. Please use Google Chrome or Edge.');
      return;
    }

    // Stop any existing instance
    if (recognitionRef.current) {
      try { recognitionRef.current.abort(); } catch (_) {}
    }

    const recognition = new SpeechRecognition();
    recognition.lang = navigator.language || 'en-US';
    recognition.interimResults = true;
    recognition.continuous = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      setIsListening(true);
      setError(null);
      setTranscript('');
    };

    recognition.onresult = (event) => {
      let currentText = '';
      for (let i = 0; i < event.results.length; i++) {
        currentText += event.results[i][0].transcript;
      }

      setTranscript(currentText);

      // Stream text live to input box
      if (callbackRef.current && currentText.trim()) {
        callbackRef.current(currentText);
      }
    };

    recognition.onerror = (e) => {
      if (e.error === 'no-speech' || e.error === 'aborted') {
        setIsListening(false);
        return;
      }
      setError(`Voice error: ${e.error}`);
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognitionRef.current = recognition;

    try {
      recognition.start();
    } catch (err) {
      console.error(err);
      setIsListening(false);
    }
  }, []);

  const stopListening = useCallback(() => {
    if (recognitionRef.current) {
      try { recognitionRef.current.stop(); } catch (_) {}
    }
    setIsListening(false);
  }, []);

  const clearTranscript = () => setTranscript('');

  return { isListening, transcript, error, startListening, stopListening, clearTranscript };
}