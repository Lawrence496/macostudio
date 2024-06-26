from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from movies.models import Movies, Reviews, MovieInteraction, UserGenrePreference, Category
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime
import re 
from django.db.models import Count, Q
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .forms import GenreForm

# Create your views here.
def signup(request):
    if request.method == "POST":
        username = request.POST["form-username"]
        email = request.POST["email"]
        password = request.POST["form-password"]
        repeat_password = request.POST['repeat-password']
        
        if password == repeat_password:
            try:
                validate_password(password)
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'The username already exists')
                    return redirect('signup')
                else:
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'The email already exists')
                        return redirect('signup')
                    else:
                        user = User.objects.create_user(username=username, email=email, password=password)
                        user.save()
                        login(request, user)
                        messages.success(request, 'Successfully created an account')
                        return redirect('genre_selection')
            except ValidationError as e:
                error_message = ' '.join(e.messages)
                messages.error(request, error_message)
                return redirect('signup')
        else:
            messages.error(request, 'The passwords do not match')
            return redirect('signup')
    else:
        return render(request, 'accounts/signup.html')
    
def signin(request):
    if request.method == "POST":
        email = request.POST['signin_email']
        password = request.POST['psw']
        
        user =  authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in')
            return redirect('index')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('signin')
    else:
        return render(request, 'accounts/signin.html')
    
def signout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Successfully logged out')
        return redirect('index')
    return redirect('index')


    
@login_required
def profile(request):
    user = request.user
    
    total_reviews = Reviews.objects.filter(user=user).count()
    
    user_reviews = Reviews.objects.filter(user=user).order_by('-created_at')[:6]
    
    total_movies_watched = Movies.objects.filter(reviews__user=user).distinct().count()
    
    date_joined = localtime(user.date_joined)

    # Find user's most watched genres
    favorite_genres = Movies.objects.filter(reviews__user=user)\
        .values('movie_categories')\
        .annotate(genre_count=Count('movie_categories'))\
        .order_by('-genre_count')

    # Get the top genres the user watched
    top_genres = [genre['movie_categories'] for genre in favorite_genres[:3]]  # Top 3 genres

    # Fetch highest-rated movies in those favorite genres
    genre_recommended_movies = Movies.objects.filter(movie_categories__in=top_genres)\
        .order_by('-rating')[:10]  # Top 10 highest-rated in those genres

    # Fetch general highest-rated movies (optional to combine with genre-specific recommendations)
    highest_rated_movies = Movies.objects.exclude(movie_categories__in=top_genres)\
        .order_by('-rating')[:10]

    recommended_movies = list(genre_recommended_movies) + list(highest_rated_movies)
    
    # Remove duplicates (if any) from combined list
    recommended_movies = list(dict.fromkeys(recommended_movies))
    
    total_movies_watched = MovieInteraction.objects.filter(user=user, action='watched').values('movie').distinct().count()
    
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_profile':
            username = request.POST.get('username')
            email = request.POST.get('email')
            firstname = request.POST.get('first_name')
            lastname = request.POST.get('last_name')
            
            if username != user.username:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'The username is already taken.')
                    return redirect('profile')
                
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'This email is already taken.')
                    return redirect('profile')
                
            if not (username or email or firstname or lastname):
                messages.error(request, 'At least one field must be filled to update profile')
                return redirect('profile')
            
            user = request.user
            
            if user.username != username:
                user.username = username
                
            if email:
                user.email = email
            
            if firstname:
                user.first_name = firstname
            
            if lastname:
                user.last_name = lastname
                
            user.save()
            messages.success(request, 'Profile details sucessfully changed')
            return redirect('profile')

        elif action == 'change_password':
            old_password = request.POST.get('oldpass')
            new_password = request.POST.get('newpass')
            confirm_password = request.POST.get('confirmpass')

            # Check if the old password is correct
            if request.user.check_password(old_password):
                if new_password == confirm_password:
                    try:
                        # Update user password
                        validate_password(new_password, user)
                        request.user.set_password(new_password)
                        request.user.save()
                        
                        messages.success(request, 'Password successfully changed.')
                        return redirect('signin')  # Or redirect to 'signin' if you want to log them out
                    except ValidationError as e:
                        # Collect error messages and display them to the user
                        error_messages = ' '.join(e.messages)
                        messages.error(request, error_messages)
                        return redirect('profile')
                else:
                    messages.error(request, 'The new passwords do not match.')
                    return redirect('profile')
            else:
                messages.error(request, 'Incorrect old password.')
                return redirect('profile')
                
        
    data = {
        'total_movies_watched': total_movies_watched,
        'recommended_movies': recommended_movies,
        'total_reviews': total_reviews,
        'user_review': user_reviews,
        'total_movies_watched': total_movies_watched,
        'date_joined': date_joined,
    }
    
    return render(request, 'accounts/dashboard.html', data)
                
def check_username(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        if username:
            if User.objects.filter(username=username).exists():
                return JsonResponse({'exists': True})
            else:
                return JsonResponse({'exists': False})
    return JsonResponse({}, status=400)

def genre_selection(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        
        print("POST data:", request.POST)
        print("Form errors:", form.errors)
        
        if form.is_valid():
            selected_genre_ids = request.POST.getlist('genres')  # Get list of selected genre IDs
            selected_genres = Category.objects.filter(id__in=selected_genre_ids)  # Query selected genres
            
            preference, created = UserGenrePreference.objects.get_or_create(user=request.user)
            
            preference.genres.clear()
            preference.genres.add(*selected_genres)
            messages.success(request, 'Your favorite genres have been saved!')
            return redirect('index')
        else:
            print("Form is not valid")
    else:
        form = GenreForm()

    return render(request, 'accounts/genre_selection.html', {'form': form, 'user': request.user})