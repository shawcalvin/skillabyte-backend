from rest_framework import views, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound

from .models import QuizAttempt, Question, AnswerChoice, Quiz
from .serializers import ProtectedQuizDetailsSerializer, ProtectedQuizAttemptDetailsSerializer, QuizAttemptSerializer, QuizDetailsSerializer
from .services import QuizService

from api.auth.permissions import IsOrganizationFacilitator, IsAttemptOwnerOrOrgFacilitator
from api.organizations.models import Organization
import traceback

class QuizAttemptViewSet(viewsets.ModelViewSet):
    queryset = QuizAttempt.objects.all()
    serializer_class = QuizAttemptSerializer


class QuizListView(views.APIView):
    permission_classes = [IsAuthenticated, IsOrganizationFacilitator]
    def get(self, request, organization_id, learner_id):
        try:
            organization = Organization.objects.get(id=organization_id)
            self.check_object_permissions(request, organization)

            attempts = QuizAttempt.objects.filter(
                learner_id = learner_id,
                learner__organizationlearner__organization_id=organization_id                                   
            )

            serializer = ProtectedQuizAttemptDetailsSerializer(attempts, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            print("UH OH")
            traceback.print_exc()


class QuizDetailsView(views.APIView):
    def get(self, request, course_id):
        quiz_service = QuizService()

        quiz = quiz_service.get_quiz(course_id=course_id)
        if quiz is None:
            raise NotFound(detail="No quiz found for given course.")
        
        serializer = ProtectedQuizDetailsSerializer(quiz)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UnprotectedQuizDetailsView(views.APIView):
    def get(self, request, course_id):
        quiz_service = QuizService()

        quiz = quiz_service.get_quiz(course_id=course_id)
        if quiz is None:
            raise NotFound(detail="No quiz found for given course.")
        
        serializer = QuizDetailsSerializer(quiz)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class QuizAttemptView(views.APIView):
    def get(self, request, course_id):
        quiz_service = QuizService()

        attempts = quiz_service.list_quiz_attempts(learner_id=request.user.learner_profile.pk, course_id=course_id)
        serializer = ProtectedQuizAttemptDetailsSerializer(attempts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, course_id):
        quiz_service = QuizService()
        quiz = quiz_service.get_quiz(course_id=course_id)
        attempt = quiz_service.create_quiz_attempt(request.user.learner_profile.pk, quiz.pk)

        serializer = ProtectedQuizAttemptDetailsSerializer(attempt)

        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizGradeView(views.APIView):
    def post(self, request, attempt_id):
        quiz_service = QuizService()
        answers = request.data.get('answers')

        score = quiz_service.grade_quiz_attempt(attempt_id, answers)

        if score is None:
            return Response({"error": "Failed to process quiz attempt."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(score, status=status.HTTP_200_OK)
    
class QuizAttemptFacilitatorView(views.APIView):
    permission_classes = [IsAuthenticated, IsAttemptOwnerOrOrgFacilitator]
    def get(self, request, organization_id, learner_id, attempt_id):
        quiz_service = QuizService()
        attempt = quiz_service.get_quiz_attempt(attempt_id)

        serializer = ProtectedQuizAttemptDetailsSerializer(attempt)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class QuizQuestionCompletionView(views.APIView):
    def post(self, request, attempt_id, question_id):
        quiz_service = QuizService()
        answer_id = request.data.get('answer_id')

        completion = quiz_service.create_question_completion(
            quiz_attempt_id=attempt_id,
            question_id=question_id,
            answer_choice_id=answer_id
        )

        if completion is None:
            return Response({"error": "Failed to process answer completion."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Recorded question completion."}, status=status.HTTP_200_OK)
    


quiz_data = {

}

class CreateQuiz(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        quiz, _ = Quiz.objects.get_or_create(
            course_id=quiz_data['course_id']
        )

        for question_data in quiz_data['questions']:
            question = Question.objects.create(
                quiz=quiz,
                question=question_data['question_text'],
                question_num=question_data['question_num']
            )
            for i, answer_data in enumerate(question_data['answer_choices'], start=1):
                AnswerChoice.objects.create(
                    question=question,
                    answer=answer_data['answer'],
                    answer_num=i,
                    is_correct=answer_data['is_correct'],
                    feedback=answer_data['feedback']
                )

        return Response(
            {"message": "Quiz created successfully!"},
            status=status.HTTP_201_CREATED
        )
        
quiz_data = {
    'course_id': 1,
    'questions': [
        {
            'question_num': 1,
            'question_text': 'Which clause is used to specify the table from which data is retrieved in a SQL query?',
            'answer_choices': [
                {'answer': 'SELECT', 'is_correct': False, 'feedback': 'Incorrect. SELECT specifies the columns to be returned, not the table.'},
                {'answer': 'FROM', 'is_correct': True, 'feedback': 'Correct.'},
                {'answer': 'WHERE', 'is_correct': False, 'feedback': 'Incorrect. WHERE is used to filter the dataset, not determine the source of the data.'},
                {'answer': 'ORDER BY', 'is_correct': False, 'feedback': 'Incorrect. ORDER BY is used to sort the dataset, not determine the source of the data.'},
            ]
        },
        {
            'question_num': 2,
            'question_text': 'What does the WHERE clause do in a SQL query?',
            'answer_choices': [
                {'answer': 'Sorts the result set', 'is_correct': False, 'feedback': 'Incorrect. ORDER BY sorts the result set, not WHERE.'},
                {'answer': 'Groups rows with similar values', 'is_correct': False, 'feedback': 'Incorrect. GROUP BY groups rows, not WHERE.'},
                {'answer': 'Filters rows based on specified conditions', 'is_correct': True, 'feedback': 'Correct.'},
                {'answer': 'Returns the first x number of rows.', 'is_correct': False, 'feedback': 'Incorrect. LIMIT returns the first x number of rows, not WHERE.'},
            ]
        },
        {
            'question_num': 3,
            'question_text': 'What is the purpose of the GROUP BY clause?',
            'answer_choices': [
                {'answer': 'To sort data in ascending or descending order', 'is_correct': False, 'feedback': 'Incorrect. This is the purpose of ORDER BY, not GROUP BY.'},
                {'answer': 'To combine multiple columns into a single row', 'is_correct': False, 'feedback': 'Incorrect. GROUP BY aggregates rows — it doesn’t combine columns.'},
                {'answer': 'To aggregate data into groups based on a column', 'is_correct': True, 'feedback': 'Correct.'},
                {'answer': 'To filter rows that match a condition', 'is_correct': False, 'feedback': 'Incorrect. This is the purpose of WHERE, not GROUP BY.'},
            ]
        },
        {
            'question_num': 4,
            'question_text': 'Which of the following SQL clauses can be used with aggregate functions (SUM(), COUNT(), etc.)?',
            'answer_choices': [
                {'answer': 'SELECT', 'is_correct': True, 'feedback': 'Correct.'},
                {'answer': 'WHERE', 'is_correct': False, 'feedback': 'Incorrect. WHERE filters the data before it gets aggregated. To filter after aggregation, you would use HAVING.'},
                {'answer': 'GROUP BY', 'is_correct': True, 'feedback': 'Correct.'},
                {'answer': 'HAVING', 'is_correct': True, 'feedback': 'Correct.'},
                {'answer': 'FROM', 'is_correct': False, 'feedback': 'Incorrect. The FROM statement is executed before GROUP BY and can’t pull data directly from aggregate functions.'},
            ]
        },
        {
            'question_num': 5,
            'question_text': 'Which of the following best describes the SELECT clause in SQL?',
            'answer_choices': [
                {'answer': 'It indicates which columns (or expressions) should be retrieved from the table', 'is_correct': True, 'feedback': 'Correct.'},
                {'answer': 'It sets the condition used to filter rows', 'is_correct': False, 'feedback': 'Incorrect. This is a better description for the WHERE clause. SELECT doesn’t filter rows but rather selects columns.'},
                {'answer': 'It sorts the rows in ascending or descending order', 'is_correct': False, 'feedback': 'Incorrect. This describes the ORDER BY clause. SELECT doesn’t sort data.'},
                {'answer': 'It groups rows by a specific column', 'is_correct': False, 'feedback': 'Incorrect. SELECT indicates the columns to retrieve but doesn’t group rows.'},
            ]
        },
        {
            'question_num': 6,
            'question_text': 'Which SQL clause would sort the output in descending order, where [field1] represents the field being sorted?',
            'answer_choices': [
                {'answer': 'SORT BY [field1]', 'is_correct': False, 'feedback': 'Incorrect. ORDER BY should be used, not SORT BY.'},
                {'answer': 'SORT BY [field1] DESC', 'is_correct': False, 'feedback': 'Incorrect. ORDER BY should be used, not SORT BY.'},
                {'answer': 'ORDER BY [field1]', 'is_correct': False, 'feedback': 'Incorrect. This would sort [field1] in ascending order by default, not descending order.'},
                {'answer': 'ORDER BY [field1] DESC', 'is_correct': True, 'feedback': 'Correct.'},
            ]
        },
        {
            'question_num': 7,
            'question_text': 'Consider the following query: SELECT s.name, s.age FROM students AS s WHERE s.age > 18; What will this query do?',
            'answer_choices': [
                {'answer': 'Select all columns from the students table', 'is_correct': False, 'feedback': 'Incorrect. This only includes students over 18, and the students table may have more than the two columns selected in the query.'},
                {'answer': 'Select the name and age columns for rows where age is 18 or less', 'is_correct': False, 'feedback': 'Incorrect. The query selects students with an age greater than 18.'},
                {'answer': 'Select the name and age columns for rows where age is greater than 18', 'is_correct': True, 'feedback': 'Correct.'},
                {'answer': 'Select all rows sorted by age in descending order', 'is_correct': False, 'feedback': 'Incorrect. The query has no ORDER BY clause, so it doesn’t sort the rows.'},
            ]
        },
        {
            'question_num': 8,
            'question_text': 'Which keyword in a WHERE clause can be used to check if a column’s value matches any one of several specified values?',
            'answer_choices': [
                {'answer': 'IN', 'is_correct': True, 'feedback': 'Correct.'},
                {'answer': 'LIKE', 'is_correct': False, 'feedback': 'Incorrect. LIKE is used to check a column’s value (case insensitive) against one string of characters, not a list of specified values.'},
                {'answer': 'AS', 'is_correct': False, 'feedback': 'Incorrect. AS is used to assign aliases to columns and tables, not compare values.'},
                {'answer': 'None of the above', 'is_correct': False, 'feedback': 'Incorrect. IN matches the keyword described in the question.'},
            ]
        },
        {
            'question_num': 9,
            'question_text': 'If you want to select all columns from a table named employees, which of the following is the correct syntax?',
            'answer_choices': [
                {'answer': 'SELECT columns FROM employees;', 'is_correct': False, 'feedback': 'Incorrect. The field named columns is not a supported keyword in SQL and does not indicate all columns.'},
                {'answer': 'SELECT * FROM employees;', 'is_correct': True, 'feedback': 'Correct.'},
                {'answer': 'SELECT ALL FROM Employees;', 'is_correct': False, 'feedback': 'Incorrect. The keyword ALL doesn’t indicate all columns.'},
                {'answer': 'SELECT employees FROM employees;', 'is_correct': False, 'feedback': 'Incorrect. The table name employees cannot be used to indicate all columns.'},
            ]
        },
        {
            'question_num': 10,
            'question_text': 'Which of the following queries will select rows from the products table where price is greater than 100 and less than 500?',
            'answer_choices': [
                {'answer': 'SELECT * FROM products AS p WHERE p.price = 100 OR p.price = 500;', 'is_correct': False, 'feedback': 'Incorrect. This query would select rows where price is equal to either 100 or 500.'},
                {'answer': 'SELECT * FROM products AS p WHERE p.price < 100 OR p.price > 500;', 'is_correct': False, 'feedback': 'Incorrect. This query would select rows where price is less than 100 or greater than 500.'},
                {'answer': 'SELECT * FROM products AS p WHERE p.price >100 AND <500;', 'is_correct': False, 'feedback': 'Incorrect. This syntax is wrong; p.price would need to be written again after the AND operator, like in option d.'},
                {'answer': 'SELECT * FROM products AS p WHERE p.price > 100 AND p.price < 500;', 'is_correct': True, 'feedback': 'Correct.'},
            ]
        }
    ]
}