import { useState, useCallback, useEffect, useRef } from 'react';
import emotions from '../mocks/emotions.json';

const successMessages = ['כל הכבוד!', 'נכון מאוד!', 'יפה מאוד!', 'מצוין!', 'אתה אלוף!', 'איזו הצלחה!'];
const errorMessages = ['לא נורא', 'אולי בפעם הבאה', 'נסה שוב', 'כמעט!', 'בוא ננסה עוד פעם'];

const TARGET_EMOTION = 'שמח';

const pickRandom = (arr) => arr[Math.floor(Math.random() * arr.length)];

const pickRoundEmotions = () => {
  const target = emotions.find((e) => e.name === TARGET_EMOTION);
  const distractors = emotions
    .filter((e) => e.name !== TARGET_EMOTION)
    .sort(() => Math.random() - 0.5)
    .slice(0, 3);
  return [...distractors, target].sort(() => Math.random() - 0.5);
};

const useGameRound = () => {
  const [roundEmotions, setRoundEmotions] = useState(() => pickRoundEmotions());
  const [feedback, setFeedback] = useState(null);
  const [isError, setIsError] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  const timerRef = useRef(null);

  useEffect(() => {
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, []);

  const handleEmotionClick = useCallback((emotionName) => {
    if (emotionName === TARGET_EMOTION) {
      setFeedback(pickRandom(successMessages));
      setIsError(false);
      setShowConfetti(true);
    } else {
      setFeedback(pickRandom(errorMessages));
      setIsError(true);
      setShowConfetti(false);
    }

    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(() => {
      setFeedback(null);
      setShowConfetti(false);
      setIsError(false);
      setRoundEmotions(pickRoundEmotions());
      timerRef.current = null;
    }, 2500);
  }, []);

  const resetGame = useCallback(() => {
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = null;
    setFeedback(null);
    setShowConfetti(false);
    setIsError(false);
    setRoundEmotions(pickRoundEmotions());
  }, []);

  return { roundEmotions, feedback, isError, showConfetti, handleEmotionClick, resetGame };
};

export default useGameRound;
