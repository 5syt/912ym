import { useState } from 'react';
import { Link } from 'react-router-dom';
import { ChevronLeft, ChevronRight, Home, CheckCircle2, XCircle } from 'lucide-react';
import { judgeQuestions } from '@/data/questions';
import { useQuizStore } from '@/store/quizStore';

export default function JudgePage() {
  const [idx, setIdx] = useState(0);
  const { judgeAnswers, judgeSubmitted, setJudgeAnswer, submitJudge } = useQuizStore();
  const q = judgeQuestions[idx];
  const selected = judgeAnswers[q.id];
  const submitted = judgeSubmitted[q.id];
  const isCorrect = submitted && selected === q.answer;

  const handleSelect = (val: boolean) => {
    if (submitted) return;
    setJudgeAnswer(q.id, val);
  };

  const handleSubmit = () => {
    if (selected === undefined) return;
    submitJudge(q.id);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Header */}
      <div className="sticky top-0 z-10 bg-slate-950/90 backdrop-blur border-b border-slate-800">
        <div className="max-w-3xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors">
            <Home className="w-4 h-4" />
            <span className="text-sm">首页</span>
          </Link>
          <div className="text-sm font-medium text-amber-400">
            判断题 {idx + 1} / {judgeQuestions.length}
          </div>
          <div className="flex items-center gap-1">
            {judgeQuestions.map((_, i) => (
              <button
                key={i}
                onClick={() => setIdx(i)}
                className={`w-2 h-2 rounded-full transition-colors ${
                  i === idx ? 'bg-amber-400' : judgeSubmitted[judgeQuestions[i].id] ? 'bg-slate-600' : 'bg-slate-800'
                }`}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Question */}
      <div className="max-w-3xl mx-auto px-6 py-10">
        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-8">
          <h2 className="text-lg font-semibold mb-8 leading-relaxed">{q.question}</h2>

          <div className="grid grid-cols-2 gap-4">
            <button
              onClick={() => handleSelect(true)}
              className={`py-6 rounded-xl border-2 font-bold text-xl transition-all duration-200 ${
                submitted
                  ? (q.answer === true ? 'border-emerald-500/60 bg-emerald-500/10 text-emerald-400' : selected === true ? 'border-red-500/60 bg-red-500/10 text-red-400' : 'border-slate-700 bg-slate-800/50 text-slate-500')
                  : selected === true ? 'border-amber-500 bg-amber-500/10 text-amber-400' : 'border-slate-700 bg-slate-800/50 text-slate-300 hover:border-slate-600'
              }`}
            >
              <div className="flex flex-col items-center gap-2">
                <CheckCircle2 className="w-8 h-8" />
                <span>正确</span>
              </div>
            </button>
            <button
              onClick={() => handleSelect(false)}
              className={`py-6 rounded-xl border-2 font-bold text-xl transition-all duration-200 ${
                submitted
                  ? (q.answer === false ? 'border-emerald-500/60 bg-emerald-500/10 text-emerald-400' : selected === false ? 'border-red-500/60 bg-red-500/10 text-red-400' : 'border-slate-700 bg-slate-800/50 text-slate-500')
                  : selected === false ? 'border-amber-500 bg-amber-500/10 text-amber-400' : 'border-slate-700 bg-slate-800/50 text-slate-300 hover:border-slate-600'
              }`}
            >
              <div className="flex flex-col items-center gap-2">
                <XCircle className="w-8 h-8" />
                <span>错误</span>
              </div>
            </button>
          </div>

          {/* Submit / Analysis */}
          {!submitted ? (
            <button
              onClick={handleSubmit}
              disabled={selected === undefined}
              className="mt-6 w-full py-3 rounded-xl bg-amber-600 hover:bg-amber-500 disabled:bg-slate-700 disabled:text-slate-500 font-semibold transition-colors"
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
                <span className="text-slate-500 text-sm ml-2">
                  正确答案：{q.answer ? '正确 ✓' : '错误 ✗'}
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
            onClick={() => setIdx(Math.min(judgeQuestions.length - 1, idx + 1))}
            disabled={idx === judgeQuestions.length - 1}
            className="flex items-center gap-1 px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 disabled:opacity-30 transition-colors text-sm"
          >
            下一题 <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
