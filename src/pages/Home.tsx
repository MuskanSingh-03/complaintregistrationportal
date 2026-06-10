export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-2xl mx-auto text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Campus Grievance Hub
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            A platform for students to report and track grievances on campus
          </p>
          <div className="space-y-4">
            <button className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-8 rounded-lg transition">
              Submit a Grievance
            </button>
            <p className="text-gray-600">
              Track your complaints and get real-time updates
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
