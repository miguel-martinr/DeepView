def printExceptionMessage(e: Exception):
  currentException = e.__cause__
  while currentException.__cause__ is not None:
    currentException = currentException.__cause__
  
  details = currentException.details
  writeErrors = details['writeErrors']
  return writeErrors[0]['errmsg']