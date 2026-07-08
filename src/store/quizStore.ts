import { create } from 'zustand';

interface QuizState {
  choiceAnswers: Record<number, number>;
  judgeAnswers: Record<number, boolean>;
  choiceSubmitted: Record<number, boolean>;
  judgeSubmitted: Record<number, boolean>;
  revealedShort: Record<number, boolean>;
  revealedCalc: Record<number, boolean>;
  setChoiceAnswer: (id: number, answer: number) => void;
  setJudgeAnswer: (id: number, answer: boolean) => void;
  submitChoice: (id: number) => void;
  submitJudge: (id: number) => void;
  toggleShort: (id: number) => void;
  toggleCalc: (id: number) => void;
  resetAll: () => void;
}

export const useQuizStore = create<QuizState>((set) => ({
  choiceAnswers: {},
  judgeAnswers: {},
  choiceSubmitted: {},
  judgeSubmitted: {},
  revealedShort: {},
  revealedCalc: {},
  setChoiceAnswer: (id, answer) =>
    set((s) => ({ choiceAnswers: { ...s.choiceAnswers, [id]: answer } })),
  setJudgeAnswer: (id, answer) =>
    set((s) => ({ judgeAnswers: { ...s.judgeAnswers, [id]: answer } })),
  submitChoice: (id) =>
    set((s) => ({ choiceSubmitted: { ...s.choiceSubmitted, [id]: true } })),
  submitJudge: (id) =>
    set((s) => ({ judgeSubmitted: { ...s.judgeSubmitted, [id]: true } })),
  toggleShort: (id) =>
    set((s) => ({ revealedShort: { ...s.revealedShort, [id]: !s.revealedShort[id] } })),
  toggleCalc: (id) =>
    set((s) => ({ revealedCalc: { ...s.revealedCalc, [id]: !s.revealedCalc[id] } })),
  resetAll: () =>
    set({
      choiceAnswers: {},
      judgeAnswers: {},
      choiceSubmitted: {},
      judgeSubmitted: {},
      revealedShort: {},
      revealedCalc: {},
    }),
}));
