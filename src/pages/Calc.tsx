import { useState } from 'react';
import { Link } from 'react-router-dom';
import { ChevronLeft, ChevronRight, Home, Eye, EyeOff } from 'lucide-react';
import { calcQuestions } from '@/data/questions';
import { useQuizStore } from '@/store/quizStore';

export default function CalcPage() {
  const [idx, setIdx] = useState(0);
  const { revealedCalc, toggleCalc } = useQuizStore();
  const q = calcQuestions[idx];
  const revealed = revealedCalc[q.id] || false;

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Header */}
      <div className="sticky top-0 z-10 bg-slate-950/90 backdrop-blur border-b border-slate-800">
        <div className="max-w-3xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors">
            <Home className="w-4 h-4" />
            <span className="text-sm">首页</span>
          </Link>
          <div className="text-sm font-medium text-purple-400">
            计算题 {idx + 1} / {calcQuestions.length}
          </div>
          <div className="flex items-center gap-1">
            {calcQuestions.map((_, i) => (
              <button
                key={i}
                onClick={() => setIdx(i)}
                className={`w-2 h-2 rounded-full transition-colors ${
                  i === idx ? 'bg-purple-400' : revealedCalc[calcQuestions[i].id] ? 'bg-slate-600' : 'bg-slate-800'
                }`}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Question */}
      <div className="max-w-3xl mx-auto px-6 py-10">
        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-8">
          <h2 className="text-lg font-semibold mb-6 leading-relaxed whitespace-pre-wrap">{q.question}</h2>

          <button
            onClick={() => toggleCalc(q.id)}
            className="w-full py-3 rounded-xl bg-purple-600/20 hover:bg-purple-600/30 border border-purple-500/30 text-purple-400 font-semibold transition-colors flex items-center justify-center gap-2"
          >
            {revealed ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            {revealed ? '隐藏解题过程' : '显示解题过程'}
          </button>

          {revealed && (
            <div className="mt-5 p-5 rounded-xl border border-purple-500/20 bg-purple-500/5">
              <div className="text-sm font-semibold text-purple-400 mb-3">解题过程</div>
              <div className="text-slate-300 text-sm leading-relaxed whitespace-pre-wrap">{q.answer}</div>
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
            onClick={() => setIdx(Math.min(calcQuestions.length - 1, idx + 1))}
            disabled={idx === calcQuestions.length - 1}
            className="flex items-center gap-1 px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 disabled:opacity-30 transition-colors text-sm"
          >
            下一题 <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
