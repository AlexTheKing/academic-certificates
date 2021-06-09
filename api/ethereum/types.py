from pydantic import constr

Address = constr(min_length=42, max_length=42, regex='0x[a-fA-F0-9]{40}')
Hash = constr(min_length=64, max_length=64, regex='(0x)?[a-fA-F0-9]{64}')
