# eDjango

An extended Django, for avoing to write the same stuff over and over again. Makes strong use of fabric for automating tasks.

By default uses Django version 1.8.4 but should work up to the latest official version - just change it in the requirements.


Usage:
------

Clone/download the repo, install requirements, and create you app in eDjango/edjango/your_project_app. You probably want to hardlink against another folder/repo. Note that the suffix "_app" is mandatory.


The structure for "your_project_app" is then almost the same as an usual (entire) Django project - except that in this case is completely decoupled from Django itself.


It has to include the standard models.py, settings.py, urls.py and views.py files, as well as the static and templates folders.

That's it, eDjango implements automatic app disovery so yo don't have to do anything else.