
# Container class
class Blueprint:
  def __init__(self, name, builder, materials, foundation):
    self.name = name                        # String: uid of target material
    self.builder = builder                  # Builder closure
    self.materials = frozenset(materials)   # Frozenset of Strings (material uids)
    self.foundation = frozenset(foundation) # List of Blueprints
