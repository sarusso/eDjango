

import time
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
#from common import log_user_activity, timezonize, username_hash, format_exception, os_shell
from django.contrib.auth import update_session_auth_hash
import uuid
import json
import socket
import os

from edjango.base_app.models import LoginToken
from edjango.common.utils import send_email, format_exception, log_user_activity, random_username

from edjango.settings import EDJANGO_PROJECT_NAME, EDJANGO_PUBLIC_HTTP_HOST 

# Setup logging
import logging
logger = logging.getLogger(__name__)

from edjango.common.exceptions import ErrorMessage

# This is a support array used to prevent double click problems
ONGOING_SIGNUPS = {}

#=========================
#  Decorators
#=========================

def private_view(func):
    def func_wrapper(request):
        if request.user.is_authenticated():
            log_user_activity("DEBUG", "Called", request)
            try:
                return func(request)
            except Exception as e:
                if isinstance(e, ErrorMessage):
                    error_text = str(e)
                else:
                    error_text = 'something went wrong'
                    logger.error(format_exception(e))
                data = {'user': request.user,
                        'title': 'Error',
                        'error' : 'Error: "{}"'.format(error_text)}
            return render(request, 'error.html', {'data': data})
        
        else:
            log_user_activity("DEBUG", "Redirecting to login since not authenticated", request)
            return HttpResponseRedirect('/login')               
    return func_wrapper

def public_view(func):
    def func_wrapper(request):
        log_user_activity("DEBUG", "Called", request)
        try:
            return func(request)
        except Exception as e:
            if isinstance(e, ErrorMessage):
                error_text = str(e)
            else:
                error_text = 'something went wrong'
                logger.error(format_exception(e))
            data = {'user': request.user,
                    'title': 'Error',
                    'error' : 'Error: "{}"'.format(error_text)}
        return render(request, 'error.html', {'data': data})           
    return func_wrapper





def login_view(request, template, redirect):
    
    # If authenticated user reloads the main URL
    if request.method == 'GET' and request.user.is_authenticated():
        return HttpResponseRedirect(redirect)
    
    # If unauthenticated user tries to log in
    if request.method == 'POST':
        if not request.user.is_authenticated():
            username = request.POST.get('username')
            password = request.POST.get('password')
            # Use Django's machinery to attempt to see if the username/password
            # combination is valid - a User object is returned if it is.
            
            if "@" in username:
                # Get the username from the email
                try:
                    user = User.objects.get(email=username)
                    username = user.username
                except User.DoesNotExist:
                    return render(request, template, {'error': 'Check email/password, cannot log in!'})
            
            if password:
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    return HttpResponseRedirect(redirect)
                else:
                    return render(request, template, {'error': 'Check user/password, cannot log in!'})
            else:
                
                # If empty password, send mail with login token
                logger.debug('Sending login token via mail to {}'.format(user.email))
                
                token = uuid.uuid4()
                
                # Create token or update if existent (and never used)
                try:
                    loginToken = LoginToken.objects.get(user=user)
                except LoginToken.DoesNotExist:     
                    LoginToken.objects.create(user=user, token=token)
                else:
                    loginToken.token = token
                    loginToken.save()
                
                send_email(to=user.email, subject='{} login link'.format(EDJANGO_PROJECT_NAME), text='Hello,\n\nhere is your login link: {}/login/?token={}\n\nOnce logged in, you can go to "My Account" and change password (or just keep using the login link feature).\n\nThe {} Team.'.format(EDJANGO_PUBLIC_HTTP_HOST, token, EDJANGO_PROJECT_NAME))
               
                # Return here, we don't want to give any hints about existing users
                data = {'success': 'Ok, if we have your data in our systems you will receive a login link by email shortly.'}
                return render(request, 'success.html', {'data': data})
                    
                
        else:
            # This should never happen.
            # User tried to log-in while already logged in: log him out and then render the login
            logout(request)        
              
    else:
        # If we are logging in through a token
        token = request.GET.get('token', None)
        logger.debug('TOKEN:"{}"'.format(token))
        if token:
            
            loginTokens = LoginToken.objects.filter(token=token)
            
            if not loginTokens:
                raise ErrorMessage('Token not valid or expired')
    
            
            if len(loginTokens) > 1:
                raise Exception('Consistency error: more than one user with the same login token ({})'.format(len(loginTokens)))
            
            # Use the first and only token (todo: use the objects.get and correctly handle its exceptions)
            loginToken = loginTokens[0]
            
            # Get the user from the table
            user = loginToken.user
            
            # Set auth backend
            user.backend = 'django.contrib.auth.backends.ModelBackend'
    
            # Ok, log in the user
            login(request, user)
            loginToken.delete()
            
            # Now redirect to site
            return HttpResponseRedirect(redirect)

                
    # All other cases, render the login page again
    return render(request, template)



