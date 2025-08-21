from rest_framework import serializers
from .models import Quiz, QuizAttempt, Question, AnswerChoice, QuestionCompletion

from api.courses.serializers import CourseSerializer
        
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'course', 'title', 'description']


class QuizAttemptSerializer(serializers.ModelSerializer):
    score = serializers.ReadOnlyField()

    class Meta:
        model = QuizAttempt
        fields = ['id', 'learner', 'quiz', 'time_started', 'time_submitted', 'score']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'question', 'question_num']


class AnswerChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerChoice
        fields = ['id', 'question', 'answer', 'answer_num', 'is_correct', 'feedback']


class QuestionCompletionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = QuestionCompletion
        fields = ['question', 'given_answer']


class QuestionDetailsSerializer(serializers.ModelSerializer):
    answer_choices = AnswerChoiceSerializer(many=True, read_only=True, source='answerchoice_set')

    class Meta:
        model = Question
        fields = ['id', 'question', 'question_num', 'answer_choices']


class QuizDetailsSerializer(serializers.ModelSerializer):
    questions = QuestionDetailsSerializer(many=True, read_only=True, source='question_set')
    course = CourseSerializer()

    class Meta:
        model = Quiz
        fields = ['id', 'course', 'title', 'description', 'questions']


class ProtectedAnswerChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerChoice
        fields = ['id', 'question', 'answer', 'answer_num']


class ProtectedQuestionDetailsSerializer(serializers.ModelSerializer):
    answer_choices = ProtectedAnswerChoiceSerializer(many=True, read_only=True, source='answerchoice_set')

    class Meta:
        model = Question
        fields = ['id', 'question', 'question_num', 'answer_choices']

class ProtectedQuizDetailsSerializer(serializers.ModelSerializer):
    questions = ProtectedQuestionDetailsSerializer(many=True, read_only=True, source='question_set')
    course = CourseSerializer()

    class Meta:
        model = Quiz
        fields = ['id', 'course', 'title', 'description', 'questions']

class ProtectedQuizAttemptDetailsSerializer(serializers.ModelSerializer):
    score = serializers.ReadOnlyField()
    quiz = ProtectedQuizDetailsSerializer()
    question_completions = QuestionCompletionSerializer(many=True, source='questioncompletion_set')

    class Meta:
        model = QuizAttempt
        fields = ['id', 'learner', 'quiz', 'time_started', 'time_submitted', 'score', 'question_completions']