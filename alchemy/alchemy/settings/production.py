from base import *

########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION

# Make this unique, and don't share it with anybody.
#SECRET_KEY = 'd()n*zeja_hhr@na6zi(_4db+25ib1v(u8$c7hmsd9n9#=sw0o'
########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = get_env_variable("DJANGO_SECRET_KEY")
########## END SECRET CONFIGURATION
