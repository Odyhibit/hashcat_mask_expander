This is small Python script that takes input similar to a HashCat mask, and creates a wordlist file.

The wildcards available
  ?l = abcdefghijklmnopqrstuvwxyz
  ?u = ABCDEFGHIJKLMNOPQRSTUVWXYZ
  ?d = 0123456789
  ?h = 0123456789abcdef
  ?H = 0123456789ABCDEF
  ?s = «space»!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
  ?a = ?l?u?d?s

It's faster to just use HashCat, but if you want to use Python here ya go.
