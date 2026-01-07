export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          MedAdReview
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          AI 기반 의료광고 자동 심의 시스템
        </p>
        <div className="space-x-4">
          <a
            href="/login"
            className="inline-flex items-center px-6 py-3 bg-emerald-500 hover:bg-emerald-600 text-white font-medium rounded-lg transition-colors"
          >
            로그인
          </a>
          <a
            href="/docs"
            className="inline-flex items-center px-6 py-3 border border-gray-300 bg-white hover:bg-gray-50 text-gray-700 font-medium rounded-lg transition-colors"
          >
            API 문서
          </a>
        </div>
      </div>
    </main>
  );
}
