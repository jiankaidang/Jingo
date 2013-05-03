# default state name
STATE_NAME_DEFAULT     = 'myState'

# return dataset
RESULT_SUCCESS         = 1
RESULT_FAIL            = 0
MESSAGE_EMAIL_ERROR    = 'Sorry, you have a wrong email!'
MESSAGE_PASSWORD_ERROR = 'Your password is not correct!'
LOGOUT_FAIL            = 'Unknown reason causes you can\'t logout right now'
LOGOUT_SUCCESS         = 'You\'re logged out.'

# filter and system tags
N_SYSTEM_TAGS          = 11
IS_CHECKED_DEFAULT     = 1

# post notes 
N_DEFAULT_RADIUS       = 200
IS_COMMENT             = 1
N_LIKES                = 0

# include Project library 
from Jingo.lib.HttpRequestTasks import *
from Jingo.lib.DataVerification import *
from Jingo.lib.SQLExecution import *