all
# Set unordered list preference
rule 'MD004', :style => :consistent
# Be explicit about desired indent level
rule 'MD007', :indent => 3
# Ignore line length rule in code blocks
rule 'MD013', :code_blocks => false
# Use ordered style for numbered lists
rule 'MD029', :style => :ordered
