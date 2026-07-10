import os

HERE = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(os.path.dirname(HERE), "samples", "vat_script.txt")

with open(script_path, "r", encoding="utf-8") as f:
    text = f.read()

# Search specifically for "apply" followed by whatever comes next -
# this targets the exact penalties sentence, not just any "starting" in the file
idx = text.find("penalties apply")
if idx == -1:
    print("Could not find 'penalties apply' in the file at all - check spelling/wording.")
else:
    snippet = text[idx:idx+60]
    print("Raw snippet:", repr(snippet))
    print("Character codes:")
    for ch in snippet:
        print(f"  {repr(ch)} -> U+{ord(ch):04X}")

# Also report how many times "starting" appears total, in case there's more than one
count = text.lower().count("starting")
print(f"\n'starting' appears {count} time(s) in the file.")