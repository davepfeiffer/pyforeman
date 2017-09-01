from makeshells import gcc_builders
from foreman import blueprint, foreman

if __name__ == "__main__":

  script_path = "./hello_build.sh"
  hello_build = gcc_builders.ShellScript(script_path)

  compiler = gcc_builders.hire_gcc_builder("gcc", "-Wall", hello_build)
  file_collector = gcc_builders.hire_file_collector(hello_build)

  hello_world_c = blueprint.Blueprint(
    name="hello_world.c",
    builder=file_collector,
    materials=[],
    foundation=[]
  )

  hello_world = blueprint.Blueprint(
    name="hello_world",
    builder=compiler,
    materials=[hello_world_c.name],
    foundation=[hello_world_c]
  )

  foreman.construct(hello_world, frozenset())
print("Generated: {}".format(script_path))