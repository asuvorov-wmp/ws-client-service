import os
import sys

from django.core.wsgi import get_wsgi_application


project_dir = os.path.dirname(__file__)

sys.path.append(project_dir)
sys.path.append(os.path.join(project_dir, "epa"))

application = get_wsgi_application()
