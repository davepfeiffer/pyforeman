import foreman.blueprint
import queue

# TODO: parallelize builder calls

#--{ depth first construction }-------------------------------------------------
"""
This should probably be deprecated. This version is simple but may cause
duplication of work for dependent nodes / fanout.
"""

# constructs a blueprint in depth first fashion
def df_construct(blueprint, env=frozenset()):
  env_p = construct_foundation(blueprint.foundation, env)
  return blueprint.builder(env_p, blueprint.name, blueprint.materials)

# constructs foundation then add their materials to the environment
def construct_foundation(foundation, env):
  new_materials = []
  for blueprint in foundation:
    new_materials.append(df_construct(blueprint, env))
  return env.union(new_materials)

#--{ breadth first construction }-----------------------------------------------

# constructs a blueprint in breadth first fashion
# calls level builder between each level of the dependency graph
def bf_construct(blueprint, level_builder, env=frozenset()):
  q = queue.Queue()
  q.put((0, blueprint))
  lst = bf_collect(q, [])
  lst.reverse()
  last_level = -1
  for (level, bp) in lst:
    if last_level != level:
      level_builder(env)
      last_level = level
    env = env.union(bp.builder(env, bp.name, bp.materials))
  level_builder(env)

# do a breadth first traversal
def bf_collect(q, visited):
  print(q.qsize(), len(visited))
  if q.empty():
    print(len(visited))
    return visited
  else:
    level, blueprint = q.get()
    for _, other_blueprint in visited:
      if other_blueprint.name == blueprint.name: 
        return bf_collect(q, visited)

    visited.append((level, blueprint))
    for kid in blueprint.foundation:
      print(kid.name)
      q.put((level + 1, kid))
    return bf_collect(q, visited)

