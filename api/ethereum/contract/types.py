from pydantic import constr

String16 = constr(max_length=16)
String32 = constr(max_length=32)
String36 = constr(max_length=36)
String48 = constr(max_length=48)
String64 = constr(max_length=64)
