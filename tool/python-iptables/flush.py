import iptc
"""This script use for delete all chains  and rules non-builtin"""
table = iptc.Table(iptc.Table.FILTER)
# iptc.easy.delete_chain('filter', 'input', flush=True)
table.flush()

table.commit()
table.autocommit = True
