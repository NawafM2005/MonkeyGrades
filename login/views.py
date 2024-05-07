from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Course, Grade
from .calculator import Calculator


# Create your views here.
def home(request):
    return render(request, 'index.html')

def signup(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username = username):
            error_message = 'Username already exists'
        elif User.objects.filter(email = email):
            error_message = 'Email already exists'
        elif len(username) > 10:
            error_message = 'Username too long. Must be less than 10 characters.'
        elif pass1 != pass2:
            error_message = 'Passwords do not match'
        elif not username.isalnum():
            error_message = 'Username must be alphanumeric'
        else:
            my_user = User.objects.create_user(username, email, pass1)
            my_user.first_name = fname
            my_user.last_name = lname
            my_user.is_active = True
            my_user.save()
            return render(request, 'signin.html', {'created_message': 'Your Account has been Created!'})

    return render(request, 'signup.html', {'error_message': error_message})

def signin(request):
    
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')

        user = authenticate(username=username, password=pass1)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = "Bad credentials"

    return render(request, 'signin.html', {'error_message': error_message})

def signout(request):
    logout(request)
    return redirect('home')

def simple(request):
    return render(request, 'simple.html')

def dashboard(request):
    if request.method == 'POST':
        # Handle form submissions to add grades or delete data
        
        if 'delete_data' in request.POST:
            assignment = request.POST.get('assignment')
            grade_value = request.POST.get('grade')
            weight = request.POST.get('weight')
            course_name = request.POST.get('course')

            try:
                # Get the course object
                course = Course.objects.get(name=course_name)
                # Query all grades for the given course name
                grades = Grade.objects.filter(course = course, assignment=assignment, grade=grade_value, weight=weight)

                # Delete all matching grades
                for grade in grades:
                    grade.delete()
                    break
            except Exception:
                messages.error(request, 'Something went wrong. Try Again!')
                return redirect('dashboard')


            return redirect('dashboard')
        
        assignment = request.POST.get('assignment')
        grade = request.POST.get('grade')
        weight = request.POST.get('weight')
        course = request.POST.get('course')

        try:
            float(grade)
            float(weight)
        except Exception:
            messages.error(request, 'Grade and Weight must be Integer Numbers!')
            return redirect('dashboard')

        if int(grade) < 0 or int(weight) < 0:
            messages.error(request, 'Values Cannot be Negative!')
            return redirect('dashboard')
        
        try:
            # Find the course belonging to the logged-in user
            course = Course.objects.get(user=request.user, name=course)
            # Create a new grade associated with the course and the logged-in user
            Grade.objects.create(course=course, assignment=assignment, grade=grade, weight=weight)
        except Exception:
            messages.error(request, 'Something went wrong. Please check Inputs and Try Again!')
            return redirect('dashboard')

        return redirect('dashboard')
    
    # Retrieve all courses belonging to the logged-in user
    courses = Course.objects.filter(user=request.user)

    # Create a dictionary to store courses and their average grades
    course_data = {}

    overall_avg = []

    # Retrieve grades associated with each course and store them in a list
    for course in courses:
        grades = Grade.objects.filter(course=course)
        grades_list = [str(grade.grade) for grade in grades]  # Assuming grades are stored as strings
        weights_list = [str(grade.weight) for grade in grades]  # Assuming weights are stored as strings

        # Create an instance of the Calculator class
        calculator = Calculator(grades_list, weights_list)

        # Calculate the average grade
        average_grade = calculator.avg_grade()

        if average_grade != 0:
            overall_avg.append(average_grade)

        # Add average grade to the course data dictionary
        course_data[course] = {'grades': grades, 'average_grade': average_grade}

    # Pass courses and their associated data to the template
    user_first_name = request.user.first_name

    # Retrieve messages for the user
    messages_to_display = messages.get_messages(request)

    try:
        avg = round(sum(overall_avg)/len(overall_avg), 2)
    except Exception:
        avg = 0
        

    return render(request, 'dashboard.html', {'course_data': course_data, 'fname': user_first_name, 'avg': avg, 
                                              'error_message': messages_to_display})

def remove_course(request):
    if request.method == 'POST':
        try:
            course = request.POST.get('course')
            Course.objects.get(user = request.user, name = course).delete()
            return redirect('dashboard')
        except Exception:
            messages.error(request, 'Course does not Exist')
            return redirect('dashboard')


def add_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('course')
        
        # Check if the course with the same name exists for the user
        existing_course = Course.objects.filter(user=request.user, name=course_name).exists()
        if existing_course:
            messages.error(request, 'Course with the same name already exists.')
            return redirect('dashboard')
        
        # Create a new course for the logged-in user
        Course.objects.create(user=request.user, name=course_name)
        return redirect('dashboard')
    