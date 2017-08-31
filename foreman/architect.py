
# Container class
class Blueprint:
  def __init__(name, builder, materials, foundation):
    self.name = name              # String: uid of target material
    self.builder = builder        # Builder llambda
    self.materials = materials    # Frozenset of Strings (material uids)
    self.foundation = foundation  # Tuple of Blueprints
