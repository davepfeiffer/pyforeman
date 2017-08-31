

class BuilderError(Exception):
  pass

# this is a bad way to do things, but it's quick to write
class ShellScript:
  def __init__(self, path):
    self.path = path
    self.append_command("#!/bin/sh")

  def append_command(self, command):
    with open(self.path, "a") as s:
      s.write(command + "\n")

# python imports . . .
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


def hire_file_collector(script):
  def builder(env, target, materials):
    name_check(env, target)
    material_check(env, materials)
    script.append_command(
          "test -e {} || (echo '{} not found' && exit 1)".format(target, target))
    script.append_command("")
    return target
  return builder

def hire_gcc_builder(gcc_path, flags, script):
  def builder(env, target, materials):
    name_check(env, target)         # ensure target is unique
    material_check(env, materials)  # ensure required materials are present
    sources = " "
    for m in materials:
      sources += m + " " 
    script.append_command("# {}".format(target))
    # TODO: insert cmds to check if the target is newer than the dependancies
    script.append_command(
                      "{} {}{}-o {}".format(gcc_path, flags, sources, target))
    script.append_command("")
    return target
  return builder
