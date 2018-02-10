__all__ = [
  'catchfile',
  'servefile',
  'text',
  'authorize',
  'sleep',
  'log'
]

def isAllowed(action: str):
  return action in __all__

def run(action, app, route, request, sessionId):
  if isAllowed(action) == False:
    return None
  modules = globals()
  if action in modules:
    return modules[action].run(app, route, request, sessionId)
  return None