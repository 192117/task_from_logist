

def error_message(error, args=None):
    message = {
        'Event': 'Error',
        'Detail': error,
        'Arguments': args
    }
    return message