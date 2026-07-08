import { Link } from 'react-router-dom';
import { BookOpen, CheckCircle, XCircle, MessageSquareText, Calculator, BarChart3 } from 'lucide-react';
import { choiceQuestions, judgeQuestions, shortQuestions, calcQuestions } from '@/data/questions';
import { useQuizStore } from '@/store/quizStore';

const categoryCards = [
  {
    title: '选择题',
    count: choiceQuestions.length,
    icon: CheckCircle,
    path: '/choice',
    gradient: 'from-blue-600 to-cyan-500',
    bg: 'bg-gradient-to-br from-blue-600 to-cyan-500',
  },
  {
    title: '判断题',
    count: judgeQuestions.length,
    icon: XCircle,
    path: '/judge',
    gradient: 'from-amber-500 to-orange-500',
    bg: 'bg-gradient-to-br from-amber-500 to-orange-500',
  },
  {
    title: '简答题',
    count: shortQuestions.length,
    icon: MessageSquareText,
    path: '/short',
    gradient: 'from-emerald-500 to-teal-500',
    bg: 'bg-gradient-to-br from-emerald-500 to-teal-500',
  },
  {
    title: '计算题',
    count: calcQuestions.length,
    icon: Calculator,
    path: '/calc',
    gradient: 'from-purple-600 to-pink-500',
    bg: 'bg-gradient-to-br from-purple-600 to-pink-500',
  },
];

export default function Home() {
  const { choiceSubmitted, judgeSubmitted, revealedShort, revealedCalc } = useQuizStore();

  const choiceCorrect = choiceQuestions.filter(
    (q) => choiceSubmitted[q.id] && choiceQuestions.find((cq) => cq.id === q.id)
  ).filter((q) => {
    const store = useQuizStore.getState();
    return store.choiceAnswers[q.id] === q.answer;
  }).length;

  const choiceDone = Object.keys(choiceSubmitted).length;
  const judgeDone = Object.keys(judgeSubmitted).length;
  const shortDone = Object.keys(revealedShort).length;
  const calcDone = Object.keys(revealedCalc).length;

  const totalQuestions = choiceQuestions.length + judgeQuestions.length + shortQuestions.length + calcQuestions.length;
  const totalDone = choiceDone + judgeDone + shortDone + calcDone;
  const progress = totalQuestions > 0 ? Math.round((totalDone / totalQuestions) * 100) : 0;

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Hero */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-950 via-blue-950/50 to-slate-950" />
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-blue-500/10 rounded-full blur-3xl" />
        <div className="relative max-w-5xl mx-auto px-6 pt-16 pb-12">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2.5 rounded-xl bg-blue-500/20 border border-blue-500/30">
              <BookOpen className="w-6 h-6 text-blue-400" />
            </div>
            <span className="text-sm font-medium text-blue-400 tracking-wider uppercase">2026 计算机网络</span>
          </div>
          <h1 className="text-5xl font-bold tracking-tight mb-3 bg-gradient-to-r from-white via-blue-100 to-blue-300 bg-clip-text text-transparent">
            计网知识点题库
          </h1>
          <p className="text-slate-400 text-lg max-w-xl">
            涵盖选择题、判断题、简答题、计算题，助你高效复习计算机网络核心知识点
          </p>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-6 pb-20 space-y-10">
        {/* Progress */}
        <div className="bg-slate-900/80 backdrop-blur border border-slate-800 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-blue-400" />
              <span className="font-semibold text-white">学习进度</span>
            </div>
            <span className="text-2xl font-bold text-blue-400">{progress}%</span>
          </div>
          <div className="w-full h-3 bg-slate-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-blue-500 to-cyan-400 rounded-full transition-all duration-700"
              style={{ width: `${progress}%` }}
            />
          </div>
          <div className="grid grid-cols-4 gap-4 mt-5 text-center">
            <div>
              <div className="text-2xl font-bold text-white">{choiceDone}</div>
              <div className="text-xs text-slate-500">选择题已做</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-white">{judgeDone}</div>
              <div className="text-xs text-slate-500">判断题已做</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-white">{shortDone}</div>
              <div className="text-xs text-slate-500">简答题已看</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-white">{calcDone}</div>
              <div className="text-xs text-slate-500">计算题已看</div>
            </div>
          </div>
        </div>

        {/* Category Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
          {categoryCards.map((card) => {
            const Icon = card.icon;
            return (
              <Link
                key={card.path}
                to={card.path}
                className="group relative overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/60 backdrop-blur p-6 transition-all duration-300 hover:border-slate-700 hover:shadow-lg hover:shadow-blue-500/5 hover:-translate-y-0.5"
              >
                <div className={`absolute top-0 right-0 w-32 h-32 ${card.bg} opacity-10 rounded-full blur-2xl group-hover:opacity-20 transition-opacity`} />
                <div className="relative">
                  <div className={`inline-flex p-3 rounded-xl ${card.bg} mb-4`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-white mb-1">{card.title}</h3>
                  <p className="text-slate-500 text-sm">共 {card.count} 题</p>
                </div>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
}