def logout_view(request, redirect):
    logout(request)
    return HttpResponseRedirect(redirect)


def register_view(request, invitation_code):

    # user var
    user = None

    # Init data
    data={}
    data['user']   = request.user
    data['title'] = "Register"
    data['status'] = None

    # Get data
    email      = request.POST.get('email', None)
    password   = request.POST.get('password', None)
    invitation = request.POST.get('invitation', None) # Verification code set for anyone

    if request.user.is_authenticated():
        return (user, HttpResponseRedirect('/'))

    else:

        if email and password:
            
            # Check both email and password are set
            if not email:
                data['error'] = 'Missing email'
                return (user, render(request, 'error.html', {'data': data}))
         
            if not password:
                data['error'] = 'Missing password'
                return (user, render(request, 'error.html', {'data': data}))
         
            # Check if we have to validate an invitation code
            if invitation_code:
                if invitation != invitation_code:
                    data['status'] = 'wrong_invite'
                    return (user, render(request, 'register.html', {'data': data}))

            
            if not email in ONGOING_SIGNUPS:
                
                # Add user to recent signups dict
                ONGOING_SIGNUPS[email] = None
                
                # Check if user with this email already exists
                if len(User.objects.filter(email = email)) > 0:
                    data['error'] = 'The email address you entered is already registered.'
                    return (user, render(request, 'error.html', {'data': data}))
                
                # Register the user
                username = random_username(email) # It is actually a random string
                try:
                    user = User.objects.create_user(username, password=password, email=email)
                except Exception as e:
                    logger.error('Got exception when creating the user: {}'.format(format_exception(e)))
                    data['error'] = 'Error in creating the user. Please try again and if the error persists contact us at info@symplitica.com'
                    del ONGOING_SIGNUPS[email]
                    return (user, render(request, 'error.html', {'data': data}))

                # Is this necessary?
                user.save() 
                
                # Manually set the auth backend for the user
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                
                data['status'] = 'activated'
                data['user'] = user
                
                # Remove user from recent signups
                del ONGOING_SIGNUPS[email]
                
                return (user, render(request, 'register.html', {'data': data}))
            
            else:

                # Check previous requesta ctivated the user
                i=0
                while True:
                    if email not in ONGOING_SIGNUPS:
                        break
                    else:
                        time.sleep(1)
                        i+=1
                    if i>30:
                        data['error'] = 'Timed up. Your user might have been correctly created anyway. Please try to login if it does not work to signup again, if the error persists contact us at info@symplitica.com'
                        return (user, render(request, 'error.html', {'data': data}))

                users_with_this_email = User.objects.filter(email = email)
                if users_with_this_email<1:
                    data['error'] = 'Error in creating the user. Please try again and if the error persists contact us at info@symplitica.com'
                    return (user, render(request, 'error.html', {'data': data}))
                else:
                    data['status'] = 'activated'
                    data['user'] = users_with_this_email[0]
                    user = authenticate(username=users_with_this_email[0].username, password=password)
                    if not user:
                        data['error'] = 'Error. Please try again and if the error persists contact us at info@symplitica.com'
                        return (user, render(request, 'error.html', {'data': data}))
                    login(request, user)
                    return (user, render(request, 'register.html', {'data': data}))   

        else:
            return (user, render(request, 'register.html', {'data': data}))





