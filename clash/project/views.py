from django.shortcuts import render, redirect, HttpResponse
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Register, Response, Questions
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import re
import random
import datetime
from django.utils import timezone
from collections import Counter
#from django.views.decorators.cache import cache_control

app_name = 'project'
number_of_questions = 12


def checkspin(request):
    flag=request.GET.get('flag')
    getuser = Register.objects.get(user=request.user)
    getuser.spincount-=1
    getuser.flag = int(flag)
    flag=int(flag)
    if int(flag)==2 and getuser.freezetimestart==None:
        getuser.freezetimestart=timezone.now()
    getuser.spin_wheel=True
    getuser.save()
    '''life=["congrats u won chance to reattempt a question",
          "Unlucky! -5 from ur total",
          "congrats ur time is freezed for current question" ,
          "Unlucky! -8 + 4 for next 3 questions",
          "congrats you have no negative marks for next 3 questions",
          "Unlucky! u cannot spin here after",
          "congrats you have +16-10 marking scmeme fpr current question"]'''
    data={'flag':int(flag),'useflag':getuser.flag,'flashblind':getuser.flashblind}
    print(flag)
    return JsonResponse(data)



def check(request):
    username_lst = []
    user_list = User.objects.values()
    for user in user_list:
        username_lst.append(user['username'])
    data = {'is_taken': False}
    if request.GET.get('name') in username_lst:
        data = {'is_taken': True}
    return JsonResponse(data)


def signup(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('success')
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']
        phone = data['phone']
        password = data['password']
        conf_pass = data['confirm_password']
        level = data['level']
        language = data['language']
        regexusername = "^[[A-Z]|[a-z]][[A-Z]|[a-z]|\\d|[_]]{7,29}$"
        regexemail = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
        if not re.search(regexusername, username):
            return render(request, 'task2part2temp/signup.html', {'msg': ["Username is Not Valid"]})
        if not re.search(regexemail, email):
            return render(request, 'task2part2temp/signup.html', {'msg': ["Email ID is not Valid"]})
        if not str(firstname).isalpha():
            return render(request, 'task2part2temp/signup.html', {'msg': ["First Name is not Valid"]})
        if not str(lastname).isalpha():
            return render(request, 'task2part2temp/signup.html', {'msg': ["Last Name is not Valid"]})
        if not str(phone).isnumeric() and len(phone) == 10 and phone < 59999999999:
            return render(request, 'task2part2temp/signup.html', {'msg': ["Invalid Phone Number is Entered"]})
        if password != conf_pass:
            return render(request, 'task2part2temp/signup.html', {'msg': ["Passwords Don't match"]})
        try:
            ouruser = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, email=email,
                                               password=password)
            newuser = Register(user=ouruser, phone=phone, level=level, language=language)
            ouruser.save()
            newuser.status = False
            newuser.save()
            lst = []
            if newuser.level=='fe':
                cp=random.randint(5,7)
                newuser.checkpoint=cp
            elif newuser.level=='se':
                cp=random.randint(8,10)
                newuser.checkpoint=cp
            else:
                cp=random.randint(9,12)
                newuser.checkpoint=cp
            for i in range(0, 10):
                while True:
                    questionNo = random.randint(1, number_of_questions)
                    if questionNo not in lst:
                        break
                lst.append(questionNo)
            newuser.quelist = json.dumps(lst)
            newuser.quefulllist = json.dumps(lst)
            auth.login(request, ouruser)
            newuser.save()
            return HttpResponseRedirect(reverse('success'))
        except:
            return render(request, 'task2part2temp/signup.html', {'msg': ["User already exists"]})
    return render(request, 'task2part2temp/signup.html')


# @cache_control(no_cache=True,must_revalidate=True,no_store=True)


def signin(request):
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        try:
            getuser = Register.objects.get(user=user)
            if user and getuser.status == True:
                login(request, user)
                getuser.status = False
                getuser.save()
                return HttpResponseRedirect(reverse('success'))
            return render(request, 'task2part2temp/signin.html', {'msg': ['Invalid Credentials!'], 'user': getuser})
        except:
            return render(request, 'task2part2temp/signin.html', {'msg': ['Invalid Credentials!']})
    return render(request, 'task2part2temp/signin.html')


def recfun(getuser):
    getuser.flag = -1
    getuser.spin_wheel = False
    getuser.save()




