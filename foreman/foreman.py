from architect import Blueprint

# TODO: parallelize builder calls
class Foreman:

  # Blueprint Tuple -> Material Set -> Material Set
  def construct_list(blueprints, env):
    new_materials = []
    for blueprint in blueprints:
      new_materials.append(construct(blueprint, env))
    return env.union(new_materials)

  # Blueprint -> Material Set -> Material Set
  def construct(blueprint, env): 
    env_p = construct_list(blueprint.foundation, env)
    return blueprint.builder(env_p, blueprint.name, blueprint.materials)
