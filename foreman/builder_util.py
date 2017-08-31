

class BuilderError(Exception):
  pass


def name_check(env, name):
  if name in env:
    raise BuilderError("Blueprint name conflict: {}".format(name))


def material_check(env, materials):
  if not materials <= env:
    missing = []
    for material in materials:
      if not material in env:
        missing.append(material)
    raise("Materials missing from environment: {}".format(missing))