# @cache_control(no_cache=True,must_revalidate=True,no_store=True)

def success(request):
    try:
        msg3=""
        getuser = Register.objects.get(user=request.user)
        time_diff = timezone.now() - getuser.user.last_login
        minute=getuser.extra_time//60
        second=getuser.extra_time%60
        time_rem = datetime.timedelta(minutes=28+minute,seconds=second) - time_diff
        total_seconds = time_rem.total_seconds()
        getuser.time_rem = int(total_seconds)
        getuser.save()
        time=[getuser.time_rem // 60,getuser.time_rem%60]
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        if getuser.progress>=100:
            getuser.freezebar=True
        if total_seconds <= 0:
            return redirect('logout')
        msg2 = "TIME REMAINING  = " + str(minutes) + ":" + str(seconds)
        lst = json.loads(getuser.quelist)
        flst=json.loads(getuser.queflist)
        if request.method == 'GET' and getuser.user.is_authenticated:
            pass
        if (getuser.total_score%getuser.checkpoint==0) and getuser.spin_wheel==True:
            allow=False
            getuser.getassured=False
            if getuser.spincount>=0:
                allow=True
            if allow:
                if getuser.flag==0 and request.method=='POST':
                    msg3="congrats u won chance to reattempt a question"
                    quenumber=request.POST['quenum']                #take question number!
                    lst.append(flst[int(quenumber)-1])              #152
                    getuser.marks=6                                 #43
                    recfun(getuser)
                elif getuser.flag==1:
                    msg3="Unlucky! -5 from ur total"
                    getuser.total_score-=5
                    recfun(getuser)
                elif getuser.flag == 2:
                    msg3 = "congrats ur time is freezed for current question"
                    recfun(getuser)
                elif getuser.flag == 3:
                    msg3 = "Unlucky! -8 + 4 for next 3 questions"
                    getuser.marks=3
                    getuser.flashblind=2
                    recfun(getuser)
                elif getuser.flag == 4:
                    msg3 = "congrats you have no negative marks for next 3 questions"
                    getuser.marks=4
                    getuser.flashblind=2
                    recfun(getuser)
                elif getuser.flag == 5:
                    msg3 = "Unlucky! u cannot spin here after"
                    getuser.checkpoint=-1
                    recfun(getuser)
                elif getuser.flag == 6:
                    msg3 = "congrats you have +16-10 marking scmeme fpr current question"
                    getuser.marks = 5
                    recfun(getuser)
        if getuser.getassured==True:
            pre_question = Questions.objects.get(pk=lst[-1])
            user_input1 = request.POST['attempt1']
            user_input2 = request.POST['attempt2']
            print(user_input1, user_input2)
            getuser.freezebar=False
            if pre_question.correct_answer == user_input1:
                if pre_question.correct_answer == user_input1:
                    score = 10
                    getuser.marks = 1
            else:
                if pre_question.correct_answer == user_input2:
                    score = +2
                    getuser.marks = 1
                else :
                    score = -14
                    getuser.marks = 2


            getuser.getassured=False
            getuser.progress=0
            respo = Response(question=pre_question, user=getuser.user, selected_answer=user_input1, score=score)
            respo.save()
            getuser.total_score += respo.score
            flst.append(lst[-1])
            lst.pop()
            getuser.save()

        if request.method == 'POST' and getuser.flag!=0 and getuser.getassured==False:
            if request.POST.get('submit') == str(lst[-1]):
                user_input = request.POST['user_ans']
                pre_question = Questions.objects.get(pk=lst[-1])
                if getuser.freezetimestart!=None:
                    sec = timezone.now() - getuser.freezetimestart
                    getuser.extra_time += sec.total_seconds() + 12
                    getuser.freezetimestart = None
                if getuser.marks == 1:
                    if pre_question.correct_answer == user_input:
                        score = 4
                        getuser.marks=1
                        if getuser.progress < 100 and getuser.freezebar == False:
                            getuser.progress+=20
                    else:
                        score = -2
                        getuser.marks=2
                        if getuser.progress>0 and getuser.freezebar==False:
                            getuser.progress-=30
                elif getuser.marks==2:
                    if pre_question.correct_answer == user_input:
                        score = 2
                        getuser.marks = 1
                        if getuser.progress < 100 and getuser.freezebar == False:
                            getuser.progress += 20
                    else:
                        score = -1
                        getuser.marks = 2
                        if getuser.progress > 0 and getuser.freezebar == False:
                            getuser.progress -= 30
                elif getuser.marks==3:
                    if pre_question.correct_answer == user_input:
                        score = +4
                        if getuser.flashblind>0:
                            getuser.flashblind-=1
                            getuser.marks=3
                        else:
                            getuser.marks=1
                    else:
                        score = -8
                        if getuser.flashblind>0:
                            getuser.flashblind-=1
                            getuser.marks=3
                        else:
                            getuser.marks = 2
                elif getuser.marks == 4:
                    if pre_question.correct_answer == user_input:
                        score = +4
                        if getuser.flashblind>0:
                            getuser.flashblind-=1
                            getuser.marks=4
                        else:
                            getuser.marks=1
                    else:
                        score = 0
                        if getuser.flashblind>0:
                            getuser.flashblind-=1
                            getuser.marks=4
                        else:
                            getuser.marks = 2
                elif getuser.marks == 5:
                    if pre_question.correct_answer == user_input:
                        score = +16
                        getuser.marks = 1
                    else:
                        score = -10
                        getuser.marks = 2
                elif getuser.marks == 6:
                    if pre_question.correct_answer == user_input:
                        score = +5
                        getuser.marks = 1
                    else:
                        score = -5
                        getuser.marks = 2

                respo = Response(question=pre_question, user=getuser.user, selected_answer=user_input, score=score)
                respo.save()
                getuser.total_score += respo.score
                flst.append(lst[-1])
                lst.pop()
                if getuser.progress>100:
                    getuser.progress=100
                if getuser.progress<0:
                    getuser.progress=0
                getuser.save()

        if len(lst) == 0:
            return HttpResponseRedirect(reverse('logout'))
        question = Questions.objects.get(pk=lst[-1])
        getuser.quelist = json.dumps(lst)
        getuser.queflist=json.dumps(flst)
        getuser.save()
        return render(request, 'task2part2temp/question.html', {'user': getuser, 'question': question, 'timemin': [time[0]],'timesec':[time[1]]})
    except Exception as e:
        return render(request, 'task2part2temp/signin.html', {'msg': [f'Login First ..!! {e}']})
    #return render(request, 'task2part2temp/question.html', {'user': getuser, 'question': question, 'timemin': [time[0]],'timesec':[time[1]]})
# @cache_control(no_cache=True,must_revalidate=True,no_store=True)


def userlogout(request):
    try:
        getuser = Register.objects.get(user=request.user)
        getuser.logouttime = timezone.now()
        getuser.extra_time=0
        getuser.save()
        logout(request)
        return render(request, 'task2part2temp/result.html', {'user': getuser, 'msg': ['Quiz Finished']})
    except:
        return render(request, 'task2part2temp/signup.html', {'msg': ['You need To Login/Register First :)']})


def getassured(request):
    getuser = Register.objects.get(user=request.user)
    lst = json.loads(getuser.quelist)
    question = Questions.objects.get(pk=lst[-1])
    getuser.getassured=True
    getuser.save()
    return render(request, 'task2part2temp/question2.html' ,{'user': getuser, 'question': question})


def emglogin(request):
    if request.method == 'POST':
        data=request.POST
        username = data['username']
        admin_username = data['admin_username']
        admin_password = data['admin_password']
        extra_time=data['extra_time']
        # user = authenticate(request, username=username)
        super_user = authenticate(request, username=admin_username, password=admin_password)
        try:
            getuser = User.objects.get(username=username)
            if getuser and super_user:
                setuser=Register.objects.get(user=getuser)
                #print(len(json.loads(setuser.quelist)))
                if len(json.loads(setuser.quelist))==1:
                    return render(request, 'task2part2temp/emglogin.html', {'msg': ['The Player has Completed All Question..!!']})
                setuser.status = True
                setuser.extra_time += extra_time
                setuser.save()
                return render(request, 'task2part2temp/emglogin.html', {'msg': ['Time added successfully!']})
            return render(request, 'task2part2temp/emglogin.html', {'msg': ['Invalid Credentials!']})
        except:
            return render(request, 'task2part2temp/emglogin.html', {'msg': ['Invalid']})
    return render(request, 'task2part2temp/emglogin.html')