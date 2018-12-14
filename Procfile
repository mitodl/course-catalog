web: bin/start-nginx bin/start-pgbouncer-stunnel newrelic-admin run-program uwsgi uwsgi.ini
worker: celery -A course_catalog.celery:app worker -B -l $COURSE_CATALOG_LOG_LEVEL
extra_worker: celery -A course_catalog.celery:app worker -l $COURSE_CATALOG_LOG_LEVEL
