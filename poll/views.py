from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from .forms import EditPollForm
from .forms import CreatePollForm
from .models import Poll
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import auth
from django.http import HttpResponseRedirect

def home(request):
    polls = Poll.objects.all()
    context = {
        'polls' : polls
    }
    return render(request, 'poll/home.html', context)

def create(request):
    polls = Poll.objects.all()
    if not request.user.is_authenticated:
        return render(request, 'poll/login_error.html')
    else:
        if request.method == 'POST':
            form = CreatePollForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = CreatePollForm()
        form = CreatePollForm()
        context = {
            'form' : form,
            'polls' : polls
        }
        return render(request, 'poll/create.html', context)

def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    context = {
        'poll' : poll
    }
    return render(request, 'poll/results.html', context)

def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':
        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count +=1
        elif selected_option == 'option2':
            poll.option_two_count +=1
        elif selected_option == 'option3':
            poll.option_three_count +=1
        else:
            return HttpResponse(400, 'Invalid Form')

        poll.save()

        return redirect('results', poll.id)
    context = {
        'poll' : poll
    }
    return render(request, 'poll/vote.html', context)

def edit(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
        context = {
        'poll' : poll
        }
        if request.method == 'POST':
            #poll = EditPollForm(request.POST)
            poll.question = request.POST.get('question')
            poll.option_one = request.POST.get('option_one')
            poll.option_two = request.POST.get('option_two')
            poll.option_three = request.POST.get('option_three')
            poll.option_one_count = 0
            poll.option_two_count = 0
            poll.option_three_count = 0
            #if poll.is_valid():
            poll.save()
            return render(request, 'poll/home.html',context)
        else: 
            return render(request, 'poll/edit.html', context)
            
    except Poll.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")
        
def delete(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    poll.delete()
    return render(request, 'poll/delete.html')