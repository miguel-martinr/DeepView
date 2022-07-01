def printExceptionMessage(e: Exception):
  currentException = e.__cause__
  
  if currentException is not None:    
    while currentException.__cause__ is not None:
      currentException = currentException.__cause__
  
  if hasattr(e, 'details'):
    details = e.details
    writeErrors = details['writeErrors']
    return writeErrors[0]['errmsg']

  if hasattr(e, 'message'):
    return str(e.message)

  return 'Unknown cause'