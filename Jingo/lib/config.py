# default state name
STATE_NAME_DEFAULT     = 'myState'

# return dataset
RESULT_SUCCESS         = 1
RESULT_FAIL            = 0
MESSAGE_EMAIL_ERROR    = 'Sorry, you have a wrong email!'
MESSAGE_PASSWORD_ERROR = 'Your password is not correct!'
LOGOUT_FAIL            = 'Unknown reason causes you can\'t logout right now'
LOGOUT_SUCCESS         = 'You\'re logged out.'

# system tags
N_SYSTEM_TAGS          = 11

# include Project library 
from Jingo.lib.HttpRequestTasks import *
from Jingo.lib.DataVerification import *
from Jingo.lib.SQLExecution import *