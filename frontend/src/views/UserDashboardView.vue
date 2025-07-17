<template>
  <div class="user-dashboard">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-lg-3 col-md-4">
        <BaseSidebar user-role="user" />
      </div>
      
      <!-- Main Content -->
      <div class="col-lg-9 col-md-8">
        <!-- Header -->
        <div class="dashboard-header glass mb-5">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h1 class="text-light mb-2">Welcome back, {{ user.name }}!</h1>
              <p class="text-secondary mb-0 fs-5">{{ getGreeting() }} - Ready to continue your learning journey?</p>
            </div>
            <SearchBar v-model="searchQuery" placeholder="Search quizzes, subjects..." />
          </div>
        </div>

        <!-- Statistics Row -->
        <div class="row mb-5">
          <div class="col-xl-3 col-lg-6 mb-4">
            <StatsWidget
              :value="stats.totalQuizzesTaken"
              label="Quizzes Completed"
              icon="bi bi-check-circle"
              color="success"
              trend="+3"
              trend-direction="up"
            />
          </div>
          <div class="col-xl-3 col-lg-6 mb-4">
            <StatsWidget
              :value="stats.averageScore"
              label="Average Score"
              icon="bi bi-graph-up"
              color="primary"
              trend="+5%"
              trend-direction="up"
            />
          </div>
          <div class="col-xl-3 col-lg-6 mb-4">
            <StatsWidget
              :value="stats.currentStreak"
              label="Day Streak"
              icon="bi bi-fire"
              color="warning"
              trend="+2"
              trend-direction="up"
            />
          </div>
          <div class="col-xl-3 col-lg-6 mb-4">
            <StatsWidget
              :value="stats.bestSubject"
              label="Best Subject"
              icon="bi bi-trophy"
              color="info"
              trend="Web Dev"
              trend-direction="up"
            />
          </div>
        </div>

        <!-- Upcoming Quizzes Section -->
        <div class="row mb-5">
          <div class="col-12">
            <DashboardCard title="Upcoming Quizzes" icon="bi bi-calendar-event">
              <div class="row">
                <div 
                  v-for="quiz in upcomingQuizzes" 
                  :key="quiz.id" 
                  class="col-lg-4 col-md-6 mb-4"
                >
                  <UpcomingQuizCard 
                    :quiz="quiz"
                    @start-quiz="handleStartQuiz"
                    @view-details="handleViewDetails"
                  />
                </div>
              </div>
            </DashboardCard>
          </div>
        </div>

        <!-- Recent Performance & Subject Progress -->
        <div class="row">
          <!-- Recent Performance -->
          <div class="col-lg-6 mb-4">
            <DashboardCard title="Recent Performance" icon="bi bi-clock-history">
              <div class="row">
                <div 
                  v-for="score in recentScores" 
                  :key="score.id" 
                  class="col-12 mb-3"
                >
                  <RecentScoreCard 
                    :score="score"
                    @view-details="handleViewScoreDetails"
                    @retake-quiz="handleRetakeQuiz"
                  />
                </div>
              </div>
            </DashboardCard>
          </div>

          <!-- Subject Progress -->
          <div class="col-lg-6 mb-4">
            <DashboardCard title="Subject Progress" icon="bi bi-bar-chart">
              <div class="row">
                <div 
                  v-for="subject in subjectProgress" 
                  :key="subject.id" 
                  class="col-12 mb-3"
                >
                  <SubjectProgress 
                    :subject="subject"
                    @start-quiz="handleStartSubjectQuiz"
                    @review-subject="handleReviewSubject"
                    @view-details="handleViewSubjectDetails"
                  />
                </div>
              </div>
            </DashboardCard>
          </div>
        </div>

        <!-- Available Quizzes Section -->
        <div class="row mb-5">
          <div class="col-12">
            <DashboardCard title="Available Quizzes" icon="bi bi-play-circle">
              <div class="row">
                <div 
                  v-for="quiz in availableQuizzes" 
                  :key="quiz.id" 
                  class="col-lg-4 col-md-6 mb-4"
                >
                  <QuizCard 
                    :quiz="quiz"
                    @start-quiz="handleStartQuiz"
                    @continue-quiz="handleContinueQuiz"
                    @view-result="handleViewResult"
                    @view-details="handleViewDetails"
                  />
                </div>
              </div>
            </DashboardCard>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BaseSidebar from '../components/BaseSidebar.vue'
import DashboardCard from '../components/DashboardCard.vue'
import SearchBar from '../components/SearchBar.vue'
import StatsWidget from '../components/StatsWidget.vue'
import QuizCard from '../components/QuizCard.vue'
import UpcomingQuizCard from '../components/UpcomingQuizCard.vue'
import RecentScoreCard from '../components/RecentScoreCard.vue'
import SubjectProgress from '../components/SubjectProgress.vue'

