# form data error message
USERNAME_LENGTH        = 6
USERNAME_INVALID       = 'User name should be at least ' + str(USERNAME_LENGTH) + ' characters, including alphabet and digits.'
USERNAME_TOO_SHORT     = 'User name should be at least ' + str(USERNAME_LENGTH) + ' characters.'
EMAIL_TAKEN            = 'The email address is already taken.'
EMAIL_INVAILD          = 'The email address is invalid.'
PASSWORD_LENGTH        = 6
PASSWORD_INVALID       = 'Password should be at least ' + str(PASSWORD_LENGTH) + ' characters, including lowercase or uppercase alphabet and digits.'
PASSWORD_TOO_SHORT     = 'Password should be at least ' + str(PASSWORD_LENGTH) + ' characters.'
PASSWORD_CONFIRM_ERROR = 'The confirm-password does not match your password.'

# default state name
STATE_NAME_DEFAULT     = 'myState'

# return dataset
RESULT_SUCCESS         = 1
RESULT_FAIL            = 0
MESSAGE_REQUEST_ERROR  = 'Forbidden action!'
MESSAGE_EMAIL_ERROR    = 'Sorry, you have a wrong email!'
MESSAGE_PASSWORD_ERROR = 'Your password is not correct!'
LOGOUT_FAIL            = 'Unknown reason causes you can\'t logout right now'
LOGOUT_SUCCESS         = 'You\'re logged out.'

# filter and system tags
N_SYSTEM_TAGS          = 11
IS_CHECKED_DEFAULT     = 1
N_START_TIME           = '2000-01-01 00:00:00'
N_STOP_TIME            = '2000-12-31 23:59:59'

# post notes 
N_DEFAULT_RADIUS       = 200
IS_COMMENT             = 1
N_LIKES                = 0
SPLITTER_SYMBOL        = '_'
NORMAL_DATE_PATTERN    = '%Y-%m-%d %H:%M:%S'

# include Project library 
from Jingo.lib.HttpRequestTasks import *
from Jingo.lib.DataVerification import *
from Jingo.lib.SQLExecution import *