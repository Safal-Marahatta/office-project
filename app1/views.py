from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse, HttpResponseNotFound,HttpResponseRedirect
from .forms import loginform,RegisterForm,InputForm
# from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from .models import Task,repeat
from django.contrib.auth.models import User
from django.core.serializers import serialize
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,timedelta
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.
@never_cache
def login_page(request):
    if request.method == 'POST':
        form = loginform(request.POST)
        if form.is_valid():
            print('valid form')
            username= form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username,password=password)#If the credentials are valid, the function returns a user object representing the authenticated user. 
                                                                              #If the credentials are invalid, the function returns None.
            
           ## eg. this gives the username of the user:::print(user.get_username())
            
            if user is not None:
                if user.is_active:
                    login(request,user)#yesle k garxa vane:
    #                            -->aauta session banaidinxa ani tesma session data haru store gardinxa.tyo session id chai cookie ko rup ma send gardinxa browser lai.
    #                            -->aba tyo data haru request.session.get('_auth_user_id',default='default') yesto garera herna milxa.
                    messages.success(request, 'You have successfully logged in.')
                    return redirect('home')
                else:
                    return render(request,'app1/errorlogin.html',{'form':form})

            else:
                return render(request,'app1/errorlogin.html',{'form':form})
    else:
        form = loginform()
    return render(request, 'app1/login.html', {'form': form})


# @csrf_exempt
@never_cache
def register(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            password=form.cleaned_data['password']
            username=form.cleaned_data['username']
            first_name=form.cleaned_data['firstname']
            last_name=form.cleaned_data['lastname']
            email=form.cleaned_data['email']

            try:
                user = User.objects.create_user(username=username,password= password)#At this point, user is a User object that has already been saved to the database.
                #if you want to change other fields.
                    #>>> user.last_name = "Lennon"
                    #>>> user.save()
                user.first_name=first_name
                user.last_name=last_name
                user.email=email
                user.is_active=False # User is not active until approved by admin
                user.save()
                send_mail(
                    'New Account Request',#subject
                    'Dear Admin,\nYou have received a new request to approve MyTask account of following user:\n'+'Name:'+first_name+' '+last_name+'\ncompany:IES\n'+'Email:'+email+'\nPlease approve it from admin account.\n'+'MyTask',
                    'mytaskowner@gmail.com',
                    ['anup.khanal@ies.com.np']
                )
                return render(request,"app1/register_pending.html")
            except Exception as e:
                return HttpResponse('An error occurred while registering the user: {}'.format(str(e)))
    
    
    else:
        form=RegisterForm()
    
    return render(request,"app1/register.html",{'form':form})


def logout_page(request):
    logout(request)
    return redirect('login')

@never_cache
def home(request):
    if request.method=="GET":
        current_user = request.user# Access the current logged-in user
        fname=current_user.first_name
        lname=current_user.last_name
        expired_list=[]
        today_list=[]
        tomorrow_list=[]
        thisweek_list=[]
        thismonth_list=[]
        thisyear_list=[]
        current_date = datetime.now().date()#current date
        current_month = current_date.month

        # Get all instances of the Postponed model
        all_repeat_data = repeat.objects.filter(user=current_user)
        sorted_tasks = Task.objects.filter(user=current_user).order_by('deadline')#database ma store vako date nikaleko
        for task in sorted_tasks:
            #print(task.description, task.deadline)
            if current_date>task.deadline:
                print("deadline finished")
                expired_list.append(task)

            elif current_date==task.deadline:
                print("deadline today")
                today_list.append(task)
            elif task.deadline == current_date + timedelta(days=1):
                print("deadline tommorrow")
                tomorrow_list.append(task)
            elif task.deadline <= current_date + timedelta(days=6):
                print("deadline this week")
                days_rem=task.deadline-current_date
                due_days=days_rem.days
                thisweek_list.append([task,due_days])
            elif task.deadline.month == current_month:
                due_days = (task.deadline - current_date).days
                thismonth_list.append([task, due_days])
            else:
                print("deadline more than a year")
                days_rem=task.deadline-current_date
                due_days=days_rem.days
                thisyear_list.append([task,due_days])    
        form=InputForm()
        
        return render(request,"app1/home_page.html",{'form':form,'repeat':all_repeat_data,'expired':expired_list,"today":today_list,"tommorrow":tomorrow_list,"this_week":thisweek_list,"this_month":thismonth_list,"this_year":thisyear_list,"firstname":fname,"lastname":lname}) 
    
    if request.method=="POST":#yo chai tyo naya task user le halda teslai handle garne
        form=InputForm(request.POST)
        if form.is_valid():
            current_user=request.user
            description=form.cleaned_data['description']
            deadline=form.cleaned_data['deadline']            
            try:
                task =Task.objects.create(user=current_user,description=description,deadline=deadline)
                task.save()
                return redirect('home')#Redirect to the home
            except Exception as e:
                return HttpResponse('An error occurred while saving the task {}'.format(str(e)))
        else:
            return HttpResponse("Invalid form")
        



        
        

      
@api_view(['post'])
def complete_task(request):
    if request.method == "POST":
        # Read the JSON data from the request
        current_user=request.user
        data = request.data
        # Perform any required processing on the data
        row_id = data.get('rowId')
        if row_id.endswith("b"):
            print("end with b")
            new_rowid=row_id[:-1]
            try:
                objrepeat=repeat.objects.get(user=current_user,id=new_rowid)
            except Task.DoesNotExist:
                return Response({'message':"No task found"},status=500)
            objrepeat.delete()
        else:
            try:
                obj=Task.objects.get(user=current_user,id=row_id)
            except Task.DoesNotExist:
                return Response({'message':"No task found"},status=500)

            obj.delete()
            print(row_id)
            
        # Return a response
        return Response({'message': 'Task completed'}, status=200)

        
@api_view(['post'])
def postpone_task(request):
    if request.method == "POST":
        # Read the JSON data from the request
        data = request.data
        current_user=request.user

        row_id=data.get('rowId')    
        new_deadline=data.get('new_deadline')
        print(row_id)
        print("the new deadline is")
        print(new_deadline)

        if row_id.endswith("b"):
            print("end with b")
            new_rowid=row_id[:-1]
            try:
                objrepeat=repeat.objects.get(user=current_user,id=new_rowid)
                new_task_obj=Task(user=current_user,description=objrepeat.descripti,deadline=new_deadline)
            except:
                return Response({'message':"something wrong when retreiving data from database"})
            new_task_obj.save()
            objrepeat.delete()
        else:
            print("does not end with b")
            try:
                obj=Task.objects.get(user=current_user,id=row_id)
            except:
                return Response({'message':"an error occured when retreiving from database"})
            obj.deadline=new_deadline
            obj.save()
        
        return Response({'message':'updated'},status=200)
    

@api_view(['post'])
def repeat_task(request):
    if request.method == "POST":
        current_user=request.user
        # Read the JSON data from the request
        data = request.data

        row_id=data.get('rowId')  

        # current_date = datetime.now().date()#current date 
         
        try:
            obj=Task.objects.get(user=current_user,id=row_id)
            descrip=obj.description
            obj.delete()
            new_postponed_record = repeat(user=current_user,descripti=descrip)
            new_postponed_record.save()
        except:
            return Response({'message':'an error occured'},status=200)
            
        return Response({'message':'repeated'},status=200)




        



