from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from chatty_back.chatty_users import models as chattyuser_models
from chatty_back.partners import models as partner_models


@python_2_unicode_compatible
class TimeStampedModel(models.Model):

    """ Basic Model """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Question(TimeStampedModel):

    """ Single question Model """

    message = models.TextField()
    creator = models.ForeignKey(
        chattyuser_models.ChattyUser, on_delete=models.CASCADE, related_name="questions", null=True
        )

    def __str__(self):
        return '{} - creator: {}'.format(self.message, self.creator.name)


@python_2_unicode_compatible
class Question_set(TimeStampedModel):

    """ Question set list table """

    question_list = models.TextField()

    def __str__(self):
        return self.question_list

    # 글자 질문 list
    @property
    def questions(self):

        questions = []

        question_list = self.question_list.split(',')

        for question_id in question_list:

            question = Question.objects.get(id=question_id)
            
            questions.append(question)

        return questions

    
@python_2_unicode_compatible
class Single_diary(TimeStampedModel):

    """ Single diary table """

    creator = models.ForeignKey(chattyuser_models.ChattyUser, on_delete=models.CASCADE, related_name="diaries")
    question_set = models.ForeignKey(Question_set, on_delete=models.CASCADE)
    state = models.CharField(max_length=80, null=True)
    partner = models.ForeignKey(
        partner_models.Partner, on_delete=models.CASCADE, related_name="diaries", null=True)


    class Meta:
        ordering = ['-created_at']

    @property
    def questions(self):
        return self.question_set.questions

    @property
    def answer_count(self):
        return self.answers.all().count()
    
    @property
    def current_question(self):

        index = self.answer_count

        question_set = self.question_set.questions 
        
        try:
            question = question_set[index]

            return question

        except:
            return None

    @property
    def first_question(self):
        return self.questions[0]


    def __str__(self):
        return 'creator: {} - id: {}'.format (self.creator.name, self.id)


@python_2_unicode_compatible
class User_answer(TimeStampedModel):

    """ User answer Model """

    diary = models.ForeignKey(Single_diary, on_delete=models.CASCADE, related_name='answers')
    creator = models.ForeignKey(chattyuser_models.ChattyUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    answer = models.TextField()


    def __str__(self):
        return self.answer

