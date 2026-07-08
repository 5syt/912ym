import { useState } from 'react';
import { Link } from 'react-router-dom';
import { ChevronLeft, ChevronRight, Home, CheckCircle2, XCircle } from 'lucide-react';
import { choiceQuestions } from '@/data/questions';
import { useQuizStore } from '@/store/quizStore';

export default function ChoicePage() {
  const [idx, setIdx] = useState(0);
  const { choiceAnswers, choiceSubmitted, setChoiceAnswer, submitChoice } = useQuizStore();
  const q = choiceQuestions[idx];
  const selected = choiceAnswers[q.id];
  const submitted = choiceSubmitted[q.id];
  const isCorrect = submitted && selected === q.answer;

  const handleSelect = (optIdx: number) => {
    if (submitted) return;
    setChoiceAnswer(q.id, optIdx);
  };

  const handleSubmit = () => {
    if (selected === undefined) return;
    submitChoice(q.id);
  };

  const optionLabels = ['A', 'B', 'C', 'D'];

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Header */}
      <div className="sticky top-0 z-10 bg-slate-950/90 backdrop-blur border-b border-slate-800">
        <div className="max-w-3xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors">
            <Home className="w-4 h-4" />
            <span className="text-sm">首页</span>
          </Link>
          <div className="text-sm font-medium text-blue-400">
            选择题 {idx + 1} / {choiceQuestions.length}
          </div>
          <div className="flex items-center gap-1">
            {choiceQuestions.map((_, i) => (
              <button
                key={i}
                onClick={() => setIdx(i)}
                className={`w-2 h-2 rounded-full transition-colors ${
                  i === idx ? 'bg-blue-400' : choiceSubmitted[choiceQuestions[i].id] ? 'bg-slate-600' : 'bg-slate-800'
                }`}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Question */}
      <div className="max-w-3xl mx-auto px-6 py-10">
        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-8">
          <h2 className="text-lg font-semibold mb-6 leading-relaxed">{q.question}</h2>

          <div className="space-y-3">
            {q.options.map((opt, i) => {
              let cls = 'border-slate-700 bg-slate-800/50 hover:border-slate-600 hover:bg-slate-800';
              if (submitted) {
                if (i === q.answer) cls = 'border-emerald-500/60 bg-emerald-500/10';
                else if (i === selected && i !== q.answer) cls = 'border-red-500/60 bg-red-500/10';
              } else if (i === selected) {
                cls = 'border-blue-500 bg-blue-500/10';
              }

              return (
                <button
                  key={i}
                  onClick={() => handleSelect(i)}
                  className={`w-full text-left px-5 py-4 rounded-xl border transition-all duration-200 ${cls}`}
                >
                  <div className="flex items-center gap-3">
                    <span className={`w-7 h-7 rounded-lg flex items-center justify-center text-sm font-bold shrink-0 ${
                      submitted && i === q.answer ? 'bg-emerald-500 text-white' :
                      submitted && i === selected && i !== q.answer ? 'bg-red-500 text-white' :
                      i === selected ? 'bg-blue-500 text-white' : 'bg-slate-700 text-slate-300'
                    }`}>
                      {optionLabels[i]}
                    </span>
                    <span className="text-slate-200">{opt}</span>
                    {submitted && i === q.answer && <CheckCircle2 className="w-5 h-5 text-emerald-400 ml-auto shrink-0" />}
                    {submitted && i === selected && i !== q.answer && <XCircle className="w-5 h-5 text-red-400 ml-auto shrink-0" />}
                  </div>
                </button>
              );
            })}
          </div>

          {/* Submit / Analysis */}
          {!submitted ? (
            <button
              onClick={handleSubmit}
              disabled={selected === undefined}
              className="mt-6 w-full py-3 rounded-xl bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 disabled:text-slate-500 font-semibold transition-colors"
            >
              提交答案
            </button>
          ) : (
            <div className={`mt-6 p-5 rounded-xl border ${isCorrect ? 'border-emerald-500/30 bg-emerald-500/5' : 'border-red-500/30 bg-red-500/5'}`}>
              <div className="flex items-center gap-2 mb-2">
                {isCorrect ? (
                  <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                ) : (
                  <XCircle className="w-5 h-5 text-red-400" />
                )}
                <span className={`font-semibold ${isCorrect ? 'text-emerald-400' : 'text-red-400'}`}>
                  {isCorrect ? '回答正确' : '回答错误'}
                </span>
              </div>
              <p className="text-slate-400 text-sm leading-relaxed">{q.analysis}</p>
            </div>
          )}
        </div>

        {/* Navigation */}
        <div className="flex items-center justify-between mt-6">
          <button
            onClick={() => setIdx(Math.max(0, idx - 1))}
            disabled={idx === 0}
            className="flex items-center gap-1 px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 disabled:opacity-30 transition-colors text-sm"
          >
            <ChevronLeft className="w-4 h-4" /> 上一题
          </button>
          <button
            onClick={() => setIdx(Math.min(choiceQuestions.length - 1, idx + 1))}
            disabled={idx === choiceQuestions.length - 1}
            className="flex items-center gap-1 px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 disabled:opacity-30 transition-colors text-sm"
          >
            下一题 <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
