all
# Set unordered list preference
rule 'MD004', :style => :consistent
# Be explicit about desired indent level
rule 'MD007', :indent => 3
# Ignore line length rule in code blocks
rule 'MD013', :code_blocks => false
# Use ordered style for numbered lists
rule 'MD029', :style => :ordered
# Allow leading $ sign in console commands
exclude_rule 'MD014'
# Allow html tag syntax (<tag>) in docs. Not used as tags in
# our case, but to show command line options.
exclude_rule 'MD033'
# Allow bare URLs
exclude_rule 'MD034'
# Allow for anchors at start of file, otherwise they are
# not found in cross-referencing
exclude_rule 'MD041'
