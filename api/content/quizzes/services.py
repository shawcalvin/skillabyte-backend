from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from api.users.models import Learner
from api.courses.models import Course
from .models import Quiz, QuizAttempt, Question, AnswerChoice, QuestionCompletion

class QuizService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(QuizService, cls).__new__(cls)
        return cls._instance

    def create_quiz(self, course_id: int, title: str, description: str = None):
        """
        Create a new quiz for a given course.
        """
        try:
            course = Course.objects.get(id=course_id)
        except ObjectDoesNotExist:
            return None

        quiz = Quiz.objects.create(course=course, title=title, description=description)
        return quiz

    def add_question(self, quiz_id: int, question_text: str, question_num: int):
        """
        Add a new question to a quiz.
        """
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except ObjectDoesNotExist:
            return None

        question = Question.objects.create(quiz=quiz, question=question_text, question_num=question_num)
        return question

    def add_answer_choice(self, question_id: int, answer_text: str, answer_num: int, is_correct: bool, feedback: str):
        """
        Add a new answer choice to a specific question.
        """
        try:
            question = Question.objects.get(id=question_id)
        except ObjectDoesNotExist:
            return None

        answer_choice = AnswerChoice.objects.create(
            question=question, 
            answer=answer_text, 
            answer_num=answer_num, 
            is_correct=is_correct, 
            feedback=feedback
        )
        return answer_choice

    def get_quiz(self, course_id: int = None, quiz_id: int = None):
        """
        Retrieve a quiz by either course_id or quiz_id.
        If course_id is provided, return all quizzes for that course.
        If quiz_id is provided, return the specific quiz.
        """

        quiz = None

        if quiz_id is not None:
            try:
                quiz = Quiz.objects.prefetch_related('question_set__answerchoice_set').get(id=quiz_id)
            except Quiz.DoesNotExist:
                return None

        elif course_id is not None:
            try:
                quiz = Quiz.objects.prefetch_related('question_set__answerchoice_set').get(course_id=course_id)
            except Quiz.DoesNotExist:
                return None

        return quiz

    def create_quiz_attempt(self, learner_id: int, quiz_id: int):
        """
        Start a new quiz attempt for a learner.
        """
        try:
            learner = Learner.objects.get(id=learner_id)
            quiz = Quiz.objects.get(id=quiz_id)
        except ObjectDoesNotExist:
            return None
        
        quiz_attempt, created = QuizAttempt.objects.get_or_create(
            learner=learner, 
            quiz=quiz,
            time_submitted__isnull=True,
            defaults={'learner': learner, 'quiz': quiz}
        )
        return quiz_attempt

    def grade_quiz_attempt(self, quiz_attempt_id: int, answers: list):
        """
        Grades the quiz attempt by creating QuestionCompletion entries and calculating the score.
        """
        try:
            quiz_attempt = QuizAttempt.objects.get(id=quiz_attempt_id)
        except QuizAttempt.DoesNotExist:
            return None

        total_questions = 0
        correct_answers = 0

        for answer_data in answers:
            question_id = answer_data['question']
            selected_answer_id = answer_data['answer']

            try:
                question = Question.objects.get(id=question_id, quiz=quiz_attempt.quiz)
                selected_answer = AnswerChoice.objects.get(id=selected_answer_id, question=question)
            except (Question.DoesNotExist, AnswerChoice.DoesNotExist):
                return None

            self.create_question_completion(quiz_attempt.id, question.id, selected_answer.id)

            total_questions += 1
            if selected_answer.is_correct:
                correct_answers += 1

        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

        quiz_attempt.score = score
        quiz_attempt.time_submitted = timezone.now()
        quiz_attempt.save()

        return score

    def get_quiz_attempt(self, quiz_attempt_id: int):
        """
        Retrieve details of a quiz attempt.
        """
        try:
            quiz_attempt = QuizAttempt.objects.prefetch_related(
                'questioncompletion_set__question',
                'questioncompletion_set__given_answer'
            ).get(id=quiz_attempt_id)
            return quiz_attempt
        except ObjectDoesNotExist:
            return None
        
    def list_quiz_attempts(self, learner_id: int, course_id: int = None):
        """
        Retrieve all quiz attempts made by a specific learner.
        If course_id is provided, retrieve quiz attempts for the specific learner and course.
        """
        try:
            learner = Learner.objects.get(id=learner_id)
        except ObjectDoesNotExist:
            return None

        if course_id:
            try:
                course = Course.objects.get(id=course_id)
            except ObjectDoesNotExist:
                return None

            return QuizAttempt.objects.filter(
                learner=learner,
                quiz__course=course
            ).select_related('quiz').all()

        return QuizAttempt.objects.filter(learner=learner).select_related('quiz').all()

    def create_question_completion(self, quiz_attempt_id: int, question_id: int, answer_choice_id: int):
        """
        Record the learner's answer to a question in a quiz attempt.
        """
        try:
            quiz_attempt = QuizAttempt.objects.get(id=quiz_attempt_id)
            question = Question.objects.get(id=question_id)
            answer_choice = AnswerChoice.objects.get(id=answer_choice_id)
        except ObjectDoesNotExist:
            return None

        question_completion, created = QuestionCompletion.objects.update_or_create(
            quiz_attempt=quiz_attempt,
            question=question,
            defaults={'given_answer': answer_choice}
        )

        return question_completion

    def get_question_feedback(self, question_completion_id: int):
        """
        Retrieve feedback for a specific question in a quiz attempt.
        """
        try:
            question_completion = QuestionCompletion.objects.get(id=question_completion_id)
        except ObjectDoesNotExist:
            return None

        return question_completion.given_answer.feedback

    def delete_quiz(self, quiz_id: int):
        """
        Delete a quiz and all associated questions and answers.
        """
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except ObjectDoesNotExist:
            return False

        quiz.delete()
        return True