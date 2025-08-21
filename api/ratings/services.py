from .models import CourseRating, CourseRatingEntry

class RatingsService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RatingsService, cls).__new__(cls)
        return cls._instance
    

    def create_entry(self, rating_id, category_id, score):
        entry, created = CourseRatingEntry.objects.update_or_create(
            rating_id=rating_id,
            category_id=category_id, 
            defaults={'score': score})
        
        return entry

    def create_rating(self, course_id, learner_id, comments):
        rating, created = CourseRating.objects.update_or_create(
            course_id=course_id, 
            learner_id=learner_id, 
            defaults={'comments': comments})
        
        return rating

    def get_ratings(self, course_id):
        return CourseRating.objects.filter(course_id=course_id).prefetch_related('courseratingentry_set')