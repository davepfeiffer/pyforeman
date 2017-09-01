import foreman.blueprint

# TODO: parallelize builder calls

# Blueprint Tuple -> Material Set -> Material Set
def construct_foundation(foundation, env):
  new_materials = []
  for blueprint in foundation:
    new_materials.append(construct(blueprint, env))
  return env.union(new_materials)

# Blueprint -> Material Set -> Material Set
def construct(blueprint, env=frozenset()):
  env_p = construct_foundation(blueprint.foundation, env)
  return blueprint.builder(env_p, blueprint.name, blueprint.materials)
