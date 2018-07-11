# eDjango

An extended Django, for avoing to write the same stuff over and over again. Makes strong use of fabric for automating tasks.

By default uses Django version 1.8.4 but should work up to the latest official version - just change it in the requirements.


Usage:
------

Clone/download the repo, install requirements, and create you app in eDjango/edjango/your_app. You probably want to hardlink against another folder/repo. Note that the suffix "_app" is mandatory.


The structure for "your_app" is then almost the same as an usual (entire) Django project - except that in this case is completely decoupled from Django itself.


It has to include the standard models.py, settings.py, urls.py and views.py files, as well as the static and templates folders.

That's it, eDjango implements automatic app disovery so yo don't have to do anything else.


Configuration:
------

You can configure things like project name, databse parameters, log levels and email service via environment variables. A list of the configurable environments variables with their default values is shown below. The accepted lovels are: DEBUG, INFO, WARNING, ERROR, CRITICAL.


	# Project conf
    EDJANGO_EMAIL_FROM="info@metabox.online"
    EDJANGO_EMAIL_APIKEY=None
    EDJANGO_PROJECT_NAME="MetaBox"
    EDJANGO_PUBLIC_HTTP_HOST="https://metabox.online"

	# Dabase conf (Sqlite, default)
	DJANGO_DB_NAME="/data/edjango.sqlite3"

	# Dabase conf (Postgres)
	DJANGO_DB_ENGINE="django.db.backends.postgresql_psycopg2"
	DJANGO_DB_NAME="dbname"
	DJANGO_DB_USER="user"
	DJANGO_DB_PASSWORD="password"
	DJANGO_DB_HOST="my.postgres.host"
	DJANGO_DB_PORT=5432

	# Logging
	DJANGO_LOG_LEVEL=ERROR
	EDJANGO_LOG_LEVEL=ERROR
	
	# Debugging
	DJANGO_DEBUG=False

Setting the DJANGO_DEBUG mode causes to enable the devleopment server in full mode, to have much more verbose 500 error pages with all the stack traces and context (the classic Django yellow page) and to have stacktraces logged on more than one line (by defautl they are logged one per line to play nice with log aggregation tools)

If DJANGO_DEBUG is not set the development server can still run but it will hide all info abiut errors an serve static files only if the eDjango project is composed by only one app (excluding the base_app). This is useful for beta testing but for real production you should use a proper server and use the "collect static" machinery.



	





