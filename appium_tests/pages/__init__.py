# pages/__init__.py

from .base_page       import BasePage
from .login_page      import LoginPage
from .register_page   import RegisterPage
from .dashboard_page  import DashboardPage
from .exam_page       import ExamPage
from .flashcard_page  import FlashcardPage
from .practice_page   import PracticePage
from .document_page   import DocumentPage
from .profile_page    import ProfilePage
from .chatbot_page    import ChatbotPage
from .roadmap_page    import RoadmapPage
from .admin_login_page import AdminLoginPage
from .admin_dashboard_page import AdminDashboardPage
from .admin_user_page import AdminUserPage
from .admin_question_page import AdminQuestionPage
from .admin_exam_management_page import AdminExamManagementPage
from .admin_subject_topic_practice_page import AdminSubjectTopicPracticePage
from .admin_document_roadmap_page import AdminDocumentRoadmapPage
from .user_profile_goal_schedule_page import UserProfileGoalSchedulePage
from .user_exam_history_rankings_stats_page import UserExamHistoryRankingsStatsPage
from .user_flashcards_chatbot_roadmap_page import UserFlashcardsChatbotRoadmapPage

__all__ = [
    "BasePage",
    "LoginPage",
    "RegisterPage",
    "DashboardPage",
    "ExamPage",
    "FlashcardPage",
    "PracticePage",
    "DocumentPage",
    "ProfilePage",
    "ChatbotPage",
    "RoadmapPage",
    "AdminLoginPage",
    "AdminDashboardPage",
    "AdminUserPage",
    "AdminQuestionPage",
    "AdminExamManagementPage",
    "AdminSubjectTopicPracticePage",
    "AdminDocumentRoadmapPage",
    "UserProfileGoalSchedulePage",
    "UserExamHistoryRankingsStatsPage",
    "UserFlashcardsChatbotRoadmapPage",
]
