from django.shortcuts import render, reverse, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.template import loader
from django.views import generic
from .models import Choice, Question
from .forms import NameForm


def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')

    else:
        form = NameForm()

    return render(request, 'polls/name.html', {'form': form})


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/polls_index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


class IndexView(generic.ListView):
    template_name = 'polls/polls_index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/polls_detail.html', {'question': question})


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/polls_detail.html'


def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/polls_result.html', {'question': question})


class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/polls_result.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/polls_detail.html', {
            'question': question,
            'error_message': "你还未做出选择",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))
