

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
from edjango.common.utils import send_email

from edjango.settings import EDJANGO_PROJECT_NAME, EDJANGO_PUBLIC_HTTP_HOST 

# Setup logging
import logging
logger = logging.getLogger(__name__)

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
                raise Exception('Token not valid or expired')
                #raise ErrorMessage('Token not valid or expired')
    
            
            if len(loginTokens) > 1:
                raise Exception('Consistency error: more than one user with the same login token ({})'.format(len(loginTokens)))
            
            # Use the first and only profile (todo: use the objects.get and correctly handle its exceptions)
            loginToken = loginTokens[0]
            
            # Get the user from the profile
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