export default {
  name: 'UserDashboardView',
  components: {
    BaseSidebar,
    DashboardCard,
    SearchBar,
    StatsWidget,
    QuizCard,
    UpcomingQuizCard,
    RecentScoreCard,
    SubjectProgress
  },
  data() {
    return {
      searchQuery: '',
      user: {
        name: 'John Doe',
        role: 'user'
      },
      stats: {
        totalQuizzesTaken: 12,
        averageScore: 85,
        currentStreak: 7,
        bestSubject: 'Web Dev'
      },
      upcomingQuizzes: [
        {
          id: 1,
          title: 'JavaScript Advanced',
          subject: 'Web Development',
          date: '2024-01-15T10:00:00',
          duration: '45 min',
          questionCount: 20,
          difficulty: 'Hard',
          status: 'upcoming'
        },
        {
          id: 2,
          title: 'Python Fundamentals',
          subject: 'Programming',
          date: '2024-01-18T14:00:00',
          duration: '30 min',
          questionCount: 15,
          difficulty: 'Medium',
          status: 'upcoming'
        },
        {
          id: 3,
          title: 'Database Design',
          subject: 'Computer Science',
          date: '2024-01-20T09:00:00',
          duration: '60 min',
          questionCount: 25,
          difficulty: 'Hard',
          status: 'upcoming'
        }
      ],
      recentScores: [
        {
          id: 1,
          quizId: 1,
          quizTitle: 'JavaScript Basics',
          subject: 'Web Development',
          percentage: 85,
          correctAnswers: 17,
          incorrectAnswers: 3,
          totalQuestions: 20,
          timeTaken: '25 min',
          completedAt: '2024-01-10T14:30:00',
          feedback: 'Great performance! You showed strong understanding of JavaScript fundamentals. Consider practicing more on async functions.'
        },
        {
          id: 2,
          quizId: 2,
          quizTitle: 'HTML Fundamentals',
          subject: 'Web Development',
          percentage: 92,
          correctAnswers: 23,
          incorrectAnswers: 2,
          totalQuestions: 25,
          timeTaken: '20 min',
          completedAt: '2024-01-08T11:15:00',
          feedback: 'Excellent work! Your HTML knowledge is solid. Keep up the great work!'
        },
        {
          id: 3,
          quizId: 3,
          quizTitle: 'CSS Styling',
          subject: 'Web Development',
          percentage: 78,
          correctAnswers: 15,
          incorrectAnswers: 4,
          totalQuestions: 19,
          timeTaken: '35 min',
          completedAt: '2024-01-05T16:45:00',
          feedback: 'Good effort! Focus on CSS Grid and Flexbox concepts for improvement.'
        }
      ],
      subjectProgress: [
        {
          id: 1,
          name: 'Web Development',
          icon: 'bi bi-code-slash',
          progress: 75,
          completedQuizzes: 6,
          remainingQuizzes: 2,
          averageScore: 82,
          bestScore: 95,
          color: '#0D6EFD'
        },
        {
          id: 2,
          name: 'Programming',
          icon: 'bi bi-cpu',
          progress: 45,
          completedQuizzes: 3,
          remainingQuizzes: 4,
          averageScore: 78,
          bestScore: 88,
          color: '#198754'
        },
        {
          id: 3,
          name: 'Computer Science',
          icon: 'bi bi-laptop',
          progress: 20,
          completedQuizzes: 1,
          remainingQuizzes: 5,
          averageScore: 70,
          bestScore: 70,
          color: '#FFC107'
        }
      ],
      availableQuizzes: [
        {
          id: 4,
          title: 'React Basics',
          subject: 'Web Development',
          duration: '40 min',
          questionCount: 18,
          difficulty: 'Medium',
          status: 'available'
        },
        {
          id: 5,
          title: 'Vue.js Fundamentals',
          subject: 'Web Development',
          duration: '35 min',
          questionCount: 16,
          difficulty: 'Medium',
          status: 'available'
        },
        {
          id: 6,
          title: 'Python OOP',
          subject: 'Programming',
          duration: '50 min',
          questionCount: 22,
          difficulty: 'Hard',
          status: 'available'
        }
      ]
    }
  },
  methods: {
    getGreeting() {
      const hour = new Date().getHours()
      if (hour < 12) return 'Good morning'
      if (hour < 18) return 'Good afternoon'
      return 'Good evening'
    },
    handleStartQuiz(quizId) {
      console.log('Starting quiz:', quizId)
      // Navigate to quiz taking interface
      this.$router.push(`/quiz/${quizId}/take`)
    },
    handleContinueQuiz(quizId) {
      console.log('Continuing quiz:', quizId)
      // Navigate to quiz taking interface with saved progress
      this.$router.push(`/quiz/${quizId}?continue=true`)
    },
    handleViewResult(quizId) {
      console.log('Viewing result for quiz:', quizId)
      // Navigate to quiz result view
      this.$router.push(`/result/${quizId}`)
    },
    handleViewDetails(quizId) {
      console.log('Viewing details for quiz:', quizId)
      // Navigate to quiz details view
      this.$router.push(`/quiz/${quizId}/details`)
    },
    handleViewScoreDetails(scoreId) {
      console.log('Viewing score details:', scoreId)
      // Navigate to detailed score view
      this.$router.push(`/score/${scoreId}`)
    },
    handleRetakeQuiz(quizId) {
      console.log('Retaking quiz:', quizId)
      // Navigate to quiz taking interface
      this.$router.push(`/quiz/${quizId}?retake=true`)
    },
    handleStartSubjectQuiz(subjectId) {
      console.log('Starting quiz for subject:', subjectId)
      // Navigate to quiz taking interface for specific subject
      this.$router.push(`/subject/${subjectId}/quiz`)
    },
    handleReviewSubject(subjectId) {
      console.log('Reviewing subject:', subjectId)
      // Navigate to subject review interface
      this.$router.push(`/subject/${subjectId}/review`)
    },
    handleViewSubjectDetails(subjectId) {
      console.log('Viewing subject details:', subjectId)
      // Navigate to subject details view
      this.$router.push(`/subject/${subjectId}`)
    }
  }
}
</script>

<style scoped>
.user-dashboard {
  padding: 2rem;
}

.dashboard-header {
  background: rgba(35, 43, 51, 0.8);
  border-radius: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  padding: 2rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .user-dashboard {
    padding: 1rem;
  }
  
  .dashboard-header {
    padding: 1.5rem;
  }
}
</style> 